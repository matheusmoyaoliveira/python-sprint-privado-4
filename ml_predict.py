# ------------------------------------------------------------
# Módulo de Machine Learning integrado à API Python
# Usa o modelo de CLASSIFICAÇÃO da Sprint 4 de IA
# ------------------------------------------------------------

import joblib
import numpy as np

modelo = joblib.load("classificacao.joblib")

# ------------------------------------------------------------
# Função de predição
# ------------------------------------------------------------
def prever(dados):
    """
    Recebe um dicionário JSON com as features do paciente e retorna
    a probabilidade de falta e a classificação.
    Exemplo de entrada:
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
        probabilidade = float(modelo.predict_proba(X)[0][1])  

        
        return {
            "resultado": "Faltará" if classe == 1 else "Comparecerá",
            "probabilidade_falta": round(probabilidade * 100, 2)
        }

    except Exception as e:
        return {"erro": f"Erro ao processar predição: {str(e)}"}
