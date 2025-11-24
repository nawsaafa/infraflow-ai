# InfraFlow AI Backend - Quick Start Guide

Get the backend running in 5 minutes!

## Prerequisites

- Python 3.11+
- PostgreSQL 15+ (or use Docker Compose)

## Option 1: Docker Compose (Recommended for Testing)

The fastest way to get everything running:

```bash
# 1. Navigate to backend directory
cd backend

# 2. Copy environment template
cp .env.example .env

# 3. Edit .env with your API keys (minimum required):
#    - ANTHROPIC_API_KEY
#    - OPENAI_API_KEY
#    - PINECONE_API_KEY
nano .env

# 4. Start all services (backend + postgres + redis)
docker-compose up -d

# 5. View logs
docker-compose logs -f backend

# 6. Access the API
# API: http://localhost:8000
# Docs: http://localhost:8000/api/docs
```

That's it! The backend is running with a PostgreSQL database and Redis cache.

## Option 2: Local Python (For Development)

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy and configure environment
cp .env.example .env
nano .env  # Add your API keys

# Minimum required keys:
# - ANTHROPIC_API_KEY=sk-ant-api03-...
# - OPENAI_API_KEY=sk-...
# - PINECONE_API_KEY=...
# - DATABASE_URL=postgresql://user:pass@localhost:5432/infraflow
# - JWT_SECRET_KEY=your-secret-key

# 5. Run the server
./start.sh
# Or: uvicorn main:app --reload
```

## Option 3: Production Deployment (Railway - 1-Click)

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login to Railway
railway login

# 3. Initialize project
railway init

# 4. Link to existing project or create new
railway link

# 5. Add PostgreSQL
railway add postgresql

# 6. Set environment variables
railway variables set ANTHROPIC_API_KEY=sk-ant-...
railway variables set OPENAI_API_KEY=sk-...
railway variables set PINECONE_API_KEY=...
# ... etc

# 7. Deploy
railway up

# Your backend is now live!
```

## Getting Your API Keys

### 1. Anthropic Claude (Required)
- Go to: https://console.anthropic.com/
- Sign up and get API key
- Add to `.env`: `ANTHROPIC_API_KEY=sk-ant-api03-...`

### 2. OpenAI (Required for Embeddings)
- Go to: https://platform.openai.com/
- Get API key
- Add to `.env`: `OPENAI_API_KEY=sk-...`

### 3. Pinecone (Required for Vector Search)
- Go to: https://www.pinecone.io/
- Create free account
- Create index named `infraflow-docs`
- Get API key
- Add to `.env`:
  ```
  PINECONE_API_KEY=your-key
  PINECONE_INDEX=infraflow-docs
  ```

### 4. Supabase (Optional - for cloud database)
- Go to: https://supabase.com/
- Create project
- Get connection string and keys
- Add to `.env`:
  ```
  SUPABASE_URL=https://xxx.supabase.co
  SUPABASE_SERVICE_KEY=...
  DATABASE_URL=postgresql://...
  ```

## Testing the Installation

### 1. Check Health Endpoint
```bash
curl http://localhost:8000/health
```

Should return:
```json
{
  "status": "healthy",
  "timestamp": "2024-11-23T...",
  "version": "1.0.0"
}
```

### 2. View API Documentation
Open browser to: http://localhost:8000/api/docs

You'll see interactive Swagger UI with all endpoints.

### 3. Create a Test Project
```bash
# First, get a JWT token (in production, this comes from auth service)
# For testing, you can use a simple token

# Create project
curl -X POST "http://localhost:8000/api/projects/create" \
  -H "Authorization: Bearer your-test-token" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Solar Project",
    "country": "Egypt",
    "sector": "renewable_energy",
    "total_value": 1000000,
    "sponsor": "Test Corp"
  }'
```

## Troubleshooting

### "Connection refused" error
- Make sure PostgreSQL is running
- Check DATABASE_URL is correct
- If using Docker: `docker-compose ps` to see if services are up

### "Invalid API key" error
- Check your API keys in `.env`
- Make sure there are no extra spaces
- Verify keys are valid at respective provider dashboards

### "Module not found" error
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again

### Database connection error
- If using local PostgreSQL:
  ```bash
  # Create database
  createdb infraflow

  # Update .env
  DATABASE_URL=postgresql://localhost:5432/infraflow
  ```
- If using Docker Compose, the database is created automatically

### Port already in use
```bash
# Check what's using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use a different port
uvicorn main:app --port 8001
```

## Common Commands

### Start Server
```bash
# Development (with auto-reload)
uvicorn main:app --reload

# Production
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker

# With start script
./start.sh
```

### Docker Commands
```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild after code changes
docker-compose up -d --build

# Access database
docker-compose exec postgres psql -U infraflow -d infraflow
```

### Database Commands
```bash
# Create database
createdb infraflow

# Connect to database
psql infraflow

# Run migrations (automatic on startup)
# Or manually create tables if needed
```

## Next Steps

1. ✅ Backend running
2. 📝 Read `/api/docs` to understand all endpoints
3. 🔑 Get all API keys configured
4. 📊 Upload a test document
5. 🧪 Run analysis on a project
6. 🚀 Deploy to production

## Environment Variables Cheat Sheet

**Minimum Required:**
```bash
# AI Services
ANTHROPIC_API_KEY=sk-ant-api03-...
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=...

# Database
DATABASE_URL=postgresql://localhost:5432/infraflow

# Security
JWT_SECRET_KEY=change-this-to-random-string
```

**Production Required:**
```bash
# Add to minimum required:
ENV=production
DEBUG=False
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_KEY=...
CORS_ORIGINS=https://your-frontend.com
SENTRY_DSN=...  # For error tracking
```

## Getting Help

- 📖 Documentation: See `README.md` for detailed info
- 🚀 Deployment: See `DEPLOYMENT.md` for deployment guides
- 🐛 Issues: Check logs with `docker-compose logs -f backend`
- 💬 API Docs: http://localhost:8000/api/docs

## Example API Usage

### 1. Create Project
```bash
POST /api/projects/create
{
  "name": "Egypt Green Hydrogen",
  "country": "Egypt",
  "sector": "renewable_energy",
  "total_value": 5000000000,
  "sponsor": "Scatec ASA"
}
```

### 2. Upload Documents
```bash
POST /api/documents/upload
FormData: files=[file1.pdf, file2.docx]
```

### 3. Analyze Project
```bash
GET /api/projects/{project_id}/analyze
```

### 4. Run Compliance Check
```bash
POST /api/projects/{project_id}/compliance-check
{
  "standards": ["ebrd_environmental", "ifc_performance"]
}
```

### 5. Create Financial Model
```bash
POST /api/projects/{project_id}/financial-model
{
  "model_type": "dcf",
  "assumptions": {
    "discount_rate": 0.10,
    "project_lifetime": 25
  }
}
```

## Quick Tips

1. **API Documentation**: Always check `/api/docs` - it's auto-generated and interactive
2. **Logs**: Use `docker-compose logs -f` to see what's happening
3. **Database**: Use pgAdmin (port 5050) to inspect database if using Docker Compose
4. **Environment**: Always copy `.env.example` to `.env` and customize
5. **Testing**: Use the Swagger UI at `/api/docs` to test endpoints interactively

## Success Checklist

- [ ] Python 3.11+ installed
- [ ] API keys obtained (Claude, OpenAI, Pinecone)
- [ ] `.env` file configured
- [ ] Dependencies installed
- [ ] Server starts without errors
- [ ] `/health` endpoint returns 200
- [ ] `/api/docs` loads successfully
- [ ] Can create a test project
- [ ] Database connection working

If all checked, you're ready to go! 🚀

---

**Time to Hello World**: ~5 minutes with Docker Compose
**Time to Production**: ~30 minutes with Railway
