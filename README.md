# 🧠 NeuroAI - Sistema Hospitalar (Sprint 4 - Computational Thinking Using Python)

## 📘 Descrição do Projeto
O projeto **NeuroAI** é um sistema hospitalar desenvolvido como parte da Sprint 4 da disciplina *Computational Thinking Using Python* (FIAP).  
Ele integra uma **API Flask** com um **banco de dados Oracle** e um **Front-End web em Flask**, oferecendo funcionalidades completas de CRUD para **Pacientes**, **Médicos** e **Consultas**.

O sistema também está preparado para **integração com modelos de Machine Learning**, permitindo previsões e análises clínicas automatizadas.

---

## ⚙️ Tecnologias Utilizadas
- **Python 3.11+**
- **Flask**
- **Flask-CORS**
- **cx_Oracle**
- **HTML5 / CSS3 / Jinja2**
- **Banco de Dados Oracle**
- **Joblib (para integração com Machine Learning)**

---

## 🧩 Estrutura do Sistema

| Componente | Descrição |
|-------------|------------|
| `app.py` | API Flask principal (CRUD + integração com Oracle + ML) |
| `banco.py` | Conexão e operações SQL (SELECT, INSERT, UPDATE, DELETE) |
| `ml_predict.py` | Integração com modelo de Machine Learning (classificação e regressão) |
| `front.py` | Interface web integrada ao back-end |
| `templates/` | Páginas HTML com layout unificado NeuroAI |
| `static/css/style.css` | Estilos visuais responsivos e modernos |
| `static/js/script.js` | Confirmação de exclusões e comportamentos da interface |
| `cria_sprint4.sql` | Script de criação das tabelas e dados iniciais |
| `apaga_sprint4.sql` | Script para limpar todas as tabelas do banco |
| `classificacao.joblib` | Modelo de Machine Learning |
| `integrantes_link.txt` | Nomes dos integrantes e link do vídeo de apresentação |
| `relatorio_api.json` | Exportação dos dados em formato JSON |

---

## 🚀 Funcionalidades
- CRUD completo para **Pacientes**, **Médicos** e **Consultas**
- Integração direta com o **Oracle Database**
- Interface web em Flask com layout unificado
- Consumo e integração com modelo **Machine Learning**
- Exportação automática dos dados para **JSON**
- Confirmação antes de exclusões via JavaScript
- Páginas responsivas com o tema **NeuroAI**

---

## 🧠 Equipe de Desenvolvimento
**FIAP - 1TDSPV**

| Nome | RM |
|------|----|
| Matheus Moya de Oliveira | 562822 |
| Daniel Nicolas Leoterio | 562186 |
| Ana Carolina Pereira Fontes | 562145 |

---

## 🧾 Execução Local
1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure o banco Oracle (execute `cria_sprint4.sql`)
3. Inicie a API:
   ```bash
   python app.py
   ```
4. Em outro terminal, inicie o front-end:
   ```bash
   python front.py
   ```
5. Acesse:
   - **API** → `http://127.0.0.1:5000`
   - **Front-end** → `http://127.0.0.1:8080`

---

## 🧪 Testes Recomendados
- Inserir novos pacientes, médicos e consultas via web
- Confirmar no **Oracle Developer** se os dados foram gravados
- Testar operações de **atualização e exclusão**
- Exportar o relatório (`relatorio_api.json`) e verificar o conteúdo

---

## 🎥 Vídeo Demonstrativo
O vídeo com a explicação do projeto, execução e integração entre as APIs será anexado ao arquivo `integrantes_link.txt`.

---

## 🏁 Conclusão
O projeto **NeuroAI** cumpre todos os requisitos da Sprint 4:
- CRUD completo conectado ao banco Oracle
- Integração com API externa (Machine Learning)
- Interface web funcional e responsiva
- Exportação JSON e relatórios automáticos
- Código limpo, modular e em conformidade com os padrões da FIAP
