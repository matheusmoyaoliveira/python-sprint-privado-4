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

# ===================== API CONSULTAS =====================
consultas_json = [
    {"id": 1, "dataHora": "2025-11-10 10:00:00", "modalidade": "Presencial", "idPaciente": 1, "idMedico": 2},
    {"id": 2, "dataHora": "2025-11-11 14:30:00", "modalidade": "Online", "idPaciente": 2, "idMedico": 1},
    {"id": 3, "dataHora": "2025-11-12 09:15:00", "modalidade": "Presencial", "idPaciente": 3, "idMedico": 3}
]

@app.route("/api/consultas", methods=["GET"])
def listar_consultas():
    return jsonify(consultas_json)

@app.route("/api/consultas", methods=["POST"])
def adicionar_consulta():
    data = request.get_json()
    nova = {
        "id": len(consultas_json) + 1,
        "dataHora": data.get("dataHora", ""),
        "modalidade": data.get("modalidade", ""),
        "idPaciente": data.get("idPaciente"),
        "idMedico": data.get("idMedico"),
    }
    consultas_json.append(nova)
    return jsonify(nova), 201

@app.route("/api/consultas/<int:id>", methods=["PUT"])
def atualizar_consulta(id):
    data = request.get_json()
    for c in consultas_json:
        if c["id"] == id:
            c["dataHora"] = data.get("dataHora", c["dataHora"])
            c["modalidade"] = data.get("modalidade", c["modalidade"])
            return jsonify(c), 200
    return jsonify({"error": "Consulta não encontrada"}), 404

@app.route("/api/consultas/<int:id>", methods=["DELETE"])
def excluir_consulta(id):
    global consultas_json
    consultas_json = [c for c in consultas_json if c["id"] != id]
    return jsonify({"message": "Consulta removida com sucesso"}), 200


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

# ---------------------------
# PREDICT - API E FRONT-END
# ---------------------------

@app.route("/predict", methods=["POST"])
def prever_comparecimento():
    try:
        # 🔹 ID do modelo no Google Drive
        file_id = "1yC0lIeY-aBSM7BkIn1G64wg83xnHaM0Tk"
        output = "modelo_regressao.joblib"

        # 🔹 Baixa o modelo se ainda não existir
        if not os.path.exists(output):
            gdown.download(f"https://drive.google.com/uc?id={file_id}", output, quiet=False)

        modelo = joblib.load(output)

        # 🔹 Recebe o JSON enviado pelo front
        dados = request.get_json()
        X = pd.DataFrame([dados])

        # 🔹 Faz a previsão
        if hasattr(modelo, "predict_proba"):
            probabilidade = modelo.predict_proba(X)[0][1] * 100
        else:
            probabilidade = modelo.predict(X)[0] * 100

        interpretacao = (
            "Alta chance de comparecimento ✅" if probabilidade > 70 else "Risco de falta ❌"
        )

        return jsonify({
            "mensagem": "Previsão gerada com sucesso!",
            "probabilidade": round(probabilidade, 2),
            "interpretacao": interpretacao
        })

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# 🔹 Página do formulário de previsão
@app.route("/predict/view", methods=["GET"])
def predict_view():
    return render_template("predict.html")


# 🔹 Página de resultado
@app.route("/predict/result", methods=["GET"])
def predict_result():
    prob = request.args.get("prob")
    interpret = request.args.get("interpret")
    return render_template("predict_result.html", prob=f"{prob}%", interpretacao=interpret)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)