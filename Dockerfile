FROM python:3.11-slim

WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia arquivos de dependências
COPY pyproject.toml .
COPY README.md .

# Instala o pacote
RUN pip install --no-cache-dir -e ".[deploy]"

# Copia o código fonte
COPY src/ ./src/

# Cria diretórios para logs e dados
RUN mkdir -p /app/logs /app/models /app/data

# Expõe as portas
EXPOSE 8000 8050

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Comando padrão
CMD ["uvicorn", "src.sentiment_analysis.api.main:api", "--host", "0.0.0.0", "--port", "8000"]