# Base Python
FROM python:3.12-slim

# Criar diretório de trabalho
WORKDIR /app

# Copiar arquivos necessários
COPY requirements.txt .
COPY src/ src/

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Gerar o modelo novamente (caso não esteja incluso)
RUN python src/model.py

# Expor porta da API
EXPOSE 8000

# Comando para iniciar a API
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
