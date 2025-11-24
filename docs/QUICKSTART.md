# InfraFlow AI - Quick Start Guide

Get up and running with InfraFlow AI in under 10 minutes.

## Prerequisites

Before you begin, ensure you have:

- Node.js 18+ and npm installed
- Python 3.11+ installed
- PostgreSQL 15+ running (or use Supabase)
- Git installed

## Step 1: Clone the Repository

```bash
git clone <repository-url>
cd infraflow-ai/00-pivot
```

## Step 2: Set Up Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your configuration
nano .env  # or use your preferred editor
```

### Minimum Required Variables

For local development, you need at least:

```env
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/infraflow_ai

# Backend
SECRET_KEY=your-secret-key-min-32-characters-long

# AI Services (optional for initial setup)
ANTHROPIC_API_KEY=your_anthropic_api_key
OPENAI_API_KEY=your_openai_api_key
```

## Step 3: Set Up the Database

### Option A: Using Supabase (Recommended)

1. Create a free account at [supabase.com](https://supabase.com)
2. Create a new project
3. Get your connection string and API keys
4. Update `.env` with your Supabase credentials
5. Run the migration:

```bash
cd database
psql <your-supabase-connection-string> < migrations/001_initial_schema.sql
```

### Option B: Using Local PostgreSQL

```bash
# Create database
createdb infraflow_ai

# Run migrations
cd database
psql infraflow_ai < migrations/001_initial_schema.sql
```

## Step 4: Set Up the Backend

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
uvicorn app.main:app --reload
```

The backend API will be available at: `http://localhost:8000`

## Step 5: Set Up the Frontend

Open a new terminal window:

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be available at: `http://localhost:3000`

## Step 6: Verify Installation

1. **Check Backend API**
   - Visit: `http://localhost:8000/health`
   - You should see: `{"status": "healthy", "service": "InfraFlow AI API"}`

2. **Check API Documentation**
   - Visit: `http://localhost:8000/api/docs`
   - You should see the interactive Swagger UI

3. **Check Frontend**
   - Visit: `http://localhost:3000`
   - You should see the InfraFlow AI landing page

## Step 7: Create Your First Project

### Using the API

```bash
# Create a project (replace YOUR_TOKEN with actual token)
curl -X POST "http://localhost:8000/api/v1/projects" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Infrastructure Project",
    "sponsor": "Test Sponsor",
    "country": "United States",
    "sector": "Renewable Energy",
    "total_value": 1000000
  }'
```

### Using the Frontend

1. Navigate to `http://localhost:3000/dashboard`
2. Click "New Project"
3. Fill in the project details
4. Click "Create Project"

## Next Steps

### Explore the Platform

1. **Upload Documents**
   - Navigate to your project
   - Click "Upload Documents"
   - Upload a PDF or Word document

2. **Run Analysis**
   - Click "Analyze Project"
   - Wait for AI analysis to complete
   - View the generated insights

3. **Generate Reports**
   - Click "Generate Report"
   - Select report type (Investment Memo, Compliance, etc.)
   - Download the generated report

### Configure AI Services

To enable full AI capabilities:

1. **Get Claude API Key**
   - Sign up at [console.anthropic.com](https://console.anthropic.com)
   - Create an API key
   - Add to `.env`: `ANTHROPIC_API_KEY=your_key`

2. **Get OpenAI API Key**
   - Sign up at [platform.openai.com](https://platform.openai.com)
   - Create an API key
   - Add to `.env`: `OPENAI_API_KEY=your_key`

3. **Set Up Vector Database**
   - For Pinecone: Sign up at [pinecone.io](https://www.pinecone.io)
   - For Weaviate: Use Docker or cloud instance
   - Add credentials to `.env`

### Customize the Platform

1. **Branding**
   - Update logo in `frontend/public/logo.png`
   - Update colors in `frontend/tailwind.config.ts`

2. **Add Custom Fields**
   - Modify database schema in `database/migrations/`
   - Update backend models in `backend/app/models/`
   - Update frontend types in `frontend/src/types/`

3. **Configure Compliance Standards**
   - Add standards in `backend/app/services/compliance_checker.py`
   - Update frontend options in compliance forms

## Troubleshooting

### Common Issues

#### "Module not found" errors

```bash
# Frontend
cd frontend && npm install

# Backend
cd backend && pip install -r requirements.txt
```

#### Database connection errors

```bash
# Check if PostgreSQL is running
pg_isready

# Verify connection string in .env
echo $DATABASE_URL
```

#### Port already in use

```bash
# Find and kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

#### Backend imports not working

```bash
# Make sure you're in the backend directory
cd backend

# Make sure virtual environment is activated
source venv/bin/activate

# Make sure __init__.py files exist
find app -name __init__.py
```

## Development Workflow

### Making Changes

1. **Frontend Changes**
   - Edit files in `frontend/src/`
   - Changes hot-reload automatically
   - Check console for errors

2. **Backend Changes**
   - Edit files in `backend/app/`
   - Server auto-reloads (with `--reload` flag)
   - Check terminal for errors

3. **Database Changes**
   - Create new migration file in `database/migrations/`
   - Run migration: `psql <connection-string> < migration.sql`
   - Update models in `backend/app/models/`

### Testing

```bash
# Frontend tests
cd frontend
npm run test

# Backend tests
cd backend
pytest

# E2E tests
npm run test:e2e
```

## Getting Help

- **Documentation**: Check the `docs/` folder
- **API Reference**: `http://localhost:8000/api/docs`
- **GitHub Issues**: Report bugs and request features
- **Discord**: Join our community (link in README)

## What's Next?

1. Read the [Architecture Documentation](./ARCHITECTURE.md)
2. Explore the [API Documentation](./API.md)
3. Check out the [Development Guide](./DEVELOPMENT.md)
4. Review the [Deployment Guide](./DEPLOYMENT.md)

---

**Happy Building!** 🚀
