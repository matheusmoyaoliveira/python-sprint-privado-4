# ------------------------------------------------------------
# API Flask - Sprint 4 (Python)
# Integrada ao banco Oracle e à API Java
# ------------------------------------------------------------

import os
from flask import Flask, jsonify, request, send_file, render_template, flash, redirect, url_for
from flask_cors import CORS
import gdown
import joblib
import pandas as pd

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
app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "neuroai-front-secret"
CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:5000", "http://localhost:5000"]}})


# ------------------------------------------------------------
# Helpers de mensagens
# ------------------------------------------------------------
def flash_ok(msg: str):
    flash(msg, "success")

def flash_err(msg: str):
    flash(msg, "danger")

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
def index():
    return render_template("index.html")

    
# ------------------------------------------------------------
# FRONT-END: PACIENTES
# ------------------------------------------------------------
@app.route("/pacientes", methods=["GET"])
def pacientes_listar():
    try:
        data = banco.listar_pacientes()
        return render_template("pacientes.html", pacientes=data)
    except Exception as e:
        flash_err(f"Erro ao listar pacientes: {e}")
        return render_template("pacientes.html", pacientes=[])

@app.route("/pacientes/novo", methods=["POST"])
def pacientes_novo():
    try:
        payload = {
            "nome": request.form.get("nome", "").strip(),
            "cpf": request.form.get("cpf", "").strip(),
            "rg": request.form.get("rg", "").strip(),
            "altura": request.form.get("altura", "").strip(),
            "peso": request.form.get("peso", "").strip(),
            "data_nascimento": request.form.get("data_nascimento", "").strip(),
            "escolaridade": request.form.get("escolaridade", "").strip(),
            "estado_civil": request.form.get("estado_civil", "").strip(),
            "descricao": request.form.get("descricao", "").strip()
        }
        banco.inserir_paciente(payload)
        flash_ok("✅ Paciente adicionado com sucesso!")
    except Exception as e:
        flash_err(f"❌ Erro ao adicionar paciente: {e}")
    return redirect(url_for("pacientes_listar"))

@app.route("/pacientes/<int:pid>/excluir", methods=["POST"])
def pacientes_excluir(pid):
    try:
        banco.excluir_paciente(pid)
        flash_ok("🗑️ Paciente excluído com sucesso!")
    except Exception as e:
        flash_err(f"❌ Erro ao excluir paciente: {e}")
    return redirect(url_for("pacientes_listar"))

@app.route("/pacientes/<int:pid>/editar", methods=["POST"])
def pacientes_editar(pid):
    try:
        payload = {
            "nome": request.form.get("nome", "").strip(),
            "cpf": request.form.get("cpf", "").strip(),
            "rg": request.form.get("rg", "").strip(),
            "altura": request.form.get("altura", "").strip(),
            "peso": request.form.get("peso", "").strip(),
            "data_nascimento": request.form.get("data_nascimento", "").strip(),
            "escolaridade": request.form.get("escolaridade", "").strip(),
            "estado_civil": request.form.get("estado_civil", "").strip(),
            "descricao": request.form.get("descricao", "").strip()
        }
        banco.atualizar_paciente(pid, payload)
        flash_ok("✏️ Paciente atualizado com sucesso!")
    except Exception as e:
        flash_err(f"❌ Erro ao atualizar paciente: {e}")
    return redirect(url_for("pacientes_listar"))

# ================== API JSON ==================
from flask import jsonify, request

pacientes_json = [
    {"id": 1, "nome": "João da Silva", "idade": 45, "cpf": "123.456.789-00", "telefone": "(11) 98888-1111"},
    {"id": 2, "nome": "Maria Oliveira", "idade": 32, "cpf": "987.654.321-00", "telefone": "(11) 97777-2222"},
    {"id": 3, "nome": "Pedro Santos", "idade": 29, "cpf": "111.222.333-44", "telefone": "(11) 96666-3333"}
]

@app.route("/api/pacientes", methods=["GET"])
def api_listar_pacientes():
    """Retorna todos os pacientes em formato JSON"""
    return jsonify(pacientes_json)

@app.route("/api/pacientes", methods=["POST"])
def api_criar_paciente():
    """Cria novo paciente via JSON"""
    data = request.get_json()
    novo = {
        "id": len(pacientes_json) + 1,
        "nome": data.get("nome", ""),
        "idade": data.get("idade", ""),
        "cpf": data.get("cpf", ""),
        "telefone": data.get("telefone", "")
    }
    pacientes_json.append(novo)
    return jsonify(novo), 201

@app.route("/api/pacientes/<int:id>", methods=["PUT"])
def api_atualizar_paciente(id):
    data = request.get_json()
    for p in pacientes_json:
        if p["id"] == id:
            p["nome"] = data.get("nome", p["nome"])
            p["idade"] = data.get("idade", p["idade"])
            p["cpf"] = data.get("cpf", p["cpf"])
            p["telefone"] = data.get("telefone", p["telefone"])
            return jsonify(p), 200
    return jsonify({"error": "Paciente não encontrado"}), 404

@app.route("/api/pacientes/<int:id>", methods=["DELETE"])
def api_excluir_paciente(id):
    """Exclui paciente via JSON"""
    global pacientes_json
    pacientes_json = [p for p in pacientes_json if p["id"] != id]
    return jsonify({"message": "Paciente removido com sucesso"}), 200


# ------------------------------------------------------------
# FRONT-END: MÉDICOS
# ------------------------------------------------------------
@app.route("/medicos", methods=["GET"])
def medicos_listar():
    try:
        data = banco.listar_medicos()
        return render_template("medicos.html", medicos=data)
    except Exception as e:
        flash_err(f"Erro ao listar médicos: {e}")
        return render_template("medicos.html", medicos=[])

@app.route("/medicos/novo", methods=["POST"])
def medicos_novo():
    try:
        payload = {
            "nome": request.form.get("nome", "").strip(),
            "crm": request.form.get("crm", "").strip(),
            "especialidade": request.form.get("especialidade", "").strip(),
            "telefone": request.form.get("telefone", "").strip(),
            "email": request.form.get("email", "").strip()
        }
        banco.inserir_medico(payload)
        flash_ok("✅ Médico adicionado com sucesso!")
    except Exception as e:
        flash_err(f"❌ Erro ao adicionar médico: {e}")
    return redirect(url_for("medicos_listar"))

@app.route("/medicos/<int:mid>/excluir", methods=["POST"])
def medicos_excluir(mid):
    try:
        banco.remover_medico(mid)
        flash_ok("🗑️ Médico excluído com sucesso!")
    except Exception as e:
        flash_err(f"❌ Erro ao excluir médico: {e}")
    return redirect(url_for("medicos_listar"))

@app.route("/medicos/<int:mid>/editar", methods=["POST"])
def medicos_editar(mid):
    try:
        payload = {
            "nome": request.form.get("nome", "").strip(),
            "crm": request.form.get("crm", "").strip(),
            "especialidade": request.form.get("especialidade", "").strip(),
            "telefone": request.form.get("telefone", "").strip(),
            "email": request.form.get("email", "").strip()
        }
        banco.atualizar_medico(mid, payload)
        flash_ok("✏️ Médico atualizado com sucesso!")
    except Exception as e:
        flash_err(f"❌ Erro ao atualizar médico: {e}")
    return redirect(url_for("medicos_listar"))

# ===================== API MÉDICOS =====================
from flask import jsonify, request

medicos_json = [
    {"id": 1, "nome": "Dr. João Almeida Jr.", "crm": "CRM-12345", "especialidade": "Cardiologia"},
    {"id": 2, "nome": "Dra. Paula Castro", "crm": "CRM-67890", "especialidade": "Neurologia"},
]

@app.route("/api/medicos", methods=["GET"])
def listar_medicos():
    return jsonify(medicos_json)

@app.route("/api/medicos", methods=["POST"])
def adicionar_medico():
    data = request.get_json()
    novo = {
        "id": len(medicos_json) + 1,
        "nome": data.get("nome", ""),
        "crm": data.get("crm", ""),
        "especialidade": data.get("especialidade", "")
    }
    medicos_json.append(novo)
    return jsonify(novo), 201

@app.route("/api/medicos/<int:id>", methods=["PUT"])
def atualizar_medico(id):
    data = request.get_json()
    for m in medicos_json:
        if m["id"] == id:
            m["nome"] = data.get("nome", m["nome"])
            m["crm"] = data.get("crm", m["crm"])
            m["especialidade"] = data.get("especialidade", m["especialidade"])
            return jsonify(m), 200
    return jsonify({"error": "Médico não encontrado"}), 404

@app.route("/api/medicos/<int:id>", methods=["DELETE"])
def excluir_medico(id):
    global medicos_json
    medicos_json = [m for m in medicos_json if m["id"] != id]
    return jsonify({"message": "Médico removido com sucesso"}), 200


# ------------------------------------------------------------
# FRONT-END: CONSULTAS
# ------------------------------------------------------------
@app.route("/consultas", methods=["GET"])
def consultas_listar():
    try:
        data = banco.listar_consultas()
        return render_template("consultas.html", consultas=data)
    except Exception as e:
        flash_err(f"Erro ao listar consultas: {e}")
        return render_template("consultas.html", consultas=[])

@app.route("/consultas/novo", methods=["POST"])
def consultas_novo():
    try:
        payload = {
            "dataHora": request.form.get("dataHora", "").strip(),
            "modalidade": request.form.get("modalidade", "").strip(),
            "idPaciente": request.form.get("idPaciente", type=int, default=2),
            "idMedico": request.form.get("idMedico", type=int, default=1)
        }
        banco.inserir_consulta(payload)
        flash_ok("✅ Consulta agendada com sucesso!")
    except Exception as e:
        flash_err(f"❌ Erro ao agendar consulta: {e}")
    return redirect(url_for("consultas_listar"))

@app.route("/consultas/<int:cid>/excluir", methods=["POST"])
def consultas_excluir(cid):
    try:
        banco.deletar_consulta(cid)
        flash_ok("🗑️ Consulta excluída com sucesso!")
    except Exception as e:
        flash_err(f"❌ Erro ao excluir consulta: {e}")
    return redirect(url_for("consultas_listar"))


# ------------------------------------------------------------
# EXPORTAÇÃO
# ------------------------------------------------------------
@app.route("/exportar", methods=["GET"])
def exportar_json():
    try:
        relatorio = banco.exportar_dados_json()

        # Garante que o arquivo exista
        caminho_arquivo = "./relatorio_api.json"
        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            import json
            json.dump(relatorio, f, ensure_ascii=False, indent=4)

        # Envia o arquivo para download
        return send_file(
            caminho_arquivo,
            mimetype="application/json",
            as_attachment=True,
            download_name="relatorio_api.json"
        )

    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    

# ------------------------------------------------------------
# FRONT-END: EXPORTAR RELATÓRIO
# ------------------------------------------------------------
@app.route("/exportar/view", methods=["GET"])
def exportar_view():
    """
    Página com botão para baixar o relatório completo da API
    """
    return render_template("exportar.html")


# ------------------------------------------------------------
# PREDICT
# ------------------------------------------------------------

@app.route('/predict', methods=['POST'])
def prever_comparecimento():
    try:
        file_id = "1YcOlIeY-aBSM7BKn1G64wg83xnHaM0Tk"
        output = "modelo_regressao.joblib"

        # Baixa o modelo se ainda não existir
        if not os.path.exists(output):
            gdown.download(f"https://drive.google.com/uc?id={file_id}", output, quiet=False)

        modelo = joblib.load(output)

        # Lê o JSON enviado
        dados = request.json

        # Monta DataFrame com as chaves exatamente iguais às usadas no treino
        X = pd.DataFrame([dados])

        # Verifica se todas as colunas necessárias estão presentes
        colunas_esperadas = [
            'scholarship', 'neighbourhood', 'gender', 'age', 'appt_dow', 'handcap',
            'waiting_days', 'hipertension', 'sms_received', 'alcoholism',
            'is_weekend', 'sched_hour', 'diabetes'
        ]
        faltando = [c for c in colunas_esperadas if c not in X.columns]
        if faltando:
            return jsonify({"erro": f"Campos ausentes: {faltando}"}), 400

        # Faz a previsão
        if hasattr(modelo, "predict_proba"):
            probabilidade = modelo.predict_proba(X)[0][1] * 100
        else:
            probabilidade = modelo.predict(X)[0] * 100

        return jsonify({
            "mensagem": "Previsão gerada com sucesso!",
            "probabilidade_comparecimento": f"{probabilidade:.2f}%",
            "interpretacao": "Alta chance de comparecimento" if probabilidade > 70 else "Risco de falta"
        })

    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    

# ------------------------------------------------------------
# FRONT-END: PREDICT VIA FORM
# ------------------------------------------------------------
@app.route("/predict/view", methods=["GET"])
def predict_view():
    """
    Página HTML com o formulário de previsão
    """
    return render_template("predict.html")


@app.route("/predict/submit", methods=["POST"])
def predict_submit():
    """
    Processa o formulário do HTML e mostra o resultado na tela
    """
    try:
        # Carrega o modelo (baixa se não existir)
        file_id = "1YcOlIeY-aBSM7BKn1G64wg83xnHaM0Tk"
        output = "modelo_regressao.joblib"
        if not os.path.exists(output):
            gdown.download(f"https://drive.google.com/uc?id={file_id}", output, quiet=False)
        modelo = joblib.load(output)

        # Coleta dados do formulário
        dados = {
            "scholarship": int(request.form.get("scholarship", 0)),
            "neighbourhood": request.form.get("neighbourhood", "UNKNOWN"),
            "gender": request.form.get("gender", "F"),
            "age": int(request.form.get("age", 0)),
            "appt_dow": int(request.form.get("appt_dow", 0)),
            "handcap": int(request.form.get("handcap", 0)),
            "waiting_days": int(request.form.get("waiting_days", 0)),
            "hipertension": int(request.form.get("hipertension", 0)),
            "sms_received": int(request.form.get("sms_received", 0)),
            "alcoholism": int(request.form.get("alcoholism", 0)),
            "is_weekend": int(request.form.get("is_weekend", 0)),
            "sched_hour": int(request.form.get("sched_hour", 0)),
            "diabetes": int(request.form.get("diabetes", 0))
        }

        # Cria DataFrame com as colunas esperadas
        X = pd.DataFrame([dados])

        # Faz a previsão
        if hasattr(modelo, "predict_proba"):
            prob = modelo.predict_proba(X)[0][1] * 100
        else:
            prob = modelo.predict(X)[0] * 100

        # Define texto interpretativo
        interpretacao = "Alta chance de comparecimento" if prob > 70 else "Risco de falta"

        # Renderiza o resultado no HTML
        return render_template("predict_result.html",
                               prob=f"{prob:.2f}%",
                               interpretacao=interpretacao)

    except Exception as e:
        flash_err(f"Erro ao gerar previsão: {e}")
        return redirect(url_for("predict_view"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)