# InfraFlow AI Platform

**Infrastructure Finance Intelligence Platform**

Transform infrastructure project finance by reducing due diligence time by 50%, improving project success rates by 30%, and unlocking $1 trillion in energy transition financing.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Development Setup](#development-setup)
- [Production Deployment](#production-deployment)
- [Architecture](#architecture)
- [API Documentation](#api-documentation)
- [Environment Variables](#environment-variables)
- [Docker Services](#docker-services)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

InfraFlow AI is an AI-powered platform that serves as a bridge between Development Finance Institutions (DFIs) and energy transition projects. The platform processes complex project finance documents, generates compliance reports, and provides predictive analytics for infrastructure investments.

### Target Users

- **Primary**: Investment Officers at DFIs (EBRD, EIB, BII, AfDB)
- **Secondary**: Project Sponsors, Government Agencies, EPCs
- **Tertiary**: Legal Advisors, Technical Consultants

---

## Features

### Core Capabilities

- **Document Intelligence**
  - Multi-language ingestion (EN, FR, AR, ES, PT)
  - Extract key terms from 1000+ page documents
  - Auto-generate executive summaries
  - Risk factor identification
  - Regulatory compliance checking

- **Financial Modeling**
  - DCF analysis with 10,000 Monte Carlo scenarios
  - Blended finance structuring
  - Currency risk modeling
  - Political risk quantification
  - Carbon credit valuation

- **Stakeholder Management**
  - Track 50+ stakeholders per project
  - Automated status updates
  - Milestone monitoring
  - Issue escalation system

- **Compliance Engine**
  - EBRD Environmental Standards
  - IFC Performance Standards
  - EU Taxonomy alignment
  - Local content requirements
  - ESG scoring

---

## Tech Stack

### Frontend
- **Framework**: Next.js 14 with App Router
- **UI Library**: Shadcn/ui + Tailwind CSS
- **Charts**: Tremor.so for financial dashboards
- **Auth**: Clerk or Supabase Auth
- **Hosting**: Vercel

### Backend
- **API**: FastAPI (Python)
- **Document Processing**: LangChain + Unstructured.io
- **LLM Orchestration**: LangGraph
- **Financial Modeling**: NumPy, Pandas, SciPy
- **Hosting**: Railway.app or Render

### Database
- **Primary**: PostgreSQL (Supabase)
- **Vector**: Pinecone or Weaviate
- **Cache**: Redis (Upstash)
- **Files**: Cloudflare R2 or AWS S3

### AI/ML
- **LLM**: Claude 3.5 Sonnet via API
- **Embeddings**: OpenAI Ada or Cohere
- **OCR**: Azure Document Intelligence
- **Training**: Modal.com for custom models

### Automation
- **Workflows**: n8n (self-hosted)
- **MCP**: Custom MCP servers for DFI integrations
- **Monitoring**: Posthog analytics

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Docker** (version 20.10+)
- **Docker Compose** (version 2.0+)
- **Git**
- **Node.js** (18.17.0+) - for local development
- **Python** (3.11+) - for local development

### System Requirements

- **Minimum**: 8GB RAM, 20GB disk space
- **Recommended**: 16GB RAM, 50GB disk space
- **OS**: Linux, macOS, or Windows with WSL2

---

## Quick Start

### One-Command Launch

```bash
# Clone the repository
git clone https://github.com/your-org/infraflow-ai.git
cd infraflow-ai/00-pivot

# Make the start script executable
chmod +x start.sh

# Launch the platform (development mode)
./start.sh
```

That's it! The platform will:
1. Check prerequisites
2. Set up environment variables
3. Start all services in Docker
4. Run health checks
5. Display access URLs

### Access the Platform

Once started, access these services:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

---

## Development Setup

### Option 1: Using Docker (Recommended)

```bash
# Start in development mode with hot reload
./start.sh dev

# Start with development tools (pgAdmin, Redis Commander)
./start.sh tools

# View logs
./start.sh logs

# Stop services
./start.sh stop
```

### Option 2: Local Development (Without Docker)

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp ../.env.example ../.env
# Edit .env with your configuration

# Run database migrations
alembic upgrade head

# Start development server
uvicorn main:app --reload --port 8000
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables (if not already done)
cp ../.env.example ../.env

# Start development server
npm run dev
```

### Database Initialization

The PostgreSQL database is automatically initialized with the schema defined in `/init-scripts/01-init-db.sql`.

To manually run migrations:

```bash
# Inside backend container
docker-compose exec backend alembic upgrade head

# Or locally
cd backend
alembic upgrade head
```

---

## Production Deployment

### Using Docker Compose

```bash
# Build and start in production mode
./start.sh prod

# Or manually
docker-compose -f docker-compose.yml up -d --build
```

### Environment Configuration

For production, create a `.env.production` file:

```bash
cp .env.example .env.production
# Update with production values
```

Key production settings:
- Set `ENVIRONMENT=production`
- Set `NODE_ENV=production`
- Use strong, unique secrets
- Configure proper CORS origins
- Set up SSL/TLS certificates
- Configure production database URLs
- Use production API keys

### Deploying to Cloud Platforms

#### Vercel (Frontend)

```bash
cd frontend
vercel --prod
```

#### Railway/Render (Backend)

```bash
# Connect your repository
# Add environment variables
# Deploy via Git push
```

#### AWS/GCP/Azure

See detailed cloud deployment guides in `/docs/deployment/`.

---

## Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend Layer                          │
│  Next.js 14 • Shadcn/ui • Tailwind • Tremor.so            │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                      API Gateway                            │
│         FastAPI • GraphQL • Auth • Rate Limiting            │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                   Core Processing Layer                      │
│  Document AI • Financial Engine • Compliance • ML Pipeline  │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                      Data Layer                             │
│  PostgreSQL • Pinecone/Weaviate • Redis • S3/R2            │
└─────────────────────────────────────────────────────────────┘
```

### Container Architecture

See `docker-compose.yml` for complete service definitions.

---

## API Documentation

### Interactive API Docs

Once the backend is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

### Core Endpoints

#### Projects

- `POST /api/v1/projects/create` - Create new project
- `GET /api/v1/projects` - List all projects
- `GET /api/v1/projects/{id}` - Get project details
- `PATCH /api/v1/projects/{id}` - Update project
- `DELETE /api/v1/projects/{id}` - Delete project

#### Documents

- `POST /api/v1/documents/upload` - Upload documents
- `GET /api/v1/documents/{id}` - Get document details
- `GET /api/v1/projects/{id}/documents` - List project documents

#### Analysis

- `GET /api/v1/projects/{id}/analyze` - Run comprehensive analysis
- `POST /api/v1/projects/{id}/financial-model` - Create financial model
- `POST /api/v1/projects/{id}/compliance-check` - Run compliance check
- `GET /api/v1/projects/{id}/risk-assessment` - Get risk assessment

---

## Environment Variables

### Required Variables

See `.env.example` for a complete list of environment variables.

Key variables you must configure:

```bash
# Database
DATABASE_URL=postgresql://user:password@host:port/database

# Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_KEY=your_service_key

# AI Services
ANTHROPIC_API_KEY=your_claude_api_key
OPENAI_API_KEY=your_openai_key

# Security
JWT_SECRET=your_jwt_secret_32_chars_minimum
```

### Generating Secrets

```bash
# Generate a secure random secret
openssl rand -hex 32
```

---

## Docker Services

### Core Services

| Service | Port | Description |
|---------|------|-------------|
| Frontend | 3000 | Next.js application |
| Backend | 8000 | FastAPI application |
| PostgreSQL | 5432 | Primary database |
| Redis | 6379 | Cache and queue |

### Optional Services

| Service | Port | Profile | Description |
|---------|------|---------|-------------|
| Weaviate | 8080 | vector-db | Vector database |
| n8n | 5678 | automation | Workflow automation |
| pgAdmin | 5050 | dev-tools | PostgreSQL management |
| Redis Commander | 8081 | dev-tools | Redis management |

### Using Service Profiles

```bash
# Start with specific profiles
docker-compose --profile dev-tools up -d
docker-compose --profile automation up -d
docker-compose --profile vector-db up -d

# Or use the start script
./start.sh tools  # Includes dev-tools
./start.sh full   # Includes all profiles
```

---

## Troubleshooting

### Common Issues

#### Port Already in Use

```bash
# Find and stop the process using the port
lsof -ti:3000 | xargs kill -9  # Frontend
lsof -ti:8000 | xargs kill -9  # Backend
```

#### Database Connection Issues

```bash
# Check PostgreSQL is running
docker-compose ps postgres

# View PostgreSQL logs
docker-compose logs postgres

# Restart PostgreSQL
docker-compose restart postgres
```

#### Build Failures

```bash
# Clean rebuild
./start.sh clean
./start.sh dev
```

#### Permission Denied Errors

```bash
# Fix file permissions
chmod +x start.sh
sudo chown -R $USER:$USER .
```

### View Logs

```bash
# All services
./start.sh logs

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

### Health Checks

```bash
# Backend health
curl http://localhost:8000/health

# PostgreSQL
docker-compose exec postgres pg_isready

# Redis
docker-compose exec redis redis-cli ping
```

---

## Development Tools

### Database Management

Access pgAdmin at http://localhost:5050 (when using `tools` profile)

**Credentials** (from .env):
- Email: admin@infraflow.ai
- Password: (set in .env)

### Redis Management

Access Redis Commander at http://localhost:8081 (when using `tools` profile)

### n8n Workflow Automation

Access n8n at http://localhost:5678 (when using `automation` profile)

**Credentials** (from .env):
- Username: admin
- Password: (set in .env)

---

## CI/CD

### GitHub Actions

The platform includes automated CI/CD workflows:

- **Build & Test**: Runs on every push
- **Deploy**: Runs on merge to main branch
- **Security Scan**: Runs daily

See `.github/workflows/` for workflow definitions.

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## Success Metrics

### Week 1
- Landing page live
- Document upload working
- Basic project creation

### Week 2
- Process first real project
- Generate compliance report
- Basic financial model

### Week 4
- 3 projects processed
- First DFI user test
- Risk prediction model v1

### Week 8
- 10 projects in system
- Pilot with one DFI
- $100K in pipeline influenced

---

## Support

- **Documentation**: [docs.infraflow.ai](https://docs.infraflow.ai)
- **Issues**: [GitHub Issues](https://github.com/your-org/infraflow-ai/issues)
- **Email**: support@infraflow.ai
- **Discord**: [Join our community](https://discord.gg/infraflow)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Built with Claude 3.5 Sonnet
- Powered by Anthropic's Claude API
- Infrastructure by Supabase, Vercel, and Railway
- Open source community

---

**InfraFlow AI** - Accelerating the Energy Transition through Intelligent Finance

Made with ❤️ for a sustainable future
