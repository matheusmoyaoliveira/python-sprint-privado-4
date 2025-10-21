from flask import Flask, jsonify, request
import banco

app = Flask(__name__)

@app.route("/")
def home():
    return "Olá, Flask!"

@app.route("/pacientes", methods=["GET"])
def listar_pacientes():
    """Retorna todos os pacientes cadastrados no Oracle."""
    try:
        dados = banco.listar_pacientes()
        return jsonify(dados)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    
@app.route("/consultas", methods=["GET"])
def listar_consultas():
    """Retorna todas as consultas cadastradas no Oracle."""
    try:
        dados = banco.listar_consultas()
        return jsonify(dados)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    
@app.route("/exames", methods=["GET"])
def listar_exames():
    """Retorna todos os exames cadastrados no Oracle."""
    try:
        dados = banco.listar_exames()
        return jsonify(dados)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    
@app.route("/pacientes/<cpf>", methods=["GET"])
def buscar_paciente(cpf):
    """Busca um paciente específico pelo CPF."""
    try:
        paciente = banco.buscar_paciente_por_cpf(cpf)
        if paciente:
            return jsonify(paciente)
        else:
            return jsonify({"erro": "Paciente não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    
@app.route("/exportar", methods=["POST"])
def gerar_exportacao():
    """Gera o arquivo JSON completo com todos os dados."""
    try:
        nome = request.args.get("arquivo", "relatorio_api.json")
        banco.exportar_dados_json(nome)
        return jsonify({
            "mensagem": f"Arquivo '{nome}' exportado com sucesso!",
            "status": "sucesso"
        })
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    
@app.route("/pacientes/<cpf>", methods=["PUT"])
def atualizar_paciente(cpf):
    """Atualiza um paciente existente com novos dados."""
    try:
        novos = request.json
        ok = banco.atualizar_paciente(cpf, novos)
        if ok == 1:
            return jsonify({"mensagem": "Paciente atualizado com sucesso!"})
        else:
            return jsonify({"erro": "CPF não encontrado ou nenhum dado enviado"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    
@app.route("/pacientes/<cpf>", methods=["DELETE"])
def excluir_paciente(cpf):
    """Exclui um paciente do banco pelo CPF."""
    try:
        ok = banco.excluir_paciente(cpf)
        if ok == 1:
            return jsonify({"mensagem": f"Paciente {cpf} excluído com sucesso!"})
        elif ok == -1:
            return jsonify({"erro": "Violação de integridade (chave estrangeira)"}), 409
        else:
            return jsonify({"erro": "Paciente não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)