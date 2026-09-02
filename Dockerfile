FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-install-project

COPY server.py .
COPY dse_data.py .
COPY technical_analysis.py .

EXPOSE 8765

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD .venv/bin/python -c "import requests; requests.get('http://localhost:8765')" || exit 1

CMD [".venv/bin/python", "server.py", "--transport", "http", "--host", "0.0.0.0", "--port", "8765"]
