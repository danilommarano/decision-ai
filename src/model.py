import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import os

# === 1. Carregar dados ===
df = pd.read_csv("data/final.csv")

# === 2. Criar target se necessário ===
if "contratado" not in df.columns:
    df["contratado"] = df["situacao_candidado"].str.lower().str.contains("contratado").astype(int)

# === 3. Definir features ===
features = [
    "nivel_profissional", "nivel_academico_y", "nivel_ingles_y",
    "area_atuacao", "titulo_vaga", "comentario", "competencia_tecnicas_e_comportamentais"
]
target = "contratado"
df = df.fillna('')

# === 4. Separar em treino e teste ===
X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)

# === 5.Pré-processamento ===
cat_cols = ["nivel_profissional", "nivel_academico_y", "nivel_ingles_y", "area_atuacao"]
text_col = "comentario"

preprocessor = ColumnTransformer(transformers=[
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
    ("txt", TfidfVectorizer(), text_col)
])

# === 6. Pipeline ===
pipeline = Pipeline(steps=[
    ("preprocessamento", preprocessor),
    ("modelo", RandomForestClassifier(random_state=42))
])

# === 7. Treinar ===
pipeline.fit(X_train, y_train)

# === 8. Avaliação ===
y_pred = pipeline.predict(X_test)
print("📊 Relatório de Classificação:")
print(classification_report(y_test, y_pred))

# === 9. Salvar modelo ===
os.makedirs("src/model", exist_ok=True)
joblib.dump(pipeline, "src/model/modelo_contratacao.joblib")
print("✅ Modelo salvo em src/model/modelo_contratacao.joblib")
