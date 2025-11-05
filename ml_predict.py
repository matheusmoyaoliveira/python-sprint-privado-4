# ------------------------------------------------------------
# Módulo de Machine Learning integrado à API Python
# Faz download automático do modelo do Google Drive se necessário
# Usa o modelo de CLASSIFICAÇÃO da Sprint 4 de IA
# ------------------------------------------------------------

import os
import joblib
import numpy as np

import gdown

MODEL_PATH = os.getenv("MODEL_PATH", "classificacao.joblib")

MODEL_DRIVE_ID = "1mxGi6txwZe0NOuCgQG0jaO2fWWv7KO7p"
MODEL_URL = f"https://drive.google.com/uc?id={MODEL_DRIVE_ID}"

def _baixar_modelo_se_necessario():
    """Baixa o .joblib do Google Drive se não existir localmente."""
    if os.path.exists(MODEL_PATH):
        return

    url = MODEL_URL
    if not url and MODEL_DRIVE_ID:
        url = f"https://drive.google.com/uc?id={MODEL_DRIVE_ID}"

    if not url:
        raise RuntimeError(
            "Modelo não encontrado localmente e nenhuma origem foi configurada. "
            "Defina MODEL_DRIVE_ID (ID do arquivo no Drive) ou MODEL_URL (link direto)."
        )

    print("📥 Baixando modelo de Machine Learning do Google Drive...")
    gdown.download(url, MODEL_PATH, quiet=False)

_baixar_modelo_se_necessario()
modelo = joblib.load(MODEL_PATH)


def prever(dados):
    """
    Recebe um dicionário JSON com as features do paciente e retorna
    a probabilidade de falta e a classificação.
    Esperado (ajuste para as features do seu training set):
    {
        "idade": 45,
        "faltas_anteriores": 3,
        "consultas_anteriores": 10,
        "dias_desde_ultima": 30
    }
    """
    try:
        X = np.array([[dados["idade"],
                       dados["faltas_anteriores"],
                       dados["consultas_anteriores"],
                       dados["dias_desde_ultima"]]])

        classe = int(modelo.predict(X)[0])
        prob_falta = float(modelo.predict_proba(X)[0][1])

        return {
            "resultado": "Faltará" if classe == 1 else "Comparecerá",
            "probabilidade_falta": round(prob_falta * 100, 2)
        }

    except Exception as e:
        return {"erro": f"Erro ao processar predição: {str(e)}"}
