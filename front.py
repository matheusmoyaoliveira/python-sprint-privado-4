# ------------------------------------------------------------
# FRONT Flask - Interface Web para API Python (porta 8080)
# ------------------------------------------------------------

from flask import Flask, render_template, request, redirect, url_for, flash
import requests
from requests.exceptions import RequestException

app = Flask(__name__)
app.secret_key = "neuroai-front-secret"

# URL da API Flask (back-end principal)
API_BASE = "http://127.0.0.1:5000"

# ------------------------------------------------------------
# Função auxiliar para chamar a API
# ------------------------------------------------------------
def api_request(method: str, path: str, **kwargs):
    """Chama a API do back (app.py) e retorna (ok, data|msg)"""
    url = f"{API_BASE}{path}"
    try:
        resp = requests.request(method.upper(), url, timeout=8, **kwargs)

        try:
            data = resp.json()
        except ValueError:
            data = resp.text

        if 200 <= resp.status_code < 300:
            return True, data
        else:
            msg = data if isinstance(data, str) else data if data else resp.text
            return False, msg or f"Erro HTTP {resp.status_code}"
    except RequestException as e:
        return False, f"Falha ao contatar API: {e}"

# ------------------------------------------------------------
# Helpers de mensagens
# ------------------------------------------------------------
def flash_ok(msg: str):
    flash(msg, "success")

def flash_err(msg: str):
    flash(msg, "danger")

# ------------------------------------------------------------
# Home
# ------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")

# ------------------------------------------------------------
# PACIENTES front.py
# ------------------------------------------------------------
@app.route("/pacientes", methods=["GET"])
def pacientes_listar():
    ok, data = api_request("GET", "/pacientes")
    if not ok:
        flash_err(f"Erro ao listar pacientes: {data}")
        data = []
    return render_template("pacientes.html", pacientes=data)

@app.route("/pacientes/novo", methods=["POST"])
def pacientes_novo():
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

    ok, data = api_request("POST", "/pacientes", json=payload)
    if ok:
        flash_ok("✅ Paciente adicionado com sucesso!")
    else:
        flash_err(f"❌ Erro ao adicionar paciente: {data}")
    return redirect(url_for("pacientes_listar"))

@app.route("/pacientes/<int:pid>/excluir", methods=["POST"])
def pacientes_excluir(pid):
    ok, data = api_request("DELETE", f"/pacientes/{pid}")
    if ok:
        flash_ok("🗑️ Paciente excluído com sucesso!")
    else:
        flash_err(f"❌ Erro ao excluir paciente: {data}")
    return redirect(url_for("pacientes_listar"))

@app.route("/pacientes/<int:pid>/editar", methods=["POST"])
def pacientes_editar(pid):
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

    ok, data = api_request("PUT", f"/pacientes/{pid}", json=payload)
    if ok:
        flash_ok("✏️ Paciente atualizado com sucesso!")
    else:
        flash_err(f"❌ Erro ao atualizar paciente: {data}")
    return redirect(url_for("pacientes_listar"))

# ------------------------------------------------------------
# MÉDICOS front.py
# ------------------------------------------------------------
@app.route("/medicos", methods=["GET"])
def medicos_listar():
    ok, data = api_request("GET", "/medicos")
    if not ok:
        flash_err(f"Erro ao listar médicos: {data}")
        data = []
    return render_template("medicos.html", medicos=data)

@app.route("/medicos/novo", methods=["POST"])
def medicos_novo():
    payload = {
        "nome": request.form.get("nome", "").strip(),
        "crm": request.form.get("crm", "").strip(),
        "especialidade": request.form.get("especialidade", "").strip(),
        "telefone": request.form.get("telefone", "").strip(),
        "email": request.form.get("email", "").strip()
    }

    ok, data = api_request("POST", "/medicos", json=payload)
    if ok:
        flash_ok("✅ Médico adicionado com sucesso!")
    else:
        flash_err(f"❌ Erro ao adicionar médico: {data}")
    return redirect(url_for("medicos_listar"))

@app.route("/medicos/<int:mid>/excluir", methods=["POST"])
def medicos_excluir(mid):
    ok, data = api_request("DELETE", f"/medicos/{mid}")
    if ok:
        flash_ok("🗑️ Médico excluído com sucesso!")
    else:
        flash_err(f"❌ Erro ao excluir médico: {data}")
    return redirect(url_for("medicos_listar"))

@app.route("/medicos/<int:mid>/editar", methods=["POST"])
def medicos_editar(mid):
    payload = {
        "nome": request.form.get("nome", "").strip(),
        "crm": request.form.get("crm", "").strip(),
        "especialidade": request.form.get("especialidade", "").strip(),
        "telefone": request.form.get("telefone", "").strip(),
        "email": request.form.get("email", "").strip()
    }

    ok, data = api_request("PUT", f"/medicos/{mid}", json=payload)
    if ok:
        flash_ok("✏️ Médico atualizado com sucesso!")
    else:
        flash_err(f"❌ Erro ao atualizar médico: {data}")
    return redirect(url_for("medicos_listar"))

# ------------------------------------------------------------
# CONSULTAS front.py
# ------------------------------------------------------------
@app.route("/consultas", methods=["GET"])
def consultas_listar():
    ok, data = api_request("GET", "/consultas")
    if not ok:
        flash_err(f"Erro ao listar consultas: {data}")
        data = []
    return render_template("consultas.html", consultas=data)

@app.route("/consultas/novo", methods=["POST"])
def consultas_novo():
    payload = {
        "dataHora": request.form.get("dataHora", "").strip(),
        "modalidade": request.form.get("modalidade", "").strip(),
        "idPaciente": request.form.get("idPaciente", type=int, default=2),
        "idMedico": request.form.get("idMedico", type=int, default=1)
    }

    ok, data = api_request("POST", "/consultas", json=payload)
    if ok:
        flash_ok("✅ Consulta agendada com sucesso!")
    else:
        flash_err(f"❌ Erro ao agendar consulta: {data}")
    return redirect(url_for("consultas_listar"))

@app.route("/consultas/<int:cid>/excluir", methods=["POST"])
def consultas_excluir(cid):
    ok, data = api_request("DELETE", f"/consultas/{cid}")
    if ok:
        flash_ok("🗑️ Consulta excluída com sucesso!")
    else:
        flash_err(f"❌ Erro ao excluir consulta: {data}")
    return redirect(url_for("consultas_listar"))


