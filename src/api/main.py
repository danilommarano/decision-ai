from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# ==== 1. Carregar modelo ====
model = joblib.load("src/model/modelo_contratacao.joblib")

# ==== 2. Criar app FastAPI ====
app = FastAPI(title="API de Predição de Contratação", version="1.0")

# ==== 3. Definir schema da entrada ====
class CandidatoInput(BaseModel):
    nivel_profissional: str
    nivel_academico_y: str
    nivel_ingles_y: str
    area_atuacao: str
    titulo_vaga: str
    comentario: str
    competencia_tecnicas_e_comportamentais: str

# ==== 4. Rota de predição ====
@app.post("/predict")
def predict(input_data: CandidatoInput):
    data = pd.DataFrame([input_data.dict()])
    prediction = model.predict(data)[0]
    probability = model.predict_proba(data)[0][1]
    
    return {
        "contratado": bool(prediction),
        "probabilidade_contratacao": round(float(probability), 4)
    }
