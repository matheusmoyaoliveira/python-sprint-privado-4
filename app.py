# ------------------------------------------------------------
# API Flask - Sprint 4 (Python)
# Integrada ao banco Oracle e à API Java
# ------------------------------------------------------------

import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import gdown
import joblib

# ------------------------------------------------------------
# Seleciona o banco conforme o ambiente
# ------------------------------------------------------------
if os.environ.get("RENDER", "false").lower() == "true":
    import banco_render as banco
else:
    import banco_oracle as banco

# ------------------------------------------------------------
# Inicializa a aplicação Flask
# ------------------------------------------------------------
app = Flask(__name__)
CORS(app)

# Executa carga inicial de dados apenas se estiver no Oracle
if hasattr(banco, "inserir_dados_iniciais"):
    try:
        banco.inserir_dados_iniciais()
    except Exception as e:
        print(f"⚠️ Erro ao inserir dados iniciais: {e}")


# ------------------------------------------------------------
# Rota inicial (Home)
# ------------------------------------------------------------
@app.route("/")
def home():
    return """
    <html>
      <body style='font-family: Arial; background:#f7f7f7; color:#333; padding:20px'>
        <h2>🚀 API Python Sprint 4 - FIAP</h2>
        <p>Integração com Banco Oracle, Machine Learning e Front-end.</p>
        <hr>
        <h3>🔗 Endpoints disponíveis:</h3>
        <ul>
          <li><b>Pacientes:</b> /pacientes</li>
          <li><b>Médicos:</b> /medicos</li>
          <li><b>Consultas:</b> /consultas</li>
          <li><b>Exportar JSON:</b> /exportar</li>
          <li><b>IA Predict:</b> /predict</li>
        </ul>
        <p><b>Integrantes:</b> Matheus Moya de Oliveira     - RM 562822</p>
        <p><b>Integrantes:</b> Ana Carolina Pereira Fontes  - RM 562145</p>
        <p><b>Integrantes:</b> Daniel Nicolas Leoterio      - RM 562186</p>
      </body>
    </html>
    """


# ------------------------------------------------------------
# PACIENTES
# ------------------------------------------------------------
@app.route("/pacientes", methods=["GET"])
def listar_pacientes():
    try:
        dados = banco.listar_pacientes()
        return jsonify(dados), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@app.route("/pacientes", methods=["POST"])
def criar_paciente():
    dados = request.get_json()
    resposta, status = banco.inserir_paciente(dados)
    return jsonify(resposta), status


@app.route("/pacientes/<id>", methods=["PUT"])
def atualizar_paciente_endpoint(id):
    dados = request.get_json()
    ok, resposta, status = banco.atualizar_paciente(id, dados)
    return jsonify(resposta), status


@app.route("/pacientes/<id>", methods=["DELETE"])
def deletar_paciente(id):
    if banco.excluir_paciente(id):
        return "", 204
    else:
        return jsonify({"erro": "Paciente não encontrado"}), 404


# ------------------------------------------------------------
# MÉDICOS
# ------------------------------------------------------------
@app.route("/medicos", methods=["GET"])
def listar_medicos_endpoint():
    return jsonify(banco.listar_medicos())


@app.route("/medicos/<id>", methods=["GET"])
def buscar_medico_endpoint(id):
    medico = banco.buscar_medico_por_id(id)
    if medico:
        return jsonify(medico)
    return jsonify({"erro": "Médico não encontrado"}), 404


@app.route("/medicos", methods=["POST"])
def criar_medico_endpoint():
    dados = request.get_json()
    resposta, status = banco.inserir_medico(dados)
    return jsonify(resposta), status


@app.route("/medicos/<id>", methods=["PUT"])
def atualizar_medico_endpoint(id):
    dados = request.get_json()
    ok, resposta, status = banco.atualizar_medico(id, dados)
    return jsonify(resposta), status


@app.route("/medicos/<id>", methods=["DELETE"])
def remover_medico_endpoint(id):
    ok = banco.remover_medico(id)
    if not ok:
        return jsonify({"erro": "Médico não encontrado"}), 404
    return "", 204


# ------------------------------------------------------------
# CONSULTAS
# ------------------------------------------------------------
@app.route("/consultas", methods=["GET"])
def listar_consultas():
    try:
        dados = banco.listar_consultas()
        return jsonify(dados), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@app.route("/consultas", methods=["POST"])
def criar_consulta():
    dados = request.get_json() or {}

    if "dataHora" in dados:
        dados["dataHora"] = (
            dados["dataHora"].replace("T", " ").split(".")[0].strip()
        )
        if len(dados["dataHora"].split(":")) == 2:
            dados["dataHora"] += ":00"

    print(">>> DADOS ENVIADOS PARA O BANCO:", dados)

    resposta, status = banco.inserir_consulta(dados)
    return jsonify(resposta), status


@app.route("/consultas/<id>", methods=["PUT"])
def atualizar_consulta_endpoint(id):
    dados = request.get_json()
    ok, resposta, status = banco.atualizar_consulta(id, dados)
    return jsonify(resposta), status


@app.route("/consultas/<id>", methods=["DELETE"])
def deletar_consulta_endpoint(id):
    ok, resposta, status = banco.deletar_consulta(id)
    return jsonify(resposta), status


# ------------------------------------------------------------
# EXPORTAÇÃO
# ------------------------------------------------------------
@app.route("/exportar", methods=["GET"])
def exportar_json():
    try:
        relatorio = banco.exportar_dados_json()
        return jsonify({
            "mensagem": "Relatório gerado com sucesso!",
            "total_pacientes": relatorio.get("total_pacientes", 0)
        }), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# ------------------------------------------------------------
# PREDICT
# ------------------------------------------------------------
@app.route('/predict', methods=['POST'])
def prever_comparecimento():
    try:
        # 🔹 ID do arquivo do Google Drive (pegamos da URL que você mandou)
        file_id = "1YcOlIeY-aBSM7BKn1G64wg83xnHaM0Tk"
        output = "modelo_regressao.joblib"

        # 🔹 Só baixa o modelo se ainda não existir no servidor (Render)
        if not os.path.exists(output):
            gdown.download(f"https://drive.google.com/uc?id={file_id}", output, quiet=False)

        # 🔹 Carrega o modelo
        modelo = joblib.load(output)

        # 🔹 Lê os dados enviados no JSON (exemplo: {"idade": 40, "dias_espera": 15, "historico_faltas": 1})
        dados = request.json
        X = [[
            dados.get("idade", 0),
            dados.get("dias_espera", 0),
            dados.get("historico_faltas", 0)
        ]]

        # 🔹 Faz a previsão (supondo que o modelo seja de classificação com predict_proba)
        if hasattr(modelo, "predict_proba"):
            probabilidade = modelo.predict_proba(X)[0][1] * 100
        else:
            probabilidade = modelo.predict(X)[0] * 100

        return jsonify({
            "mensagem": "Previsão gerada com sucesso!",
            "probabilidade_comparecimento": f"{probabilidade:.2f}%"
        })

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# ------------------------------------------------------------
# EXECUÇÃO
# ------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
