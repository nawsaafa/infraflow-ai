# InfraFlow AI - Backend

FastAPI backend for the Infrastructure Finance Intelligence Platform.

## Overview

This backend provides comprehensive APIs for:
- Project management and tracking
- Document upload and AI-powered processing
- Financial modeling (DCF, Monte Carlo, Blended Finance)
- Compliance checking against DFI standards
- Risk assessment and analysis
- AI-powered insights and recommendations

## Tech Stack

- **Framework**: FastAPI with async/await
- **Database**: PostgreSQL via Supabase
- **Vector DB**: Pinecone for document embeddings
- **AI**: Claude 3.5 Sonnet via Anthropic API
- **Document Processing**: LangChain + Unstructured.io
- **Authentication**: JWT-based auth

## Project Structure

```
backend/
├── main.py                    # FastAPI application with all endpoints
├── models.py                  # Pydantic models for request/response validation
├── database.py                # Database connection and operations
├── document_processor.py      # Document processing with LangChain
├── financial_engine.py        # Financial modeling and analysis
├── compliance_checker.py      # Compliance verification engine
├── auth.py                    # Authentication middleware
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## Setup

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API keys and configuration
nano .env  # or use your preferred editor
```

Required environment variables:
- `DATABASE_URL`: PostgreSQL connection string
- `SUPABASE_URL` & `SUPABASE_SERVICE_KEY`: Supabase configuration
- `ANTHROPIC_API_KEY`: Claude API key
- `OPENAI_API_KEY`: OpenAI API key (for embeddings)
- `PINECONE_API_KEY`: Pinecone vector database key
- `JWT_SECRET_KEY`: Secret key for JWT tokens

### 3. Initialize Database

The database schema is automatically created on first run. Tables include:
- `projects`: Project metadata
- `documents`: Document metadata and extracted data
- `financial_models`: Financial model results
- `compliance_checks`: Compliance check results

### 4. Run Development Server

```bash
# Run with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or use the python directly
python main.py
```

The API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/api/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/api/redoc (Alternative docs)

## API Endpoints

### Projects

- `POST /api/projects/create` - Create new project
- `GET /api/projects` - List all projects (with filters)
- `GET /api/projects/{id}` - Get project details
- `PATCH /api/projects/{id}` - Update project
- `DELETE /api/projects/{id}` - Delete project

### Documents

- `POST /api/documents/upload` - Upload and process documents
- `GET /api/documents/{id}` - Get document details
- `GET /api/projects/{id}/documents` - List project documents

### Analysis

- `GET /api/projects/{id}/analyze` - Run comprehensive analysis
- `GET /api/projects/{id}/risk-assessment` - Get risk assessment

### Financial Modeling

- `POST /api/projects/{id}/financial-model` - Create financial model
- `GET /api/projects/{id}/financial-models` - List financial models

### Compliance

- `POST /api/projects/{id}/compliance-check` - Run compliance check
- `GET /api/projects/{id}/compliance-checks` - List compliance checks

### System

- `GET /health` - Health check endpoint

## Authentication

All endpoints (except `/health`) require JWT authentication.

### Getting a Token

In production, tokens are issued by your authentication service. For development:

```python
from auth import create_user_token

token = create_user_token(
    user_id="user123",
    email="user@example.com",
    name="John Doe",
    organization="Example Corp"
)
```

### Using the Token

Include the token in the Authorization header:

```bash
curl -H "Authorization: Bearer <your-token>" \
  http://localhost:8000/api/projects
```

## Document Processing Pipeline

When documents are uploaded:

1. **Load & Parse**: Extract text using appropriate loader (PDF, DOCX, etc.)
2. **Smart Chunking**: Split into manageable chunks with overlap
3. **AI Extraction**: Claude extracts structured data (project details, financials, risks)
4. **Embeddings**: Generate embeddings for vector search
5. **Storage**: Upload to Supabase storage, save metadata to database

## Financial Modeling

Supported model types:

### DCF (Discounted Cash Flow)
- NPV calculation
- IRR calculation
- Payback period
- Scenario analysis
- Sensitivity analysis

### Monte Carlo Simulation
- 1,000-100,000 simulations
- Probabilistic NPV/IRR
- Risk distributions
- Confidence intervals

### Blended Finance
- Multi-source financing analysis
- Blended cost of capital
- Subsidy optimization

## Compliance Standards

Supported standards:
- **EBRD Environmental and Social Policy**
- **IFC Performance Standards**
- **EU Taxonomy for Sustainable Activities**
- **Equator Principles**
- **Local Content Requirements**
- **ESG Scoring Framework**

## Error Handling

All endpoints return consistent error responses:

```json
{
  "error": "Error message",
  "status_code": 400,
  "timestamp": "2024-01-15T10:00:00Z"
}
```

HTTP status codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `429`: Too Many Requests
- `500`: Internal Server Error

## Rate Limiting

Default limits:
- 100 requests per minute per user
- Configurable via environment variables

## Development

### Running Tests

```bash
pytest tests/ -v --cov=backend
```

### Code Formatting

```bash
# Format code
black backend/

# Sort imports
isort backend/

# Type checking
mypy backend/
```

### Linting

```bash
flake8 backend/
```

## Production Deployment

### Environment Variables

Ensure all production environment variables are set:
- Use strong `JWT_SECRET_KEY`
- Set `ENV=production`
- Set `DEBUG=False`
- Configure proper `CORS_ORIGINS`
- Enable monitoring with `SENTRY_DSN`

### Running with Gunicorn

```bash
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

### Recommended Hosting

- **Railway.app**: Easiest deployment
- **Render**: Good free tier
- **Fly.io**: Global edge deployment
- **Google Cloud Run**: Serverless containers
- **AWS ECS/Fargate**: Enterprise-grade

## Monitoring

### Health Check

```bash
curl http://localhost:8000/health
```

Returns:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:00:00Z",
  "version": "1.0.0"
}
```

### Logs

Structured logging to stdout/stderr:
```
2024-01-15 10:00:00 - backend.main - INFO - Starting InfraFlow AI API...
2024-01-15 10:00:01 - backend.database - INFO - Database connected
```

### Error Tracking

Configure Sentry for error tracking:
```bash
SENTRY_DSN=your-sentry-dsn
```

## Support

For issues or questions:
- GitHub Issues: [your-repo]/issues
- Documentation: [your-docs-url]
- Email: support@infraflow.ai

## License

Copyright © 2024 InfraFlow AI. All rights reserved.
