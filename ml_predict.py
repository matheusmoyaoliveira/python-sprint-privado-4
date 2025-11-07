import os
import joblib
import pandas as pd
import gdown


MODEL_DRIVE_ID = "1YcOlIeY-aBSM7BKn1G64wg83xnHaM0Tk"
MODEL_URL = f"https://drive.google.com/uc?export=download&id={MODEL_DRIVE_ID}"
MODEL_PATH = os.path.join(os.getcwd(), "regressao.joblib")

NUMERIC_COLS = [
    "age", "scholarship", "hipertension", "diabetes", "alcoholism",
    "handcap", "sms_received", "waiting_days", "appt_dow", "sched_hour", "is_weekend"
]
CATEGORICAL_COLS = ["gender", "neighbourhood"]

_model = None
_SCHEMA = None

def _baixar_modelo():
    """Baixa o modelo de regressão do Google Drive (forçando substituição)."""
    print("📦 Baixando modelo de regressão do Google Drive...")
    try:
        if os.path.exists(MODEL_PATH):
            os.remove(MODEL_PATH)

        gdown.download(MODEL_URL, MODEL_PATH, quiet=False, fuzzy=True)

        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError("Download falhou: arquivo não encontrado após download.")

        print("✅ Modelo baixado com sucesso!")
    except Exception as e:
        raise RuntimeError(f"Falha ao baixar modelo: {e}")

def _ensure_model():
    """Garante que o modelo esteja carregado e disponível."""
    global _model, _SCHEMA
    if _model is not None:
        return

    _baixar_modelo()

    try:
        _model = joblib.load(MODEL_PATH)
    except Exception:
        print("⚠️ Modelo corrompido — baixando novamente...")
        _baixar_modelo()
        _model = joblib.load(MODEL_PATH)

    nomes = getattr(_model, "feature_names_in_", None)
    if nomes is not None:
        _SCHEMA = list(nomes)
        return

    try:
        for _, step in getattr(_model, "steps", []):
            nomes = getattr(step, "feature_names_in_", None)
            if nomes is not None:
                _SCHEMA = list(nomes)
                return
    except Exception:
        pass

    n = getattr(_model, "n_features_in_", None)
    if n:
        _SCHEMA = {"n_features_in": int(n)}
    else:
        _SCHEMA = None

def schema_esperado():
    try:
        _ensure_model()
        return _SCHEMA
    except Exception as e:
        return {"erro": str(e)}

def prever_probabilidade(dados: dict):
    try:
        _ensure_model()
        if not isinstance(_SCHEMA, list):
            return {"erro": "Schema indisponível; reexporte o modelo com feature_names_in_."}

        cols = _SCHEMA[:]
        faltando = [c for c in cols if c not in dados]
        if faltando:
            return {"erro": f"JSON incompleto. Faltam: {faltando}", "schema_esperado": cols}

        linha = {}
        for col in cols:
            val = dados[col]
            if col in NUMERIC_COLS:
                linha[col] = float(val)
            else:
                linha[col] = str(val)

        X = pd.DataFrame([linha], columns=cols)
        y = float(_model.predict(X)[0])
        prob_pct = round(max(0.0, min(y * 100.0, 100.0)), 2)

        return {
            "probabilidade_comparecimento": f"{prob_pct}%",
            "mensagem": "Alta probabilidade de comparecimento ✅" if prob_pct >= 70 else "Risco de falta detectado ⚠️",
            "schema_utilizado": cols
        }
    except Exception as e:
        return {"erro": f"Erro ao processar previsão: {str(e)}"}
