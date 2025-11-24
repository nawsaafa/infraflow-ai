# InfraFlow AI Backend - Deployment Guide

## Quick Start (Development)

### 1. Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Redis (optional, for caching)
- API Keys: Anthropic, OpenAI, Pinecone

### 2. Setup

```bash
# Clone repository
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys and configuration

# Run database migrations (automatic on startup)
# Or manually create tables if needed

# Start server
./start.sh
# Or: uvicorn main:app --reload
```

### 3. Verify Installation

```bash
# Check health endpoint
curl http://localhost:8000/health

# View API documentation
open http://localhost:8000/api/docs
```

## Docker Deployment

### Development with Docker Compose

```bash
# Start all services (backend + postgres + redis)
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

### Production Docker Build

```bash
# Build production image
docker build --target production -t infraflow-backend:latest .

# Run container
docker run -d \
  --name infraflow-backend \
  -p 8000:8000 \
  --env-file .env \
  infraflow-backend:latest
```

## Cloud Deployment Options

### Option 1: Railway.app (Recommended - Easiest)

1. **Connect GitHub Repository**
   - Go to [Railway.app](https://railway.app)
   - Click "New Project" → "Deploy from GitHub"
   - Select your repository

2. **Configure Service**
   - Railway auto-detects Python/FastAPI
   - Root directory: `/backend`
   - Start command: `gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`

3. **Add Environment Variables**
   - Copy all variables from `.env.example`
   - Set in Railway dashboard

4. **Add PostgreSQL**
   - Click "New" → "Database" → "PostgreSQL"
   - Railway automatically sets `DATABASE_URL`

5. **Deploy**
   - Push to main branch
   - Railway auto-deploys

**Estimated Cost**: $5-20/month

### Option 2: Render

1. **Create New Web Service**
   - Go to [Render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your repository

2. **Configure Build**
   - Name: `infraflow-backend`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`

3. **Add Environment Variables**
   - Add all from `.env.example` in dashboard

4. **Add PostgreSQL**
   - Create new PostgreSQL database
   - Link to web service

**Estimated Cost**: Free tier available, $7+/month for production

### Option 3: Google Cloud Run (Serverless)

1. **Install gcloud CLI**
   ```bash
   # Install Google Cloud SDK
   curl https://sdk.cloud.google.com | bash
   gcloud init
   ```

2. **Build and Push to Container Registry**
   ```bash
   # Set project ID
   export PROJECT_ID=your-project-id

   # Build container
   gcloud builds submit --tag gcr.io/$PROJECT_ID/infraflow-backend
   ```

3. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy infraflow-backend \
     --image gcr.io/$PROJECT_ID/infraflow-backend \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars "ENV=production" \
     --min-instances 1 \
     --max-instances 10
   ```

4. **Add Secrets**
   ```bash
   # Create secrets for sensitive data
   echo -n "your-secret-key" | gcloud secrets create jwt-secret-key --data-file=-

   # Update service to use secrets
   gcloud run services update infraflow-backend \
     --update-secrets=JWT_SECRET_KEY=jwt-secret-key:latest
   ```

5. **Add Cloud SQL PostgreSQL**
   ```bash
   # Create Cloud SQL instance
   gcloud sql instances create infraflow-db \
     --database-version=POSTGRES_15 \
     --tier=db-f1-micro \
     --region=us-central1

   # Connect Cloud Run to Cloud SQL
   gcloud run services update infraflow-backend \
     --add-cloudsql-instances=$PROJECT_ID:us-central1:infraflow-db
   ```

**Estimated Cost**: Pay per request, ~$10-50/month for moderate traffic

### Option 4: AWS (ECS Fargate)

1. **Create ECR Repository**
   ```bash
   aws ecr create-repository --repository-name infraflow-backend
   ```

2. **Build and Push Image**
   ```bash
   # Login to ECR
   aws ecr get-login-password --region us-east-1 | \
     docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

   # Build and tag
   docker build -t infraflow-backend .
   docker tag infraflow-backend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/infraflow-backend:latest

   # Push
   docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/infraflow-backend:latest
   ```

3. **Create ECS Cluster and Task Definition**
   - Use AWS Console or CLI to create ECS cluster
   - Define task with environment variables
   - Configure load balancer

4. **Add RDS PostgreSQL**
   - Create RDS PostgreSQL instance
   - Set DATABASE_URL in task definition

**Estimated Cost**: $30-100/month

### Option 5: DigitalOcean App Platform

1. **Create New App**
   - Go to DigitalOcean App Platform
   - Connect GitHub repository

2. **Configure Component**
   - Type: Web Service
   - Source Directory: `/backend`
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8080`

3. **Add Environment Variables**
   - Add all from `.env.example`

4. **Add Managed PostgreSQL**
   - Add PostgreSQL database component
   - Connect to app

**Estimated Cost**: $12+/month

## Production Checklist

### Security
- [ ] Change `JWT_SECRET_KEY` to a strong random value
- [ ] Set `ENV=production`
- [ ] Set `DEBUG=False`
- [ ] Configure proper `CORS_ORIGINS`
- [ ] Enable HTTPS/TLS
- [ ] Set up firewall rules
- [ ] Use environment variables for all secrets (never commit)
- [ ] Enable rate limiting
- [ ] Set up API key rotation

### Database
- [ ] Use managed PostgreSQL (Supabase/RDS/Cloud SQL)
- [ ] Enable automatic backups
- [ ] Set up read replicas for scaling
- [ ] Configure connection pooling
- [ ] Set appropriate indexes

### Monitoring
- [ ] Configure Sentry for error tracking
- [ ] Set up application logs
- [ ] Configure uptime monitoring
- [ ] Set up alerts for errors
- [ ] Monitor API response times
- [ ] Track API usage and costs

### Performance
- [ ] Enable Redis caching
- [ ] Configure CDN for static assets
- [ ] Set up load balancing
- [ ] Enable compression
- [ ] Optimize database queries
- [ ] Configure worker processes based on CPU cores

### Backups
- [ ] Database backups (daily)
- [ ] Document storage backups
- [ ] Environment configuration backups
- [ ] Test restore procedures

### Documentation
- [ ] Update API documentation
- [ ] Document deployment process
- [ ] Create runbook for common issues
- [ ] Document environment variables
- [ ] Create disaster recovery plan

## Environment Variables Reference

### Required (Production)
```bash
# Core
ENV=production
DEBUG=False
JWT_SECRET_KEY=<generate-strong-random-key>

# Database
DATABASE_URL=postgresql://user:pass@host:5432/dbname
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=<your-key>

# AI Services
ANTHROPIC_API_KEY=sk-ant-api03-...
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=<your-key>
PINECONE_INDEX=infraflow-docs

# Storage
STORAGE_BUCKET=documents

# CORS
CORS_ORIGINS=https://your-frontend-domain.com
```

### Optional (Recommended)
```bash
# Monitoring
SENTRY_DSN=<your-sentry-dsn>

# Caching
REDIS_URL=redis://host:6379/0

# Rate Limiting
RATE_LIMIT_PER_MINUTE=100
```

## Scaling Strategy

### Horizontal Scaling
1. **Multiple Backend Instances**: Use load balancer to distribute traffic
2. **Database Read Replicas**: Split read/write operations
3. **Redis Cluster**: For distributed caching
4. **CDN**: Offload static content

### Vertical Scaling
1. **Instance Size**: Start with 1-2 vCPU, 2GB RAM
2. **Scale Up**: Monitor CPU/memory usage, scale as needed
3. **Database Size**: Start with smallest tier, upgrade based on usage

### Auto-scaling Configuration
```yaml
# Example for Cloud Run
min_instances: 1
max_instances: 100
target_cpu_utilization: 70
target_memory_utilization: 80
```

## Troubleshooting

### Common Issues

**Issue**: Database connection failures
```bash
# Check DATABASE_URL is correct
echo $DATABASE_URL

# Test connection
psql $DATABASE_URL -c "SELECT 1"

# Check firewall rules allow connection
```

**Issue**: API key errors
```bash
# Verify environment variables are set
env | grep API_KEY

# Test API key
curl -H "Authorization: Bearer sk-ant-..." https://api.anthropic.com/v1/models
```

**Issue**: Out of memory
```bash
# Check memory usage
docker stats

# Increase worker count or instance size
# Reduce num_simulations in Monte Carlo
```

**Issue**: Slow response times
```bash
# Enable caching
# Add database indexes
# Use connection pooling
# Scale horizontally
```

## Support & Maintenance

### Regular Tasks
- **Daily**: Monitor error rates and API usage
- **Weekly**: Review logs for anomalies
- **Monthly**: Review and optimize costs
- **Quarterly**: Security audit and dependency updates

### Updates
```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Test updates
pytest

# Deploy with zero downtime
# Use blue-green or rolling deployment
```

## Cost Optimization

### Tips
1. **Right-size Instances**: Don't over-provision
2. **Use Spot/Preemptible Instances**: For non-critical workloads
3. **Cache Aggressively**: Reduce API calls and database queries
4. **Optimize LLM Usage**: Use smaller models when appropriate
5. **Monitor API Costs**: Set up alerts for Claude/OpenAI usage
6. **Use Reserved Instances**: For predictable workloads

### Estimated Monthly Costs (Production)
```
Compute (Railway/Render):     $10-20
Database (Managed Postgres):  $15-25
Redis Cache:                  $5-10
Claude API (moderate usage):  $50-200
OpenAI API (embeddings):      $10-30
Pinecone (vector DB):         $70-150
Storage (Supabase):           $0-10
Monitoring (Sentry):          $0-26

Total:                        $160-471/month
```

Costs scale with usage. Start small and monitor.

## Next Steps

After deployment:
1. Test all endpoints with production data
2. Set up monitoring and alerts
3. Configure backup and recovery
4. Document deployment for team
5. Create incident response plan
6. Set up CI/CD pipeline

For help: support@infraflow.ai
