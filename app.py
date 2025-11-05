# ------------------------------------------------------------
# API Flask - Sprint 4 (Python)
# Integrada ao banco Oracle e à API Java
# ------------------------------------------------------------

from flask import Flask, jsonify, request
from flask_cors import CORS
import banco 
import ml_predict 
import os

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
        <p><b>Integrantes:</b> Matheus Moya de Oliveira e equipe</p>
      </body>
    </html>
    """


@app.route("/pacientes", methods=["GET"])
def listar_pacientes():
    try:
        dados = banco.listar_pacientes()
        return jsonify(dados), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@app.route("/pacientes", methods=["POST"])
def criar_paciente():
    try:
        novo = request.get_json()
        banco.inserir_paciente(novo)
        return jsonify({"mensagem": "Paciente cadastrado com sucesso!"}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@app.route("/pacientes/<id>", methods=["PUT"])
def atualizar_paciente(id):
    try:
        dados = request.get_json()
        banco.atualizar_paciente(id, dados)
        return jsonify({"mensagem": "Paciente atualizado com sucesso!"}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@app.route("/pacientes/<id>", methods=["DELETE"])
def excluir_paciente(id):
    try:
        banco.excluir_paciente(id)
        return jsonify({"mensagem": "Paciente excluído com sucesso!"}), 204
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@app.route("/medicos", methods=["GET"])
def listar_medicos():
    try:
        conn = banco.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ID_MEDICO, NM_MEDICO, NR_CRM FROM T_HC_MEDICO ORDER BY ID_MEDICO")
        medicos = [{"id": r[0], "nome": r[1], "crm": r[2]} for r in cursor.fetchall()]
        cursor.close()
        conn.close()
        return jsonify(medicos), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@app.route("/medicos", methods=["POST"])
def criar_medico():
    try:
        dados = request.get_json()
        conn = banco.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO T_HC_MEDICO (ID_MEDICO, NM_MEDICO, NR_CRM)
            VALUES (TO_CHAR(SQ_T_HC_MEDICO.NEXTVAL), :1, :2)
        """, (dados["nome"], dados["crm"]))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensagem": "Médico cadastrado com sucesso!"}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@app.route("/medicos/<id>", methods=["DELETE"])
def excluir_medico(id):
    try:
        conn = banco.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM T_HC_MEDICO WHERE ID_MEDICO = :1", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensagem": "Médico excluído com sucesso!"}), 204
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@app.route("/consultas", methods=["GET"])
def listar_consultas():
    try:
        conn = banco.get_connection()
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
    try:
        dados = request.get_json()
        conn = banco.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO T_HC_CONSULTA (ID_CONSULTA, DT_HR_CONSULTA, DS_MODALIDADE)
            VALUES (TO_CHAR(SQ_T_HC_CONSULTA.NEXTVAL), TO_DATE(:1, 'YYYY-MM-DD HH24:MI:SS'), :2)
        """, (dados["dataHora"], dados["modalidade"]))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensagem": "Consulta cadastrada com sucesso!"}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@app.route("/exportar", methods=["GET"])
def exportar_json():
    try:
        relatorio = banco.exportar_dados_json()
        return jsonify({
            "mensagem": "Relatório gerado com sucesso!",
            "total_pacientes": relatorio["total_pacientes"]
        }), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@app.route("/predict", methods=["POST"])
def predict():
    try:
        dados = request.get_json()
        resultado = ml_predict.prever(dados)
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)