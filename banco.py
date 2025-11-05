import oracledb
import json
import os

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
        SELECT ID_PACIENTE, NM_PACIENTE, NR_CPF, NR_RG, NR_ALTURA, NR_PESO,
               DT_NASCIMENTO, DS_ESCOLARIDADE, DS_ESTADO_CIVIL, DS_DESCRICAO
        FROM T_HC_PACIENTE
        ORDER BY ID_PACIENTE
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


def inserir_paciente(paciente):
    """Insere um novo paciente no banco."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO T_HC_PACIENTE
        (ID_PACIENTE, NM_PACIENTE, NR_CPF, NR_RG, NR_ALTURA, NR_PESO,
         DT_NASCIMENTO, DS_ESCOLARIDADE, DS_ESTADO_CIVIL, DS_DESCRICAO)
        VALUES (TO_CHAR(SQ_T_HC_PACIENTE.NEXTVAL), :1, :2, :3, :4, :5, TO_DATE(:6, 'YYYY-MM-DD'), :7, :8, :9)
    """, (
        paciente["nome"],
        paciente["cpf"],
        paciente["rg"],
        paciente["altura"],
        paciente["peso"],
        paciente["dataNascimento"],
        paciente["escolaridade"],
        paciente["estadoCivil"],
        paciente["descricao"]
    ))
    conn.commit()
    cursor.close()
    conn.close()


def atualizar_paciente(id_paciente, dados):
    """Atualiza um paciente existente."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE T_HC_PACIENTE
        SET NM_PACIENTE = :1, NR_CPF = :2, NR_RG = :3, NR_ALTURA = :4,
            NR_PESO = :5, DT_NASCIMENTO = TO_DATE(:6, 'YYYY-MM-DD'),
            DS_ESCOLARIDADE = :7, DS_ESTADO_CIVIL = :8, DS_DESCRICAO = :9
        WHERE ID_PACIENTE = :10
    """, (
        dados["nome"], dados["cpf"], dados["rg"], dados["altura"],
        dados["peso"], dados["dataNascimento"], dados["escolaridade"],
        dados["estadoCivil"], dados["descricao"], id_paciente
    ))
    conn.commit()
    cursor.close()
    conn.close()


def excluir_paciente(id_paciente):
    """Remove um paciente do banco."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM T_HC_PACIENTE WHERE ID_PACIENTE = :1", (id_paciente,))
    conn.commit()
    cursor.close()
    conn.close()

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