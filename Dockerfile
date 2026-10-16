# Imagem oficial Python verificada no Docker Hub, com tag fixa (sem "latest")
# para garantir builds reprodutiveis. slim-bookworm reduz a superficie de
# pacotes do sistema operacional mantendo compatibilidade com wheels manylinux.
FROM python:3.14.8-slim-bookworm

# Evita a geracao de arquivos .pyc/__pycache__ (cache desnecessario em
# container efemero) e garante que stdout/stderr nao fiquem bufferizados,
# permitindo que os logs apareçam em tempo real (`docker logs`).
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# Pacotes de sistema: apenas o curl, necessario para o HEALTHCHECK validar
# os endpoints de liveness/readiness. --no-install-recommends evita pacotes
# opcionais desnecessarios e o cache do apt e removido na mesma camada para
# nao inflar a imagem final.
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Usuario de baixa permissao que executara a aplicacao (nunca como root).
RUN groupadd --system app \
    && useradd --system --no-create-home --gid app \
        --shell /usr/sbin/nologin app

# Dependencias copiadas e instaladas antes do codigo da aplicacao para
# aproveitar o cache de camadas do Docker (so reinstala se o
# requirements.txt mudar).
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# pyproject.toml atua como marcador da raiz do projeto, usado em runtime
# por `encontrar_raiz_projeto()` para localizar `models/` dinamicamente.
COPY pyproject.toml ./

# Apenas o necessario para servir os endpoints: o pacote da aplicacao e o
# artefato do modelo treinado. Diretorios de desenvolvimento (tests/,
# notebooks/, docs/, scripts/, data/, .dvc/) ficam de fora via .dockerignore
# e por nao serem copiados explicitamente aqui.
COPY src/tech_challenge_churn_prediction ./tech_challenge_churn_prediction
COPY models ./models

# As variaveis de ambiente da aplicacao (APP_*, LOG_*, MODEL_*, SECURITY_*)
# nao sao definidas aqui: sao carregadas dinamicamente a partir do .env via
# `env_file` no docker-compose.yml, mantendo a imagem agnostica de ambiente.
RUN chown -R app:app /app
USER app

# Porta exposta dentro da rede isolada do container (mapeada para 8001 no
# host via docker-compose.yml).
EXPOSE 8000

# O HEALTHCHECK foi movido para o docker-compose.yml (campo `healthcheck`),
# junto com a politica de restart e os limites de recursos do servico.

# Inicializa o servidor a partir de app.py
# (tech_challenge_churn_prediction.app:app).
CMD ["python", "-m", "uvicorn", "tech_challenge_churn_prediction.app:app", "--host", "0.0.0.0", "--port", "8000"]
