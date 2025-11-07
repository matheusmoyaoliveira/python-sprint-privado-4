# NeuroAI - Sprint 4 (Computational Thinking Using Python)

Aplicação Flask para CRUD de pacientes, médicos e consultas, com:
- Exportação JSON;
- Consumo de API externa (ViaCEP);
- Integração com front-end web;
- Deploy no Render.

## Endpoints principais
| Método | Endpoint | Descrição |
|---------|-----------|-----------|
| GET | /consultas | Lista consultas |
| POST | /consultas | Cria nova consulta |
| PUT | /consultas/<id> | Atualiza consulta |
| DELETE | /consultas/<id> | Remove consulta |
| GET | /consultas/exportar | Exporta consultas para JSON |
| GET | /cep/<cep> | Consulta endereço via ViaCEP |

Deploy: [https://neuroai-sprint4.onrender.com](https://neuroai-sprint4.onrender.com)
