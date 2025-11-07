import json, os

# ------------------------------------------------------------
# Caminhos dos arquivos JSON simulando as tabelas
# ------------------------------------------------------------
DIR = "data"
if not os.path.exists(DIR):
    os.makedirs(DIR)

ARQ_PACIENTES = os.path.join(DIR, "pacientes.json")
ARQ_MEDICOS = os.path.join(DIR, "medicos.json")
ARQ_CONSULTAS = os.path.join(DIR, "consultas.json")

# ------------------------------------------------------------
# Funções genéricas de leitura/escrita
# ------------------------------------------------------------
def _carregar(caminho):
    if not os.path.exists(caminho):
        return []
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

def _salvar(caminho, dados):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

# ------------------------------------------------------------
# PACIENTES
# ------------------------------------------------------------
def listar_pacientes():
    return _carregar(ARQ_PACIENTES)

def inserir_paciente(dados):
    pacientes = _carregar(ARQ_PACIENTES)
    dados["id"] = len(pacientes) + 1
    pacientes.append(dados)
    _salvar(ARQ_PACIENTES, pacientes)
    return {"mensagem": "Paciente cadastrado com sucesso!"}, 201

def atualizar_paciente(id, novos_dados):
    pacientes = _carregar(ARQ_PACIENTES)
    for p in pacientes:
        if p["id"] == int(id):
            p.update(novos_dados)
            _salvar(ARQ_PACIENTES, pacientes)
            return True, {"mensagem": "Paciente atualizado!"}, 200
    return False, {"erro": "Paciente não encontrado"}, 404

def excluir_paciente(id):
    pacientes = _carregar(ARQ_PACIENTES)
    atualizados = [p for p in pacientes if p["id"] != int(id)]
    if len(atualizados) == len(pacientes):
        return False
    _salvar(ARQ_PACIENTES, atualizados)
    return True

# ------------------------------------------------------------
# MÉDICOS
# ------------------------------------------------------------
def listar_medicos():
    return _carregar(ARQ_MEDICOS)

def buscar_medico_por_id(id):
    medicos = _carregar(ARQ_MEDICOS)
    for m in medicos:
        if m["id"] == int(id):
            return m
    return None

def inserir_medico(dados):
    medicos = _carregar(ARQ_MEDICOS)
    dados["id"] = len(medicos) + 1
    medicos.append(dados)
    _salvar(ARQ_MEDICOS, medicos)
    return {"mensagem": "Médico cadastrado com sucesso!"}, 201

def atualizar_medico(id, novos_dados):
    medicos = _carregar(ARQ_MEDICOS)
    for m in medicos:
        if m["id"] == int(id):
            m.update(novos_dados)
            _salvar(ARQ_MEDICOS, medicos)
            return True, {"mensagem": "Médico atualizado!"}, 200
    return False, {"erro": "Médico não encontrado"}, 404

def remover_medico(id):
    medicos = _carregar(ARQ_MEDICOS)
    novos = [m for m in medicos if m["id"] != int(id)]
    if len(novos) == len(medicos):
        return False
    _salvar(ARQ_MEDICOS, novos)
    return True

# ------------------------------------------------------------
# CONSULTAS
# ------------------------------------------------------------
def listar_consultas():
    return _carregar(ARQ_CONSULTAS)

def inserir_consulta(dados):
    consultas = _carregar(ARQ_CONSULTAS)
    dados["id"] = len(consultas) + 1
    consultas.append(dados)
    _salvar(ARQ_CONSULTAS, consultas)
    return {"mensagem": "Consulta criada com sucesso!"}, 201

def atualizar_consulta(id, novos_dados):
    consultas = _carregar(ARQ_CONSULTAS)
    for c in consultas:
        if c["id"] == int(id):
            c.update(novos_dados)
            _salvar(ARQ_CONSULTAS, consultas)
            return True, {"mensagem": "Consulta atualizada!"}, 200
    return False, {"erro": "Consulta não encontrada"}, 404

def deletar_consulta(id):
    consultas = _carregar(ARQ_CONSULTAS)
    novas = [c for c in consultas if c["id"] != int(id)]
    if len(novas) == len(consultas):
        return False, {"erro": "Consulta não encontrada"}, 404
    _salvar(ARQ_CONSULTAS, novas)
    return True, {"mensagem": "Consulta excluída!"}, 200

# ------------------------------------------------------------
# EXPORTAR (gera resumo consolidado)
# ------------------------------------------------------------
def exportar_dados_json():
    relatorio = {
        "pacientes": _carregar(ARQ_PACIENTES),
        "medicos": _carregar(ARQ_MEDICOS),
        "consultas": _carregar(ARQ_CONSULTAS),
        "total_pacientes": len(_carregar(ARQ_PACIENTES)),
        "total_medicos": len(_carregar(ARQ_MEDICOS)),
        "total_consultas": len(_carregar(ARQ_CONSULTAS))
    }
    caminho = os.path.join(DIR, "exportacao.json")
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(relatorio, f, indent=4, ensure_ascii=False)
    return relatorio
