import oracledb
import json

def conectar():
    """
    Abre uma conexão com o OracleDB e habilita chaves estrangeiras.
    Retorna o objeto de conexão.
    """
    conn = oracledb.connect(
        user="rm562822",
        password="130997",
        dsn="oracle.fiap.com.br:1521/orcl"
    )
    return conn

def criar_tabelas():
    """
    Cria as tabelas necessárias para o sistema (idempotente).
    Executar uma vez no início da aplicação.
    """
    conn = conectar()
    cur = conn.cursor()

    try:
        cur.execute("""
            CREATE TABLE pacientes (
                cpf         VARCHAR2(11) PRIMARY KEY,
                nome        VARCHAR2(100) NOT NULL,
                idade       NUMBER(3)     NOT NULL,
                telefone    VARCHAR2(15)  NOT NULL,
                endereco    VARCHAR2(200) NOT NULL,
                cartao_sus  VARCHAR2(20)
            )
        """)
        print("Tabela PACIENTES criada com sucesso.")
    except oracledb.DatabaseError:
        print("Tabela PACIENTES já existe. Pulando criação.")

    try:
        cur.execute("""
            CREATE TABLE consultas (
                id            NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                cpf           VARCHAR2(11) NOT NULL,
                data_consulta VARCHAR2(10) NOT NULL,
                especialidade VARCHAR2(50) NOT NULL,
                CONSTRAINT fk_paciente_consulta FOREIGN KEY (cpf)
                    REFERENCES pacientes(cpf)
            )
        """)
        print("Tabela CONSULTAS criada com sucesso.")
    except oracledb.DatabaseError:
        print("Tabela CONSULTAS já existe. Pulando criação.")

    try:
        cur.execute("""
            CREATE TABLE exames (
                id          NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                cpf         VARCHAR2(11) NOT NULL,
                tipo        VARCHAR2(50) NOT NULL,
                data_exame  VARCHAR2(10) NOT NULL,
                resultado   VARCHAR2(100) NOT NULL,
                CONSTRAINT fk_paciente_exame FOREIGN KEY (cpf)
                    REFERENCES pacientes(cpf)
            )
        """)
        print("Tabela EXAMES criada com sucesso.")
    except oracledb.DatabaseError:
        print("Tabela EXAMES já existe. Pulando criação.")

    conn.commit()
    conn.close()
    conn.autocommit = False

def inserir_paciente(dados):
    """
    Insere um novo paciente no banco de dados.
    Espera um dicionário com as chaves:
    nome, cpf, idade, telefone, endereco, cartao_sus
    """
    conn = conectar()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO pacientes (cpf, nome, idade, telefone, endereco, cartao_sus)
            VALUES (:1, :2, :3, :4, :5, :6)
        """, (
            dados['cpf'],
            dados['nome'],
            int(dados['idade']),
            dados['telefone'],
            dados['endereco'],
            dados.get('cartao_sus', None)
        ))
        conn.commit()
        print(f"✅ Paciente {dados['nome']} inserido com sucesso.")
    except oracledb.IntegrityError:
        print("❌ CPF já cadastrado.")
    except Exception as e:
        print("Erro ao inserir paciente:", e)
    finally:
        conn.close()

def inserir_consulta(dados):
    """
    Insere uma nova consulta no banco.
    Espera um dicionário: {'cpf', 'data', 'especialidade'}
    """
    conn = conectar()
    cur = conn.cursor()
    try:
        cur.execute("SELECT 1 FROM pacientes WHERE cpf = :1", (dados['cpf'],))
        if not cur.fetchone():
            print("❌ Paciente não cadastrado.")
            return 0
        
        cur.execute("""
            INSERT INTO consultas (cpf, data_consulta, especialidade)
            VALUES (:1, :2, :3)
        """, (dados['cpf'], dados['data'], dados['especialidade']))

        conn.commit()
        print("✅ Consulta cadastrada com sucesso.")
        return 1
    except Exception as e:
        print("Erro ao inserir consulta:", e)
        return 0
    finally:
        conn.close()

def listar_pacientes():
    """
    Retorna todos os pacientes cadastrados.
    """
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT cpf, nome, idade, telefone, endereco, cartao_sus 
        FROM pacientes
        ORDER BY nome
    """)
    registros = cur.fetchall()
    conn.close()

    colunas = ["cpf", "nome", "idade", "telefone", "endereco", "cartao_sus"]
    pacientes = [dict(zip(colunas, linha)) for linha in registros]
    return pacientes

def listar_consultas():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, cpf, data_consulta, especialidade
        FROM consultas
        ORDER BY id
    """)
    registros = cur.fetchall()
    conn.close()

    colunas = ["id", "cpf", "data_consulta", "especialidade"]
    return [dict(zip(colunas, r)) for r in registros]

def listar_exames():
    """
    Retorna todos os exames cadastrados no banco Oracle
    como uma lista de dicionários.
    """
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, cpf, tipo, data_exame, resultado
        FROM exames
        ORDER BY id
    """)
    colunas = ["id", "cpf", "tipo", "data_exame", "resultado"]
    registros = [dict(zip(colunas, r)) for r in cur.fetchall()]
    conn.close()
    return registros

def buscar_paciente_por_cpf(cpf):
    conn = conectar()
    cur = conn.cursor()

    try:
        cur.execute("""
        SELECT cpf, nome, idade, telefone, endereco, cartao_sus
        FROM pacientes
        WHERE cpf = :1
    """, (cpf,))
        
        linha = cur.fetchone()

        if not linha:
            return None
    
        colunas = ["cpf", "nome", "idade", "telefone", "endereco", "cartao_sus"]
        return dict(zip(colunas, linha))
    finally:
        conn.close()

def buscar_consultas_por_cpf(cpf):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, cpf, data_consulta, especialidade
        FROM consultas
        WHERE cpf = :1
        ORDER BY id
    """, (cpf,))
    registros = cur.fetchall()
    conn.close()

    colunas = ["id", "cpf", "data_consulta", "especialidade"]
    return [dict(zip(colunas, r)) for r in registros]

def atualizar_paciente(cpf, novos):
    """
    Atualiza campos do paciente identificado por CPF.
    'novos' pode conter qualquer subconjunto de:
      nome, idade, telefone, endereco, cartao_sus
    Retorna:
      1 -> atualizado
      0 -> CPF não encontrado ou nada para atualizar
    """
    campos = []
    params = []

    def add(campo_sql, valor):
        if valor is None:
            return
        if isinstance(valor, str):
            valor = valor.strip()
            if valor == "":
                return
        campos.append(f"{campo_sql} = :{len(params)+1}")
        params.append(valor)

    add("nome", novos.get("nome"))
    idade_val = novos.get("idade")
    if idade_val and str(idade_val).strip() != "":
        add("idade", int(idade_val))
    add("telefone", novos.get("telefone"))
    add("endereco", novos.get("endereco"))
    add("cartao_sus", novos.get("cartao_sus"))

    if not campos:
        return 0
    
    sql = f"UPDATE pacientes SET {', '.join(campos)} WHERE cpf = :{len(params)+1}"
    params.append(cpf)

    conn = conectar()
    cur = conn.cursor()
    try:
        cur.execute(sql, tuple(params))
        linhas = cur.rowcount
        conn.commit()
        return 1 if linhas == 1 else 0
    finally:
        conn.close()

def excluir_paciente(cpf):
    conn = conectar()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM pacientes WHERE cpf = :1", (cpf,))
        linhas = cur.rowcount
        conn.commit()
        return 1 if linhas == 1 else 0
    except oracledb.IntegrityError as e:
        return -1
    finally:
        conn.close()

def excluir_consulta(id_consulta):
    conn = conectar()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM consultas WHERE id = :1", (id_consulta,))
        linhas = cur.rowcount
        conn.commit()
        return 1 if linhas == 1 else 0
    finally:
        conn.close()

def exportar_dados_json(nome_arquivo="dados_exportados.json"):
    """
    Exporta todos os dados das tabelas pacientes, consultas e exames
    para um arquivo JSON.
    """
    conn = conectar()
    cur = conn.cursor()

    cur.execute("SELECT cpf, nome, idade, telefone, endereco, cartao_sus FROM pacientes")
    colunas_pac = ["cpf", "nome", "idade", "telefone", "endereco", "cartao_sus"]
    pacientes = [dict(zip(colunas_pac, r)) for r in cur.fetchall()]

    cur.execute("SELECT id, cpf, data_consulta, especialidade FROM consultas")
    colunas_con = ["id", "cpf", "data_consulta", "especialidade"]
    consultas = [dict(zip(colunas_con, r)) for r in cur.fetchall()]

    cur.execute("SELECT id, cpf, tipo, data_exame, resultado FROM exames")
    colunas_exa = ["id", "cpf", "tipo", "data_exame", "resultado"]
    exames = [dict(zip(colunas_exa, r)) for r in cur.fetchall()]

    conn.close()

    idades = [p["idade"] for p in pacientes if isinstance(p["idade"], int)]
    estatisticas = {
        "total_pacientes": len(pacientes),
        "total_consultas": len(consultas),
        "total_exames": len(exames),
        "media_idade": round(sum(idades) / len(idades), 1) if idades else 0,
        "idade_minima": min(idades) if idades else 0,
        "idade_maxima": max(idades) if idades else 0
    }

    dados = {
        "pacientes": pacientes,
        "consultas": consultas,
        "exames": exames,
        "estatisticas": estatisticas
    }

    with open(nome_arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

    print(f"✅ Dados exportados para {nome_arquivo}")