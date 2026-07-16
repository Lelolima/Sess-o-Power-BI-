# =============================================================================
# Dockerfile para Dashboard Hospitalar - Versão Web
# =============================================================================
# Imagem base: Python 3.11 slim (otimizada para produção)
# Build: docker build -t dashboard-hospitalar .
# Run: docker run -p 8501:8501 dashboard-hospitalar
# =============================================================================

FROM python:3.11-slim

# Labels de metadados
LABEL maintainer="Wellington de Lima Catarina <lelolima806@gmail.com>"
LABEL description="Dashboard Hospitalar Power BI - Versão Web Streamlit"
LABEL version="1.0.0"

# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primeiro (cache layer)
COPY src/web/requirements.txt .
COPY requirements-dev.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir -r requirements-dev.txt

# Copiar código fonte
COPY src/ ./src/
COPY tests/ ./tests/
COPY pytest.ini .

# Criar usuário não-root para segurança
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app
USER appuser

# Expor porta
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8501')" || exit 1

# Comando de entrada
CMD ["streamlit", "run", "src/web/app.py"]