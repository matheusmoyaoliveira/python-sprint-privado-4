from flask import Flask, render_template, redirect, request, jsonify
import requests

app = Flask(__name__)


API_URL = "http://127.0.0.1:5000"  # alterar para o link do Render quando subir

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/pacientes")
def listar_pacientes():
    resposta = requests.get(f"{API_URL}/pacientes")
    pacientes = resposta.json() if resposta.status_code == 200 else []
    return render_template("pacientes.html", pacientes=pacientes)

@app.route("/pacientes/adicionar", methods=["POST"])
def adicionar_paciente():
    dados = {
        "nome": request.form["nome"],
        "cpf": request.form["cpf"],
        "rg": request.form["rg"],
        "altura": request.form["altura"],
        "peso": request.form["peso"],
        "dataNascimento": request.form["dataNascimento"],
        "escolaridade": request.form["escolaridade"],
        "estadoCivil": request.form["estadoCivil"],
        "descricao": request.form["descricao"]
    }
    requests.post(f"{API_URL}/pacientes", json=dados)
    return redirect("/pacientes")

@app.route("/pacientes/deletar/<id>")
def deletar_paciente(id):
    requests.delete(f"{API_URL}/pacientes/{id}")
    return redirect("/pacientes")


@app.route("/medicos")
def listar_medicos():
    resposta = requests.get(f"{API_URL}/medicos")
    medicos = resposta.json() if resposta.status_code == 200 else []
    return render_template("medicos.html", medicos=medicos)

@app.route("/medicos/adicionar", methods=["POST"])
def adicionar_medico():
    dados = {
        "nome": request.form["nome"],
        "crm": request.form["crm"],
        "especialidade": request.form["especialidade"],
        "email": request.form["email"],
        "telefone": request.form["telefone"]
    }
    requests.post(f"{API_URL}/medicos", json=dados)
    return redirect("/medicos")

@app.route("/medicos/deletar/<id>")
def deletar_medico(id):
    requests.delete(f"{API_URL}/medicos/{id}")
    return redirect("/medicos")


@app.route("/consultas")
def listar_consultas():
    resposta = requests.get(f"{API_URL}/consultas")
    consultas = resposta.json() if resposta.status_code == 200 else []
    return render_template("consultas.html", consultas=consultas)

@app.route("/consultas/adicionar", methods=["POST"])
def adicionar_consulta():
    dados = {
        "dataHora": request.form["dataHora"],
        "modalidade": request.form["modalidade"],
        "idPaciente": request.form["idPaciente"],
        "idMedico": request.form["idMedico"]
    }
    requests.post(f"{API_URL}/consultas", json=dados)
    return redirect("/consultas")

@app.route("/consultas/deletar/<id>")
def deletar_consulta(id):
    requests.delete(f"{API_URL}/consultas/{id}")
    return redirect("/consultas")

if __name__ == "__main__":
    app.run(debug=True, port=8080)
