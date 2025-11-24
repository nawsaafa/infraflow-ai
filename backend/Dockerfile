# Multi-stage Dockerfile for FastAPI Backend
# Supports both development and production builds

# Base stage with common dependencies
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    make \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Create application directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Development stage
FROM base as development

# Install development dependencies
RUN pip install \
    pytest \
    pytest-asyncio \
    pytest-cov \
    black \
    flake8 \
    mypy \
    ipython \
    debugpy

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/uploads /app/temp /app/logs

# Expose port
EXPOSE 8000

# Run with hot reload
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Production stage
FROM base as production

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 infraflow && \
    chown -R infraflow:infraflow /app

# Create necessary directories with proper permissions
RUN mkdir -p /app/uploads /app/temp /app/logs && \
    chown -R infraflow:infraflow /app/uploads /app/temp /app/logs

# Switch to non-root user
USER infraflow

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run with gunicorn for production
CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--access-logfile", "-", "--error-logfile", "-"]
