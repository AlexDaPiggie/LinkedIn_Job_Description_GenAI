FROM python:3.11-slim

WORKDIR /app

# Create non-root user (standard for Hugging Face Spaces)
RUN useradd -m -u 1000 user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy source code and frontend
COPY --chown=user:user . .

USER user

# Hugging Face Spaces default port
EXPOSE 7860

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "7860"]
