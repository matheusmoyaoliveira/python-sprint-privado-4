import oracledb
import json
import os
import re
from datetime import datetime, date

def get_connection():
    return oracledb.connect(
        user=os.getenv("ORACLE_USER", "rm562822"),
        password=os.getenv("ORACLE_PASSWORD", "130997"),
        dsn=os.getenv("ORACLE_DSN", "oracle.fiap.com.br:1521/orcl")
    )


def listar_pacientes():
    """Retorna todos os pacientes cadastrados."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT TRIM(ID_PACIENTE) AS ID_PACIENTE,
           NM_PACIENTE, NR_CPF, NR_RG, NR_ALTURA, NR_PESO,
           TO_CHAR(DT_NASCIMENTO, 'YYYY-MM-DD') AS DT_NASCIMENTO,
           DS_ESCOLARIDADE, DS_ESTADO_CIVIL, DS_DESCRICAO
    FROM T_HC_PACIENTE
    ORDER BY TO_NUMBER(TRIM(ID_PACIENTE))
    """)
    pacientes = [
        {
            "id": row[0],
            "nome": row[1],
            "cpf": row[2],
            "rg": row[3],
            "altura": row[4],
            "peso": row[5],
            "dataNascimento": str(row[6]) if row[6] else None,
            "escolaridade": row[7],
            "estadoCivil": row[8],
            "descricao": row[9]
        }
        for row in cursor.fetchall()
    ]
    cursor.close()
    conn.close()
    return pacientes


def cpf_existe(cpf):
    """Verifica se já existe um paciente com o mesmo CPF."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM T_HC_PACIENTE WHERE TRIM(NR_CPF) = :1", [cpf])
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count > 0



def inserir_paciente(dados):
    """Insere um novo paciente com validações de CPF, nome, altura, peso e data."""
    nome = dados.get("nome", "").strip()
    cpf = dados.get("cpf", "").strip()
    rg = dados.get("rg", "").strip()
    altura = dados.get("altura", 0)
    peso = dados.get("peso", 0)
    data_nasc = dados.get("dataNascimento", "").split(" ")[0]
    escolaridade = dados.get("escolaridade", "").strip()
    estado_civil = dados.get("estadoCivil", "").strip()
    descricao = dados.get("descricao", "").strip()

    
    if not nome or len(nome) < 3:
        return {"erro": "O nome do paciente é obrigatório e deve ter pelo menos 3 caracteres."}, 400
    if not re.match(r"^\d{11}$", cpf):
        return {"erro": "O CPF deve conter exatamente 11 dígitos numéricos."}, 400
    if cpf_existe(cpf):
        return {"erro": "Já existe um paciente cadastrado com este CPF."}, 400
    if float(altura) <= 0 or float(peso) <= 0:
        return {"erro": "Altura e peso devem ser maiores que zero."}, 400
    try:
        data_obj = datetime.strptime(data_nasc, "%Y-%m-%d").date()
        if data_obj > date.today():
            return {"erro": "A data de nascimento não pode ser futura."}, 400
    except:
        return {"erro": "Formato de data inválido. Use YYYY-MM-DD."}, 400

    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO T_HC_PACIENTE
        (ID_PACIENTE, NM_PACIENTE, NR_CPF, NR_RG, NR_ALTURA, NR_PESO,
         DT_NASCIMENTO, DS_ESCOLARIDADE, DS_ESTADO_CIVIL, DS_DESCRICAO)
        VALUES (TO_CHAR(SQ_T_HC_PACIENTE.NEXTVAL), :1, :2, :3, :4, :5,
                TO_DATE(:6, 'YYYY-MM-DD'), :7, :8, :9)
    """, (nome, cpf, rg, altura, peso, data_nasc, escolaridade, estado_civil, descricao))
    conn.commit()
    cursor.close()
    conn.close()
    return {"mensagem": "Paciente cadastrado com sucesso!"}, 201


def atualizar_paciente(id_paciente, dados):
    """Atualiza um paciente com validações e formatação de data."""
    nome = dados.get("nome", "").strip()
    cpf = dados.get("cpf", "").strip()
    rg = dados.get("rg", "").strip()
    altura = dados.get("altura", 0)
    peso = dados.get("peso", 0)
    data_nasc = dados.get("dataNascimento", "").split(" ")[0]
    escolaridade = dados.get("escolaridade", "").strip()
    estado_civil = dados.get("estadoCivil", "").strip()
    descricao = dados.get("descricao", "").strip()

    if not nome or len(nome) < 3:
        return False, {"erro": "Nome inválido."}, 400
    if not re.match(r"^\d{11}$", cpf):
        return False, {"erro": "CPF deve conter 11 dígitos numéricos."}, 400
    if float(altura) <= 0 or float(peso) <= 0:
        return False, {"erro": "Altura e peso devem ser maiores que zero."}, 400

    try:
        data_obj = datetime.strptime(data_nasc, "%Y-%m-%d").date()
        if data_obj > date.today():
            return False, {"erro": "Data de nascimento inválida (futura)."}, 400
    except:
        return False, {"erro": "Formato de data inválido."}, 400

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM T_HC_PACIENTE WHERE TRIM(ID_PACIENTE) = :1", [str(id_paciente)])
    if cursor.fetchone()[0] == 0:
        cursor.close()
        conn.close()
        return False, {"erro": "Paciente não encontrado."}, 404

    cursor.execute("""
        UPDATE T_HC_PACIENTE
        SET NM_PACIENTE = :1, NR_CPF = :2, NR_RG = :3, NR_ALTURA = :4,
            NR_PESO = :5, DT_NASCIMENTO = TO_DATE(:6, 'YYYY-MM-DD'),
            DS_ESCOLARIDADE = :7, DS_ESTADO_CIVIL = :8, DS_DESCRICAO = :9
        WHERE TRIM(ID_PACIENTE) = :10
    """, (nome, cpf, rg, altura, peso, data_nasc, escolaridade, estado_civil, descricao, str(id_paciente)))

    conn.commit()
    cursor.close()
    conn.close()
    return True, {"mensagem": "Paciente atualizado com sucesso!"}, 200


def excluir_paciente(id_paciente):
    """Remove um paciente pelo ID."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM T_HC_PACIENTE
        WHERE TRIM(ID_PACIENTE) = :1
    """, [str(id_paciente)])

    apagou = (cursor.rowcount > 0)
    conn.commit()
    cursor.close()
    conn.close()
    return apagou


def crm_existe(crm):
    """Verifica se já existe um médico com o CRM informado."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM T_HC_MEDICO WHERE TRIM(NR_CRM) = :1", [crm])
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count > 0


def inserir_medico(dados):
    """Insere um novo médico no banco Oracle, validando nome e CRM."""
    nome = dados.get("nome", "").strip()
    crm = dados.get("crm", "").strip().upper()

    
    if not nome or len(nome) < 3:
        return {"erro": "O nome do médico é obrigatório e deve ter pelo menos 3 caracteres."}, 400

    
    if not re.match(r"^CRM-\d{5}$", crm):
        return {"erro": "O CRM deve seguir o formato CRM-12345."}, 400

    
    if crm_existe(crm):
        return {"erro": "CRM já cadastrado para outro médico."}, 400

    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO T_HC_MEDICO (ID_MEDICO, NM_MEDICO, NR_CRM)
        VALUES (TO_CHAR(SQ_T_HC_MEDICO.NEXTVAL), :1, :2)
    """, (nome, crm))
    conn.commit()
    cursor.close()
    conn.close()
    return {"mensagem": "Médico criado com sucesso!"}, 201


def atualizar_medico(id_medico, dados):
    """Atualiza um médico existente, validando duplicidade e formato."""
    nome = dados.get("nome", "").strip()
    crm = dados.get("crm", "").strip().upper()

    if not nome or len(nome) < 3:
        return False, {"erro": "Nome do médico inválido."}, 400

    if not re.match(r"^CRM-\d{5}$", crm):
        return False, {"erro": "CRM deve seguir o formato CRM-12345."}, 400

    conn = get_connection()
    cursor = conn.cursor()

    
    cursor.execute("SELECT COUNT(*) FROM T_HC_MEDICO WHERE TRIM(ID_MEDICO) = :1", [str(id_medico)])
    if cursor.fetchone()[0] == 0:
        cursor.close()
        conn.close()
        return False, {"erro": "Médico não encontrado."}, 404

    
    cursor.execute("""
        SELECT COUNT(*) FROM T_HC_MEDICO 
        WHERE TRIM(NR_CRM) = :1 AND TRIM(ID_MEDICO) != :2
    """, [crm, str(id_medico)])
    if cursor.fetchone()[0] > 0:
        cursor.close()
        conn.close()
        return False, {"erro": "CRM já utilizado por outro médico."}, 400

    cursor.execute("""
        UPDATE T_HC_MEDICO
           SET NM_MEDICO = :1,
               NR_CRM = :2
         WHERE TRIM(ID_MEDICO) = :3
    """, (nome, crm, str(id_medico)))

    conn.commit()
    cursor.close()
    conn.close()
    return True, {"mensagem": "Médico atualizado com sucesso!"}, 200



def listar_medicos():
    """Retorna todos os médicos cadastrados."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT TRIM(ID_MEDICO), NM_MEDICO, NR_CRM
        FROM T_HC_MEDICO
        ORDER BY TO_NUMBER(TRIM(ID_MEDICO))
    """)

    medicos = []
    for row in cursor.fetchall():
        medicos.append({
            "id": row[0],
            "nome": row[1],
            "crm": row[2]
        })

    cursor.close()
    conn.close()
    return medicos


def buscar_medico_por_id(id_medico):
    """Busca um médico pelo ID."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT TRIM(ID_MEDICO), NM_MEDICO, NR_CRM
        FROM T_HC_MEDICO
        WHERE TRIM(ID_MEDICO) = :1
    """, [str(id_medico)])

    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row:
        return {"id": row[0], "nome": row[1], "crm": row[2]}
    return None


def remover_medico(id_medico):
    """Remove um médico pelo ID."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM T_HC_MEDICO
        WHERE TRIM(ID_MEDICO) = :1
    """, [str(id_medico)])

    apagou = (cursor.rowcount > 0)
    conn.commit()
    cursor.close()
    conn.close()
    return apagou


def inserir_consulta(dados):
    """Insere uma nova consulta com validações de data, paciente e médico."""
    data_hora = dados.get("dataHora", "").split(" ")[0]
    modalidade = dados.get("modalidade", "").strip().capitalize()
    id_paciente = dados.get("idPaciente")
    id_medico = dados.get("idMedico")

    
    if modalidade not in ["Presencial", "Online"]:
        return {"erro": "Modalidade inválida. Use 'Presencial' ou 'Online'."}, 400

    
    try:
        data_obj = datetime.strptime(data_hora, "%Y-%m-%d").date()
        if data_obj < date.today():
            return {"erro": "A data da consulta deve ser futura."}, 400
    except:
        return {"erro": "Formato de data inválido. Use YYYY-MM-DD."}, 400

    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM T_HC_PACIENTE WHERE TRIM(ID_PACIENTE) = :1", [str(id_paciente)])
    if cursor.fetchone()[0] == 0:
        cursor.close()
        conn.close()
        return {"erro": "Paciente não encontrado."}, 404

    cursor.execute("SELECT COUNT(*) FROM T_HC_MEDICO WHERE TRIM(ID_MEDICO) = :1", [str(id_medico)])
    if cursor.fetchone()[0] == 0:
        cursor.close()
        conn.close()
        return {"erro": "Médico não encontrado."}, 404

    
    cursor.execute("""
        INSERT INTO T_HC_CONSULTA (ID_CONSULTA, DT_HR_CONSULTA, DS_MODALIDADE)
        VALUES (TO_CHAR(SQ_T_HC_CONSULTA.NEXTVAL), TO_DATE(:1, 'YYYY-MM-DD'), :2)
    """, (data_hora, modalidade))
    conn.commit()
    cursor.close()
    conn.close()
    return {"mensagem": "Consulta cadastrada com sucesso!"}, 201


def atualizar_consulta(id_consulta, dados):
    """Atualiza uma consulta com validações."""
    data_hora = dados.get("dataHora", "").split(" ")[0]
    modalidade = dados.get("modalidade", "").strip().capitalize()

    if modalidade not in ["Presencial", "Online"]:
        return False, {"erro": "Modalidade inválida. Use 'Presencial' ou 'Online'."}, 400
    try:
        data_obj = datetime.strptime(data_hora, "%Y-%m-%d").date()
        if data_obj < date.today():
            return False, {"erro": "A data da consulta deve ser futura."}, 400
    except:
        return False, {"erro": "Formato de data inválido."}, 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM T_HC_CONSULTA WHERE TRIM(ID_CONSULTA) = :1", [str(id_consulta)])
    if cursor.fetchone()[0] == 0:
        cursor.close()
        conn.close()
        return False, {"erro": "Consulta não encontrada."}, 404

    cursor.execute("""
        UPDATE T_HC_CONSULTA
        SET DT_HR_CONSULTA = TO_DATE(:1, 'YYYY-MM-DD'), DS_MODALIDADE = :2
        WHERE TRIM(ID_CONSULTA) = :3
    """, (data_hora, modalidade, str(id_consulta)))
    conn.commit()
    cursor.close()
    conn.close()
    return True, {"mensagem": "Consulta atualizada com sucesso!"}, 200


def deletar_consulta(id_consulta):
    """Remove uma consulta pelo ID, se existir."""
    conn = get_connection()
    cursor = conn.cursor()

    
    cursor.execute("SELECT COUNT(*) FROM T_HC_CONSULTA WHERE TRIM(ID_CONSULTA) = :1", [str(id_consulta)])
    if cursor.fetchone()[0] == 0:
        cursor.close()
        conn.close()
        return False, {"erro": "Consulta não encontrada."}, 404

    
    cursor.execute("DELETE FROM T_HC_CONSULTA WHERE TRIM(ID_CONSULTA) = :1", [str(id_consulta)])
    conn.commit()
    cursor.close()
    conn.close()
    return True, {"mensagem": "Consulta excluída com sucesso!"}, 204



def exportar_dados_json():
    """Exporta todos os dados de pacientes em JSON (para relatorio_api.json)."""
    pacientes = listar_pacientes()
    relatorio = {
        "total_pacientes": len(pacientes),
        "pacientes": pacientes
    }

    with open("relatorio_api.json", "w", encoding="utf-8") as f:
        json.dump(relatorio, f, indent=4, ensure_ascii=False)

    return relatorio


def inserir_dados_iniciais():
    """Cria registros de exemplo se o banco estiver vazio."""
    conn = get_connection()
    cursor = conn.cursor()

  
    cursor.execute("SELECT COUNT(*) FROM T_HC_PACIENTE")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO T_HC_PACIENTE
            (ID_PACIENTE, NM_PACIENTE, NR_CPF, NR_RG, NR_ALTURA, NR_PESO,
             DT_NASCIMENTO, DS_ESCOLARIDADE, DS_ESTADO_CIVIL, DS_DESCRICAO)
            VALUES (TO_CHAR(SQ_T_HC_PACIENTE.NEXTVAL), 'Maria Oliveira', '12345678900', '456789', 1.65, 60.5,
                    TO_DATE('1990-05-10','YYYY-MM-DD'), 'Superior Completo', 'Solteira', 'Paciente exemplo 1')
        """)
        cursor.execute("""
            INSERT INTO T_HC_PACIENTE
            (ID_PACIENTE, NM_PACIENTE, NR_CPF, NR_RG, NR_ALTURA, NR_PESO,
             DT_NASCIMENTO, DS_ESCOLARIDADE, DS_ESTADO_CIVIL, DS_DESCRICAO)
            VALUES (TO_CHAR(SQ_T_HC_PACIENTE.NEXTVAL), 'Carlos Silva', '98765432100', '123456', 1.80, 85.0,
                    TO_DATE('1985-03-20','YYYY-MM-DD'), 'Ensino Médio', 'Casado', 'Paciente exemplo 2')
        """)


    cursor.execute("SELECT COUNT(*) FROM T_HC_MEDICO")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO T_HC_MEDICO (ID_MEDICO, NM_MEDICO, NR_CRM)
            VALUES (TO_CHAR(SQ_T_HC_MEDICO.NEXTVAL), 'Dr. João Almeida', 'CRM-12345')
        """)
        cursor.execute("""
            INSERT INTO T_HC_MEDICO (ID_MEDICO, NM_MEDICO, NR_CRM)
            VALUES (TO_CHAR(SQ_T_HC_MEDICO.NEXTVAL), 'Dra. Fernanda Costa', 'CRM-67890')
        """)


    cursor.execute("SELECT COUNT(*) FROM T_HC_CONSULTA")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO T_HC_CONSULTA (ID_CONSULTA, DT_HR_CONSULTA, DS_MODALIDADE)
            VALUES (TO_CHAR(SQ_T_HC_CONSULTA.NEXTVAL), TO_DATE('2025-11-10 09:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'Presencial')
        """)
        cursor.execute("""
            INSERT INTO T_HC_CONSULTA (ID_CONSULTA, DT_HR_CONSULTA, DS_MODALIDADE)
            VALUES (TO_CHAR(SQ_T_HC_CONSULTA.NEXTVAL), TO_DATE('2025-11-12 14:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'Online')
        """)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Dados iniciais criados com sucesso (se necessário).")