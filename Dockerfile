FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Install system dependencies (if needed for bdshare)
RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  && rm -rf /var/lib/apt/lists/*

# Copy project files needed for uv sync
COPY pyproject.toml uv.lock README.md ./

# Install Python dependencies using uv
RUN uv sync --frozen --no-install-project

# Copy application files
COPY server.py .
COPY dse_data.py .
COPY technical_analysis.py .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD .venv/bin/python -c "import requests; requests.get('http://localhost:8000')" || exit 1

# Run server in HTTP mode
CMD [".venv/bin/python", "server.py", "--transport", "http", "--host", "0.0.0.0", "--port", "8000"]
