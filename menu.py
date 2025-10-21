import os
import banco
from datetime import datetime

pacientes = []
consultas = []
exames = []
ESPECIALIDADES = (
    "Cardiologia",
    "Neurologia",
    "Ortopedia",
    "Pediatria",
)

def validar_cpf(cpf: str) -> bool:
    return cpf.isdigit() and len(cpf) == 11

def validar_data(data_str: str) -> bool:
    try:
        datetime.strptime(data_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False
    
def validar_idade(valor: str) -> bool:
    return valor.isdigit() and 0 < int(valor) < 120

def validar_telefone(tel: str) -> bool:
    return tel.isdigit() and len(tel) >= 8

def validar_especialidade(nome: str) -> bool:
    return nome.strip().lower() in (e.lower() for e in ESPECIALIDADES)

def filtrar_consultas_por_cpf(consultas: list[dict], cpf: str) -> list[dict]:
    return [c for c in consultas if c['cpf'] == cpf]

def encontrar_indices_consultas_por_cpf(consultas: list[dict], cpf: str) -> list[int]:
    return [i for i, c in enumerate(consultas) if c['cpf'] == cpf]

def atualizar_consulta_por_indice(consultas: list[dict], idx: int, novos: dict) -> tuple[bool, str]:
    if idx < 0 or idx >= len(consultas): 
        return False, 'Consulta não encontrada'
    atual = consultas[idx]
    if 'data' in novos and novos['data'].strip():
        if not validar_data(novos['data']):
            return False, 'Data inválida.'
        atual['data'] = novos['data'].strip()
    if 'especialidade' in novos and novos['especialidade'].strip():
        if not validar_especialidade(novos['especialidade']):
            return False, 'Especialidade inválida'
        atual['especialidade'] = novos['especialidade'].strip()
    return True, 'Consulta atualizada'

def excluir_consulta_por_indice(consultas: list[dict], idx: int) -> tuple[bool, str]:
    if idx < 0 or idx >= len(consultas):
        return False, 'Consulta não encontrada'
    consultas.pop(idx)
    return True, 'Consulta excluída'

def fluxo_cadastrar_consulta():
    exibir_subtitulo('Agendar Consulta')
    cpf = input('CPF (somente números): ').strip()
    data = input('Data (dd/mm/aaaa): ').strip()
    esp = input(f"Especialidade ({', '.join(ESPECIALIDADES)}): ").strip()
    try:
        dados = {
            "cpf": input("CPF: ").strip(),
            "data": input("Data (dd/mm/aaaa): ").strip(),
            "especialidade": input(f"Especialidade ({', '.join(ESPECIALIDADES)}): ").strip()
        }
        banco.inserir_consulta(dados)
    finally:
        voltar_menu_principal()

def fluxo_listar_consultas_todas():
    exibir_subtitulo('Consultas - Todas')
    consultas = banco.listar_consultas()
    if not consultas:
        print('Nenhuma consulta cadastrada.')
    else:
        for c in consultas:
            print(f"ID: {c['id']} | CPF: {c['cpf']} | Data: {c['data_consulta']} | Esp: {c['especialidade']}")
    voltar_menu_principal()

def fluxo_listar_consultas_por_cpf():
    exibir_subtitulo('Consultas - Por CPF')
    cpf = input('CPF (somente números): ').strip()
    try:
        if not validar_cpf(cpf):
            raise Exception('CPF inválido.')
        
        consultas = banco.buscar_consultas_por_cpf(cpf)
        if not consultas:
            print('Nenhuma consulta para este CPF.')
        else:
            for c in consultas:
                print(f"ID: {c['id']} | Data: {c['data_consulta']} | Esp: {c['especialidade']}")
    except Exception as e:
        print(e)
    finally:
        voltar_menu_principal()

def fluxo_atualizar_consulta_por_cpf_e_indice():
    exibir_subtitulo('Atualizar Consulta')
    cpf = input('CPF (somente números): ').strip()
    try:
        if not validar_cpf(cpf):
            raise Exception('CPF inválido.')
        idxs = encontrar_indices_consultas_por_cpf(consultas, cpf)
        if not idxs:
            raise Exception('Nenhuma consulta encontrada para este CPF.')
        for j, ir in enumerate(idxs):
            c = consultas[ir]; print(f"({j}) Data: {c['data']} Esp: {c['especialidade']}")
        try:
            j = int(input('Escolha o número para atualizar: '))
            ir = idxs[j]
        except (ValueError, IndexError):
            print("Número inválido.")
            return
        atual = consultas[ir]
        nova_data = input(f"Nova data [{atual['data']}] (vazio mantém): ").strip()
        nova_esp = input(f"Nova especialidade [{atual['especialidade']}] (vazio mantém): ").strip()
        novos = {}
        if nova_data:
            novos['data'] = nova_data
        if nova_esp:
            novos['especialidade'] = nova_esp
        ok, msg = atualizar_consulta_por_indice(consultas, ir, novos)
        print(msg)
    except Exception as e:
        print(e)
    finally:
        voltar_menu_principal()

def fluxo_excluir_consulta_por_cpf_e_indice():
    exibir_subtitulo('Excluir Consulta')
    cpf = input('CPF (somente números): ').strip()
    try:
        if not validar_cpf(cpf):
            raise Exception('CPF inválido.')
        
        consultas = banco.excluir_consulta()
        if not consultas:
            print('Nenhuma consulta para este CPF.')
            return
        
        for c in consultas:
            print(f"ID: {c['id']} | Data: {c['data_consulta']} | Esp: {c['especialidade']}")

        id_consulta = int(input("Digite o ID da consulta que deseja excluir: "))

        confirma = input("Confirmar exclusão desta consulta? (S/N): ").strip().upper()
        if confirma != "S":
            print("Operação cancelada.")
            return

        qt = banco.excluir_consulta(id_consulta)
        if qt == 1:
            print("✅ Consulta excluída com sucesso.")
        else:
            print("❌ Consulta não encontrada.")
    except Exception as e:
        print("Erro: ", e)
    finally:
        voltar_menu_principal()

def submenu_consultas():
    while True:
        exibir_subtitulo('CONSULTAS (CRUD)')
        print('''
1 - Agendar
2 - Listar todas
3 - Listar por CPF
4 - Atualizar por índice (de um CPF)
5 - Excluir por índice (de um CPF)
6 - Voltar              
              ''')
        
        try:
            op = int(input('\nOpção: '))
        except ValueError:
            print('Digite um número válido.') 
            voltar_menu_principal() 
            continue
        match op:
            case 1:
                fluxo_cadastrar_consulta()
            case 2:
                fluxo_listar_consultas_todas()
            case 3:
                fluxo_listar_consultas_por_cpf()
            case 4:
                fluxo_atualizar_consulta_por_cpf_e_indice()
            case 5:
                fluxo_excluir_consulta_por_cpf_e_indice()
            case 6:
                break
            case _:
                print('Opção inválida.')
                voltar_menu_principal()

def cadastrar_novo_paciente():
    exibir_subtitulo('Cadastro do Paciente:')
    nome = input('Nome do paciente: ')
    cpf = input('CPF (somente números): ')
    idade = input('Idade: ')
    telefone = input('Telefone: ')
    endereco = input('Endereço: ')
    cartao_sus = input('Cartão SUS (Opcional): \n')

    try:
        if not validar_cpf(cpf): raise Exception("CPF inválido...")
        if not validar_idade(idade): raise Exception("Idade inválida...")
        if not validar_telefone(telefone): raise Exception("Telefone inválido...")
        for p in pacientes:
            if p['cpf'] == cpf:
                raise Exception(f"Paciente com o CPF {cpf} já cadastrado")
            
        dados_paciente = {
            'nome': nome,
            'cpf': cpf,
            'idade': idade,
            'telefone': telefone,
            'endereco': endereco,
            'cartao_sus': cartao_sus
        }
        
    except Exception as e:
        print(e)
    else:
        banco.inserir_paciente(dados_paciente)
        print(f"O paciente {nome} foi cadastrado com sucesso!\n")
        exibir_pacientes()
    finally:
        voltar_menu_principal()

def submenu_pacientes():
    while True:
        exibir_subtitulo('PACIENTES (CRUD)')
        print('''
1 - Cadastrar
2 - Listar todos
3 - Buscar por CPF
4 - Atualizar por CPF
5 - Excluir por CPF
6 - Voltar''')
        
        try:
            op = int(input("\nOpção: "))
        except ValueError:
            print("Digite um número válido.")
            voltar_menu_principal()
            continue

        match op:
            case 1:
                cadastrar_novo_paciente()
            case 2:
                exibir_pacientes()
                voltar_menu_principal()
            case 3:
                fluxo_buscar_paciente_por_cpf()
            case 4:
                fluxo_atualizar_paciente()
            case 5:
                fluxo_excluir_paciente()
            case 6:
                break
            case _:
                print("Opção inválida.")
                voltar_menu_principal()

def encontrar_indice_por_cpf(pacientes, cpf: str) -> int:
    for i, p in enumerate(pacientes):
        if p['cpf'] == cpf:
            return i
    return -1

def obter_paciente_por_cpf(pacientes, cpf: str):
    idx = encontrar_indice_por_cpf(pacientes, cpf)
    return pacientes[idx] if idx != -1 else None

def atualizar_paciente_por_indice(pacientes, idx: int, novos: dict) -> tuple[bool, str]:
    try:
        if idx < 0 or idx >= len(pacientes):
            return False, "Paciente não encontrado"
        atual = pacientes[idx]

        if "nome" in novos and novos["nome"].strip():
            atual["nome"] = novos["nome"].strip()

        if "idade" in novos and novos["idade"].strip():
            if not validar_idade(novos["idade"]): 
                return False, "Idade inválida."
            atual["idade"] = novos["idade"]

        if "telefone" in novos and novos["telefone"].strip():
            if not validar_telefone(novos["telefone"]):
                return False, "Telefone inválido"
            atual["telefone"] = novos["telefone"]

        if "endereco" in novos and novos["endereco"].strip():
            atual["endereco"] = novos["endereco"]

        if "cartao_sus" in novos:
            atual["cartao_sus"] = novos["cartao_sus"]

        return True, "Paciente atualizado"
    except Exception as e:
        return False, f"Erro ao atualizar: {e}"
    
def excluir_paciente_por_indice(pacientes, idx: int) -> tuple[bool, str]:
    try:
        if idx < 0 or idx >= len(pacientes):
            return False, "Paciente não encontrado."
        pacientes.pop(idx)
        return True, "Paciente excluído."
    except Exception as e:
        return False, f"Erro ao excluir: {e}"
    
def fluxo_buscar_paciente_por_cpf():
    exibir_subtitulo("Buscar Paciente por CPF")
    cpf = input("CPF (somente números): ").strip()
    try:
        if not validar_cpf(cpf):
            raise Exception("CPF inválido.")
        p = banco.buscar_paciente_por_cpf(cpf)
        if not p:
            print("Paciente não encontrado.")
        else:
            print("\nPaciente encontrado:\n")
            print(f"Nome: {p['nome']}")
            print(f"CPF: {p['cpf']}")
            print(f"Idade: {p['idade']}")
            print(f"Telefone: {p['telefone']}")
            print(f"Endereço: {p['endereco']}")
            print(f"Cartão SUS: {p['cartao_sus'] or 'Não informado'}")
    except Exception as e:
        print(e)
    finally:
        voltar_menu_principal()

def fluxo_atualizar_paciente():
    exibir_subtitulo("Atualizar Paciente")
    cpf = input("CPF (somente números): ").strip()
    try:
        if not validar_cpf(cpf):
            raise Exception("CPF inválido.")
        
        p = banco.buscar_paciente_por_cpf(cpf)
        if not p:
            raise Exception("Paciente não encontrado.")
        
        print("\nDeixe em branco para manter o valor atual.")
        nome = input(f"Nome [{p['nome']}]: ")
        idade = input(f"Idade [{p['idade']}]: ")
        telefone = input(f"Telefone [{p['telefone']}]: ")
        endereco = input(f"Endereço [{p['endereco']}]: ")
        cartao = input(f"Cartão [{p['cartao_sus'] or 'Não informado'}]: ")

        novos = {
            'nome': nome,
            'idade': idade,
            'telefone': telefone,
            'endereco': endereco,
            'cartao_sus': cartao,
        }

        qt = banco.atualizar_paciente(cpf, novos)

        if qt == 1:
            print("✅ Paciente atualizado com sucesso!")
        else:
            print("⚠ Nenhum dado alterado ou CPF não encontrado.")
    except Exception as e:
        print("Erro: ", e)
    finally:
        voltar_menu_principal()

def fluxo_excluir_paciente():
    exibir_subtitulo("Excluir Paciente")
    cpf = input("CPF (somente números): ").strip()
    try:
        if not validar_cpf(cpf):
            raise Exception("CPF inválido")
        
        confirma = input("Confirmar exclusão? (S/N): ").strip().upper()
        if confirma != "S":
            print("Operação cancelada.")
            return
        
        qt = banco.excluir_paciente(cpf)

        if qt == 1:
            print("✅ Paciente excluído com sucesso.")
        elif qt == -1:
            print("⚠ Não é possível excluir: existem consultas/exames vinculados.")
        else:
            print("❌ Paciente não encontrado.")
    except Exception as e:
        print("Erro: ", e)
    finally:
        voltar_menu_principal()

def imprimir_paciente(p):
    print(f"Nome: {p['nome']}")
    print(f"CPF: {p['cpf']}")
    print(f"Idade: {p['idade']}")
    print(f"Telefone: {p['telefone']}")
    print(f"Endereço: {p['endereco']}")
    print(f"Cartão SUS: {p['cartao_sus'] or 'Não informado'}")

def criar_consulta(consultas: list[dict], pacientes: list[dict], dados: dict) -> tuple[bool, str]:
    cpf = dados.get('cpf', '').strip()
    data = dados.get('data', '').strip()
    esp = dados.get('especialidade', '').strip()
    if not validar_cpf(cpf):
        return False, 'CPF inválido.'
    if not any(p['cpf'] == cpf for p in pacientes):
        return False, 'Paciente não cadastrado.' 
    if not validar_data(data):
        return False, 'Data inválida. Use dd/mm/aaaa.'
    if not validar_especialidade(esp):
        return False, 'Especialidade inválida.'
    consultas.append({'cpf': cpf, 'data': data, 'especialidade': esp})
    return True, 'Consulta criada'

def filtrar_exames_por_cpf(exames: list[dict], cpf: str) -> list[dict]:
    return [e for e in exames if e['cpf'] == cpf]

def criar_exame(exames: list[dict], pacientes: list[dict], dados: dict) -> tuple[bool, str]:
    cpf = dados.get('cpf', '').strip()
    tipo = dados.get('tipo', '').strip()
    data = dados.get('data', '').strip()
    resultado = dados.get('resultado', '').strip()
    if not validar_cpf(cpf): return False, 'CPF inválido.'
    if not any(p['cpf'] == cpf for p in pacientes): return False, 'Paciente não cadastrado.'
    if not tipo or not resultado: return False, 'Preencha todos os campos.'
    if not validar_data(data): return False, 'Data inválida. Use dd/mm/aaaa.'
    exames.append({'cpf': cpf, 'tipo': tipo, 'data': data, 'resultado': resultado})
    return True, 'Exame cadastrado.'

def atualizar_exame_por_indice(exames: list[dict], idx: int, novos: dict) -> tuple[bool, str]:
    if idx < 0 or idx >= len(exames): return False, 'Exame não encontrado.'
    atual = exames[idx]
    if 'tipo' in novos and novos['tipo'].strip():
        atual['tipo'] = novos['tipo'].strip()
    if 'data' in novos and novos['data'].strip():
        if not validar_data(novos['data']): return False, 'Data inválida.'
        atual['data'] = novos['data'].strip()
    if 'resultado' in novos and novos['resultado'].strip():
        atual['resultado'] = novos['resultado'].strip()
    return True, 'Exame atualizado.'

def excluir_exame_por_indice(exames: list[dict], idx: int) -> tuple[bool, str]:
    if idx < 0 or idx >= len(exames): return False, 'Exame não encontrado.'
    exames.pop(idx)
    return True, 'Exame excluído.'

def fluxo_cadastrar_exame():
    exibir_subtitulo('Cadastrar Exame')
    cpf = input('CPF (somente números): ').strip()
    tipo = input('Tipo do exame: ').strip()
    data = input('Data do exame (dd/mm/aaaa): ').strip()
    resultado = input('Resultado do exame: ').strip()
    try:
        ok, msg = criar_exame(exames, pacientes, {
            'cpf': cpf, 'tipo': tipo, 'data': data, 'resultado': resultado
        })
        print(msg)
    finally:
        voltar_menu_principal()

def fluxo_listar_exames_todos():
    exibir_subtitulo('Exames — Todos')
    exames = banco.listar_exames()
    if not exames:
        print('Nenhum exame cadastrado.')
    else:
        for e in exames:
            print(f"ID: {e['id']} | CPF: {e['cpf']} | Tipo: {e['tipo']} | Data: {e['data_exame']} | Resultado: {e['resultado']}")
    voltar_menu_principal()

def fluxo_listar_exames_por_cpf():
    exibir_subtitulo('Exames — Por CPF')
    cpf = input('CPF (somente números): ').strip()
    try:
        if not validar_cpf(cpf): raise Exception('CPF inválido.')
        lista = filtrar_exames_por_cpf(exames, cpf)
        if not lista:
            print('Nenhum exame para este CPF.')
        else:
            for i, e in enumerate(lista):
                print(f"[{i}] Tipo: {e['tipo']}  Data: {e['data']}  Resultado: {e['resultado']}")
    except Exception as e:
        print(e)
    finally:
        voltar_menu_principal()

def fluxo_atualizar_exame_por_cpf_e_indice():
    exibir_subtitulo('Atualizar Exame')
    cpf = input('CPF (somente números): ').strip()
    try:
        if not validar_cpf(cpf): raise Exception('CPF inválido.')
        idxs = [i for i, e in enumerate(exames) if e['cpf'] == cpf]
        if not idxs: raise Exception('Nenhum exame para este CPF.')
        for j, ir in enumerate(idxs):
            e = exames[ir]
            print(f"({j}) Tipo: {e['tipo']}  Data: {e['data']}  Resultado: {e['resultado']}")
        try:
            j = int(input('Escolha o número para atualizar: '))
            ir = idxs[j]
        except (ValueError, IndexError):
            print("Número inválido")
            return
        atual = exames[ir]
        novo_tipo = input(f"Novo tipo [{atual['tipo']}] (vazio mantém): ").strip()
        nova_data = input(f"Nova data [{atual['data']}] (vazio mantém): ").strip()
        novo_res  = input(f"Novo resultado [{atual['resultado']}] (vazio mantém): ").strip()
        novos = {}
        if novo_tipo: novos['tipo'] = novo_tipo
        if nova_data: novos['data'] = nova_data
        if novo_res:  novos['resultado'] = novo_res
        ok, msg = atualizar_exame_por_indice(exames, ir, novos)
        print(msg)
    except Exception as e:
        print(e)
    finally:
        voltar_menu_principal()

def fluxo_excluir_exame_por_cpf_e_indice():
    exibir_subtitulo('Excluir Exame')
    cpf = input('CPF (somente números): ').strip()
    try:
        if not validar_cpf(cpf): raise Exception('CPF inválido.')
        idxs = [i for i, e in enumerate(exames) if e['cpf'] == cpf]
        if not idxs: raise Exception('Nenhum exame para este CPF.')
        for j, ir in enumerate(idxs):
            e = exames[ir]
            print(f"({j}) Tipo: {e['tipo']}  Data: {e['data']}  Resultado: {e['resultado']}")
        try:
            j = int(input('Escolha o número para excluir: '))
            ir = idxs[j]
        except (ValueError, IndexError):
            print("Número inválido.")
            return
        conf = input('Confirmar exclusão? (S/N): ').strip().upper()
        if conf != 'S':
            print('Cancelado.')
        else:
            ok, msg = excluir_exame_por_indice(exames, ir)
            print(msg)
    except Exception as e:
        print(e)
    finally:
        voltar_menu_principal()

def fluxo_exportar_json():
    exibir_subtitulo("Exportar relatórios em JSON")
    try:
        nome = input("Nome do arquivo (pressione Enter para padrão): ").strip()
        if nome == "":
            nome = "relatorio_completo.json"
        banco.exportar_dados_json(nome)
    except Exception as e:
        print("Erro ao exportar:", e)
    finally:
        voltar_menu_principal()

def submenu_exames():
    while True:
        exibir_subtitulo('EXAMES (CRUD)')
        print('''1 - Cadastrar (criar)
2 - Listar todos
3 - Listar por CPF
4 - Atualizar por índice (de um CPF)
5 - Excluir por índice (de um CPF)
6 - Voltar''')
        try:
            op = int(input('\nOpção: '))
        except ValueError:
            print('Digite um número válido.')
            voltar_menu_principal()
            continue
        match op:
            case 1: fluxo_cadastrar_exame()
            case 2: fluxo_listar_exames_todos()
            case 3: fluxo_listar_exames_por_cpf()
            case 4: fluxo_atualizar_exame_por_cpf_e_indice()
            case 5: fluxo_excluir_exame_por_cpf_e_indice()
            case 6: break
            case _: print('Opção inválida.'); voltar_menu_principal()

def submenu_relatorios():
    while True:
        exibir_subtitulo('RELATÓRIOS')
        print('''
1 - Consultas por especialidade
2 - Exames por tipo
3 - Idade média dos pacientes
4 - Resumo por CPF
5 - Exportar relatórios em JSON
6 - Voltar''')
        try:
            op = int(input('\nOpção: '))
        except ValueError:
            print('Digite um número válido.')
            voltar_menu_principal()
            continue

        match op:
            case 1: relatorio_consultas_por_especialidade()
            case 2: relatorio_exame_por_tipo()
            case 3: relatorio_idade_media()
            case 4: relatorio_resumo_por_cpf()
            case 5: pass
            case 6: break
            case _: 
                print('Opção inválida.')
                voltar_menu_principal()
        
def informacoes_unidade():
    exibir_subtitulo('Informações da Unidade:')

    exibir_dados_hospital()
    print("Horário de funcionamento: 24 horas, todos os dias")
    print("Especialidades disponíveis:", ", ".join(ESPECIALIDADES))

    voltar_menu_principal()

def exibir_dados_hospital():
    print('Hospital das Clínicas')
    print("Av. Dr. Enéas de Carvalho Aguiar, 255...")
    print("(11) 2661-0000")

def exibir_pacientes():
    pacientes = banco.listar_pacientes()
    if len(pacientes) == 0:
        print('Nenhum paciente cadastrado ainda.')
    else:
        print('Lista de pacientes cadastrados:\n')

        for i, cont in enumerate(pacientes):
            print(f'Paciente {i + 1}:')
            print(f"  Nome: {cont['nome']}")
            print(f"  CPF: {cont['cpf']}")
            print(f"  Idade: {cont['idade']}")
            print(f"  Telefone: {cont['telefone']}")
            print(f"  Endereço: {cont['endereco']}")
            if cont['cartao_sus'] == "":
                print('  Cartão SUS: Não informado')
            else:
                print(f"  Cartão SUS: {cont['cartao_sus']}")

def relatorio_consultas_por_especialidade():
    """Contagem de consultas por especialidade (usa nomes canônicos do catálogo)."""
    exibir_subtitulo('Relatório: Consultas por Especialidade')
    if not consultas:
        print('Sem consultas registradas')
    else:
        cont = {}
        for c in consultas:
            esp = c.get('especialidade', '(sem)')
            cont[esp] = cont.get(esp, 0) + 1

        for esp in ESPECIALIDADES:
            print(f'{esp}: {cont.get(esp, 0)}')

        outros = {k: v for k, v in cont.items() if k not in ESPECIALIDADES}
        for esp, qtd in sorted(outros.items()):
            print(f'{esp}: {qtd}')
    voltar_menu_principal()

def relatorio_exame_por_tipo():
    """Contagem de exames agrupados pelo 'tipo'."""
    exibir_subtitulo('Relatório: Exames por Tipo')
    if not exames:
        print('Sem exames registrados.')
    else:
        cont = {}
        for e in exames:
            tipo = e.get('tipo', '(sem tipo)').strip() or '(sem tipo)'
            cont[tipo] = cont.get(tipo, 0) + 1
        for tipo, qtd in sorted(cont.items()):
            print(f'{tipo}: {qtd}')
    voltar_menu_principal()

def relatorio_idade_media():
    """Estatísticas simples de idade (média/min/max)."""
    exibir_subtitulo('Relatório: Idade média dos pacientes')
    idades = [int(p['idade']) for p in pacientes if str(p.get('idade', '')).isdigit()]
    if not idades:
        print('Sem pacientes com idade registrado')
    else:
        media = sum(idades) / len(idades)
        print(f'Pacientes: {len(idades)}')
        print(f'Idade média: {media:.1f}')
        print(f'Mínima: {min(idades)} | Máxima: {max(idades)}')
    voltar_menu_principal()

def relatorio_resumo_por_cpf():
    """Resumo do paciente (dados cadastrais + total de consultas e exames)"""
    exibir_subtitulo('Relatório: Resumo por CPF')
    cpf = input('CPF (somente números): ').strip()
    try:
        if not validar_cpf(cpf):
            raise Exception('CPF inválido')
        pac = next((p for p in pacientes if p['cpf'] == cpf), None)
        if not pac:
            print('Paciente não cadastrado')
        else:
            try:
                imprimir_paciente(pac)
            except NameError:
                print('\nPaciente:')
                print(f"Nome: {pac['nome']}")
                print(f"CPF: {pac['cpf']}")
                print(f"Idade: {pac['idade']}")
                print(f"Telefone: {pac['telefone']}")
                print(f"Endereço: {pac['endereco']}")
                print(f"Cartão SUS: {pac.get('cartao_sus') or 'Não informado'}")

            cons = [c for c in consultas if c['cpf'] == cpf]
            exs = [e for e in exames if e['cpf'] == cpf]
            print(f'\nTotal de consultas: {len(cons)}')
            print(f'Total de exames: {len(exs)}')
    except Exception as e:
        print(e)
    finally:
        voltar_menu_principal()

def exibir_subtitulo(texto):
    os.system('cls' if os.name == 'nt' else 'clear')
    print()
    print(texto)
    print('-' * len(texto.strip()))
    print()


def voltar_menu_principal():

    input('\nDigite uma tecla para voltar.')
    return


def exibir_nome():
    print('''
Hᴏsᴘɪᴛᴀʟ ᴅᴀs Cʟɪɴɪᴄᴀs
''')

def menu():
    exibir_nome()
    opcao = 0
    while opcao != 6:
        try:
            opcao = int(input('''\nEscolha uma opção:

1 - Pacientes (CRUD)
2 - Consultas (CRUD)
3 - Exames (CRUD)
4 - Relatórios
5 - Informações da unidade
6 - Sair

Opção: '''))
            
            match opcao:
                case 1:
                    submenu_pacientes()
                case 2:
                    submenu_consultas()
                case 3:
                    submenu_exames()
                case 4:
                    submenu_relatorios()
                case 5:
                    informacoes_unidade()
                case 6:
                    print('Saindo do sistema...')
                case _:
                    print('Opção inválida. Tente novamente.')
        except ValueError:
            print('Digite um número válido.')

if __name__ == "__main__":
    menu()