# =========================================
# Stage 1: Build base image with dependencies
# =========================================
FROM python:3.12-slim AS base

# Prevent Python from writing .pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies (for psycopg2 & bcrypt)
RUN apt-get update && apt-get install -y \
    gcc libpq-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

# Install dependencies first for layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# =========================================
# Stage 2: Copy application
# =========================================
FROM base AS final
WORKDIR /app
COPY . .

ENV PASSLIB_BUILTIN_BCRYPT=1
# Default startup command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
