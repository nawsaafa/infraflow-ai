#!/bin/bash

# InfraFlow AI - Backend Startup Script

echo "🚀 Starting InfraFlow AI Backend..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "📝 Please edit .env with your actual configuration"
    exit 1
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "🔧 Activating virtual environment..."
    source venv/bin/activate
else
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

# Check if dependencies are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

# Export environment variables
export $(grep -v '^#' .env | xargs)

# Start the server
echo "✅ Starting FastAPI server..."
echo "📍 API: http://localhost:${PORT:-8000}"
echo "📚 Docs: http://localhost:${PORT:-8000}/api/docs"

if [ "$ENV" = "production" ]; then
    echo "🏭 Running in PRODUCTION mode with Gunicorn..."
    gunicorn main:app \
        --workers ${WORKERS:-4} \
        --worker-class uvicorn.workers.UvicornWorker \
        --bind ${HOST:-0.0.0.0}:${PORT:-8000} \
        --access-logfile - \
        --error-logfile -
else
    echo "🔨 Running in DEVELOPMENT mode with Uvicorn..."
    uvicorn main:app \
        --host ${HOST:-0.0.0.0} \
        --port ${PORT:-8000} \
        --reload
fi
