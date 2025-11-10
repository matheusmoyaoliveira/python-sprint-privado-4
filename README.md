# 🧠 NeuroAI – Sprint 4 (Python)

### 📚 Projeto da disciplina *Computational Thinking Using Python*  
> FIAP – 1TDSPV | Desenvolvido por **Matheus Moya de Oliveira**

---

## 🚀 Descrição do Projeto

A **Sprint 4** teve como objetivo principal a **integração completa entre o back-end em Python (Flask)**, a **interface web (HTML + CSS + JS)** e o **modelo de Machine Learning (Regressão)** para previsão de comparecimento de pacientes em consultas de telemedicina.

O sistema simula um **ambiente hospitalar inteligente** capaz de cadastrar e gerenciar **pacientes**, **médicos** e **consultas**, além de **prever a probabilidade de comparecimento** com base em dados históricos.

O projeto foi totalmente unificado em uma única aplicação web e está hospedado no Render.

---

## 🧩 Estrutura de Arquivos Principais

| Arquivo | Função | Situação |
|----------|---------|----------|
| **`app.py`** | Núcleo da aplicação Flask. Define todas as rotas (`/pacientes`, `/medicos`, `/consultas`, `/predict/view`, `/exportar`) e integra o modelo de Machine Learning. | ✅ Principal |
| **`banco_render.py`** | Responsável pela **persistência local em JSON** (substitui o banco Oracle para o ambiente de deploy no Render). | ✅ Principal |
| **`ml_predict.py`** | Contém a função de **carregamento e execução do modelo de regressão** via Joblib, utilizado para previsão de comparecimento. | ✅ Principal |
| **`front.py`** | Versão anterior do front-end Flask (mantido como legado da Sprint 3, mas não utilizado no deploy atual). | ⚙️ Legado |
| **`banco_oracle.py`** | Script usado apenas para conexão com o banco Oracle durante o desenvolvimento local da Sprint 3. | ⚙️ Legado |

---

## 🧠 Funcionalidades

### 🔹 Módulo Pacientes
- Cadastrar, listar, editar e excluir pacientes.  
- Persistência automática em `pacientes.json`.

### 🔹 Módulo Médicos
- Cadastro de médicos com nome, CRM e especialidade.  
- Interface com select estilizado para escolher a especialidade.  
- Persistência em `medicos.json`.

### 🔹 Módulo Consultas
- Agendamento de consultas com **data e hora separadas**.  
- Edição de consultas com prompts interativos.  
- Visualização em cards.  
- Persistência em `consultas.json`.

### 🔹 Módulo Predict
- Página `/predict/view` para inserir dados de um paciente.  
- Envio dos dados para o modelo de regressão hospedado.  
- Retorno da **probabilidade de comparecimento (%)** direto na página.  
- Campos validados e mapeamento automático de bairros e variáveis numéricas.

---

## 🧮 Modelo de Machine Learning – Estrutura e Entradas

O modelo de regressão utilizado é baseado em dados históricos de agendamentos médicos (dataset público do Kaggle).  
Ele prevê a **probabilidade de um paciente comparecer à consulta** com base em 13 variáveis:

| Variável | Tipo | Descrição |
|-----------|-------|------------|
| `scholarship` | Numérica (0/1) | Indica se o paciente possui bolsa escolar. |
| `neighbourhood` | Numérica (1–8) | Bairro do paciente (mapeado automaticamente no front-end). |
| `gender` | Numérica (0 = F, 1 = M) | Gênero do paciente. |
| `age` | Numérica | Idade do paciente. |
| `appt_dow` | Numérica (0–6) | Dia da semana da consulta. |
| `handcap` | Numérica (0–4) | Grau de deficiência. |
| `waiting_days` | Numérica | Dias de espera entre agendamento e consulta. |
| `hipertension` | Numérica (0/1) | Indica se o paciente tem hipertensão. |
| `sms_received` | Numérica (0/1) | Indica se o paciente recebeu SMS de lembrete. |
| `alcoholism` | Numérica (0/1) | Indica se o paciente tem histórico de alcoolismo. |
| `is_weekend` | Numérica (0/1) | Indica se a consulta ocorre em fim de semana. |
| `sched_hour` | Numérica (0–23) | Hora da consulta. |
| `diabetes` | Numérica (0/1) | Indica se o paciente é diabético. |

O resultado é retornado como:

```json
{
  "probabilidade": 76.34,
  "probabilidade_str": "76.34%",
  "interpretacao": "Alta chance de comparecimento ✅"
}
```

---

## 🧩 Stack Tecnológica

- **Python 3.13**  
- **Flask 3.0**  
- **HTML5 / CSS3 / JavaScript (Fetch API)**  
- **Joblib + Pandas** (Machine Learning)  
- **Render.com** (Deploy da aplicação Flask)  
- **Google Drive (GDown)** – para armazenamento do modelo `.joblib`

---

## ⚙️ Deploy e Execução

### 🔹 Executar Localmente
```bash
python app.py
```

Acesse no navegador:  
`http://127.0.0.1:5000`

---

### 🔹 Executar Online (Render)
O projeto está hospedado e funcionando em produção:  
👉 **[https://python-sprint-privado-4.onrender.com](https://python-sprint-privado-4.onrender.com)**

---

## 📁 Estrutura Geral do Projeto

```
📦 Sprint4_Python
 ┣ 📂 static/
 ┃ ┣ 📂 css/
 ┃ ┃ ┣ paciente.css
 ┃ ┃ ┣ medico.css
 ┃ ┃ ┣ consulta.css
 ┃ ┃ ┗ predict.css
 ┃ ┣ 📂 js/
 ┃ ┃ ┣ paciente.js
 ┃ ┃ ┣ medico.js
 ┃ ┃ ┣ consulta.js
 ┃ ┃ ┗ predict.js
 ┣ 📂 templates/
 ┃ ┣ base.html
 ┃ ┣ pacientes.html
 ┃ ┣ medicos.html
 ┃ ┣ consultas.html
 ┃ ┗ predict.html
 ┣ 📂 data/
 ┃ ┣ pacientes.json
 ┃ ┣ medicos.json
 ┃ ┗ consultas.json
 ┣ 📄 app.py
 ┣ 📄 banco_render.py
 ┣ 📄 ml_predict.py
 ┗ 📄 requirements.txt
```

---

## 🧩 Aprendizados

Durante a Sprint 4 foi possível:
- Consolidar a integração **Flask + HTML/CSS + JS**.  
- Implementar persistência de dados em JSON.  
- Incorporar um **modelo de Machine Learning real** na aplicação.  
- Realizar deploy completo no Render.  
- Garantir a comunicação entre front-end e API em ambiente de produção.

---

## ✨ Autor

**👨‍💻 Matheus Moya de Oliveira**  
📧 [matheustechdev@gmail.com](mailto:matheustechdev@gmail.com)  
🔗 [LinkedIn](https://www.linkedin.com/in/matheusmoya)  
🔗 [GitHub](https://github.com/matheusmoya)

---

> Projeto desenvolvido para fins acadêmicos na disciplina *Computational Thinking Using Python – FIAP 2025*.
