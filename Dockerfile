FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Non-root user
RUN useradd -m -u 1000 user

# Install python dependencies (wheels only, no compiler needed)
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy source code and frontend
COPY --chown=user:user . .

USER user

# Cloud Run sets PORT (default 8080); falls back to 7860 elsewhere
ENV PORT=8080
EXPOSE 8080

CMD ["sh", "-c", "uvicorn src.api.main:app --host 0.0.0.0 --port ${PORT}"]
