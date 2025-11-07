import json, os

ARQUIVO_JSON = "consultas_db.json"

def _carregar():
    if not os.path.exists(ARQUIVO_JSON):
        return []
    with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
        return json.load(f)

def _salvar(dados):
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def listar_consultas():
    return _carregar()

def inserir_consulta(dados):
    consultas = _carregar()
    dados["id"] = len(consultas) + 1
    consultas.append(dados)
    _salvar(consultas)
    return {"mensagem": "Consulta cadastrada com sucesso!"}, 201

def atualizar_consulta(id, novos_dados):
    consultas = _carregar()
    for c in consultas:
        if c["id"] == int(id):
            c.update(novos_dados)
            _salvar(consultas)
            return True, {"mensagem": "Consulta atualizada com sucesso!"}, 200
    return False, {"erro": "Consulta não encontrada"}, 404

def deletar_consulta(id):
    consultas = [c for c in _carregar() if c["id"] != int(id)]
    _salvar(consultas)
    return True, {"mensagem": "Consulta excluída com sucesso!"}, 200
