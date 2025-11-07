# ------------------------------------------------------------
# API Flask - Sprint 4 (Python)
# Integrada ao banco Oracle e à API Java
# ------------------------------------------------------------

import os

# Define qual banco usar de acordo com o ambiente
if os.environ.get("RENDER", "false").lower() == "true":
    import banco_render as banco
else:
    import banco_oracle as banco

from flask import Flask, jsonify, request
from flask_cors import CORS
import banco_oracle

banco_oracle.inserir_dados_iniciais()

app = Flask(__name__)
CORS(app)


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


@app.route("/pacientes", methods=["GET"])
def listar_pacientes():
    try:
        dados = banco_oracle.listar_pacientes()
        return jsonify(dados), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@app.route("/pacientes", methods=["POST"])
def criar_paciente():
    dados = request.get_json()
    resposta, status = banco_oracle.inserir_paciente(dados)
    return jsonify(resposta), status


@app.route("/pacientes/<id>", methods=["PUT"])
def atualizar_paciente_endpoint(id):
    dados = request.get_json()
    ok, resposta, status = banco_oracle.atualizar_paciente(id, dados)
    return jsonify(resposta), status


@app.route("/pacientes/<id>", methods=["DELETE"])
def deletar_paciente(id):
    if banco_oracle.excluir_paciente(id):
        return "", 204
    else:
        return jsonify({"erro": "Paciente não encontrado"}), 404
    

@app.route("/medicos", methods=["GET"])
def listar_medicos_endpoint():
    return jsonify(banco_oracle.listar_medicos())


@app.route("/medicos/<id>", methods=["GET"])
def buscar_medico_endpoint(id):
    medico = banco_oracle.buscar_medico_por_id(id)
    if medico:
        return jsonify(medico)
    return jsonify({"erro": "Médico não encontrado"}), 404


@app.route("/medicos", methods=["POST"])
def criar_medico_endpoint():
    dados = request.get_json()
    resposta, status = banco_oracle.inserir_medico(dados)
    return jsonify(resposta), status


@app.route("/medicos/<id>", methods=["PUT"])
def atualizar_medico_endpoint(id):
    dados = request.get_json()
    ok, resposta, status = banco_oracle.atualizar_medico(id, dados)
    return jsonify(resposta), status


@app.route("/medicos/<id>", methods=["DELETE"])
def remover_medico_endpoint(id):
    ok = banco_oracle.remover_medico(id)
    if not ok:
        return jsonify({"erro": "Médico não encontrado"}), 404
    return "", 204


@app.route("/consultas", methods=["GET"])
def listar_consultas():
    try:
        conn = banco_oracle.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ID_CONSULTA, DT_HR_CONSULTA, DS_MODALIDADE FROM T_HC_CONSULTA ORDER BY ID_CONSULTA")
        consultas = [
            {"id": r[0], "dataHora": str(r[1]), "modalidade": r[2]}
            for r in cursor.fetchall()
        ]
        cursor.close()
        conn.close()
        return jsonify(consultas), 200
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

    resposta, status = banco_oracle.inserir_consulta(dados)
    return jsonify(resposta), status



@app.route("/consultas/<id>", methods=["PUT"])
def atualizar_consulta_endpoint(id):
    dados = request.get_json()
    ok, resposta, status = banco_oracle.atualizar_consulta(id, dados)
    return jsonify(resposta), status


@app.route("/consultas/<id>", methods=["DELETE"])
def deletar_consulta_endpoint(id):
    ok, resposta, status = banco_oracle.deletar_consulta(id)
    return jsonify(resposta), status


@app.route("/exportar", methods=["GET"])
def exportar_json():
    try:
        relatorio = banco_oracle.exportar_dados_json()
        return jsonify({
            "mensagem": "Relatório gerado com sucesso!",
            "total_pacientes": relatorio["total_pacientes"]
        }), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)