# InfraFlow AI - Deployment Guide

This guide covers deployment strategies for the InfraFlow AI platform across different environments and cloud providers.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Environment Setup](#environment-setup)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployments](#cloud-deployments)
  - [Vercel (Frontend)](#vercel-frontend)
  - [Railway (Backend)](#railway-backend)
  - [Render (Backend)](#render-backend)
  - [AWS](#aws-deployment)
  - [Google Cloud Platform](#google-cloud-platform)
  - [Azure](#azure-deployment)
- [Database Setup](#database-setup)
- [Environment Variables](#environment-variables)
- [SSL/TLS Configuration](#ssltls-configuration)
- [Monitoring & Logging](#monitoring--logging)
- [Backup & Recovery](#backup--recovery)
- [Scaling](#scaling)

---

## Prerequisites

Before deploying, ensure you have:

1. **Accounts**:
   - GitHub account
   - Supabase account (for database)
   - Anthropic API key (for Claude)
   - Cloud provider account (Vercel, Railway, AWS, etc.)

2. **Tools**:
   - Git
   - Docker & Docker Compose
   - Cloud CLI tools (optional)

3. **Secrets**:
   - API keys for all services
   - Database credentials
   - JWT secrets

---

## Environment Setup

### 1. Clone Repository

```bash
git clone https://github.com/your-org/infraflow-ai.git
cd infraflow-ai/00-pivot
```

### 2. Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Generate secure secrets
openssl rand -hex 32  # For JWT_SECRET
openssl rand -hex 32  # For WEBHOOK_SECRET
openssl rand -hex 32  # For RATE_LIMIT_SECRET

# Edit .env with your values
nano .env
```

### 3. Verify Configuration

```bash
# Test with Docker Compose locally
./start.sh dev
```

---

## Docker Deployment

### Production Docker Compose

```bash
# Build and start in production mode
docker-compose -f docker-compose.yml up -d --build

# Or use the start script
./start.sh prod
```

### Using Docker Swarm

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml infraflow

# Check services
docker stack services infraflow

# Remove stack
docker stack rm infraflow
```

### Using Kubernetes

```bash
# Coming soon - Kubernetes manifests will be added to /k8s directory
```

---

## Cloud Deployments

### Vercel (Frontend)

**Recommended for Next.js frontend**

#### Method 1: Vercel CLI

```bash
cd frontend

# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
vercel --prod
```

#### Method 2: GitHub Integration

1. Connect repository to Vercel
2. Configure build settings:
   - **Framework**: Next.js
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
   - **Install Command**: `npm ci`

3. Add environment variables in Vercel dashboard:
   - `NEXT_PUBLIC_API_URL`
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`

4. Deploy automatically on push to main branch

### Railway (Backend)

**Recommended for FastAPI backend**

#### Deployment Steps

1. **Create New Project**:

   ```bash
   # Install Railway CLI
   npm i -g @railway/cli

   # Login
   railway login

   # Initialize project
   cd backend
   railway init
   ```

2. **Configure Service**:
   - Add PostgreSQL database plugin
   - Add Redis plugin
   - Set start command: `gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`

3. **Add Environment Variables**:

   ```bash
   railway variables set DATABASE_URL=$DATABASE_URL
   railway variables set REDIS_URL=$REDIS_URL
   railway variables set ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY
   # Add all other required variables
   ```

4. **Deploy**:

   ```bash
   railway up
   ```

### Render (Backend)

**Alternative to Railway**

1. Create new Web Service on Render
2. Connect GitHub repository
3. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`
4. Add environment variables
5. Deploy

### AWS Deployment

#### Using Elastic Beanstalk

```bash
# Install EB CLI
pip install awsebcli

# Initialize EB application
cd backend
eb init -p python-3.11 infraflow-backend

# Create environment
eb create infraflow-prod

# Deploy
eb deploy

# Open application
eb open
```

#### Using ECS (Docker)

```bash
# Build and push to ECR
aws ecr create-repository --repository-name infraflow-backend
docker build -t infraflow-backend .
docker tag infraflow-backend:latest $ECR_URL/infraflow-backend:latest
docker push $ECR_URL/infraflow-backend:latest

# Deploy with ECS
# Use AWS Console or Terraform to configure ECS cluster and services
```

#### Using Lambda (Serverless)

```bash
# Use AWS SAM or Serverless Framework
# Configuration files in /serverless directory (coming soon)
```

### Google Cloud Platform

#### Using Cloud Run

```bash
# Build and push to GCR
gcloud builds submit --tag gcr.io/$PROJECT_ID/infraflow-backend

# Deploy to Cloud Run
gcloud run deploy infraflow-backend \
  --image gcr.io/$PROJECT_ID/infraflow-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### Using App Engine

```bash
# Deploy with app.yaml
gcloud app deploy app.yaml
```

### Azure Deployment

#### Using App Service

```bash
# Create resource group
az group create --name infraflow-rg --location eastus

# Create App Service plan
az appservice plan create --name infraflow-plan --resource-group infraflow-rg --sku B1 --is-linux

# Create web app
az webapp create --resource-group infraflow-rg --plan infraflow-plan --name infraflow-backend --runtime "PYTHON|3.11"

# Deploy
az webapp up --name infraflow-backend --resource-group infraflow-rg
```

---

## Database Setup

### Supabase (Recommended)

1. **Create Project**:
   - Go to [supabase.com](https://supabase.com)
   - Create new project
   - Note: URL, anon key, service key

2. **Run Migrations**:

   ```bash
   # Using Supabase CLI
   supabase db push

   # Or run SQL directly in Supabase SQL Editor
   # Copy contents of init-scripts/01-init-db.sql
   ```

3. **Configure Connection**:

   ```bash
   DATABASE_URL=postgresql://postgres:[password]@db.[project-ref].supabase.co:5432/postgres
   ```

### Self-Hosted PostgreSQL

```bash
# Using Docker
docker run -d \
  --name infraflow-postgres \
  -e POSTGRES_PASSWORD=your_password \
  -e POSTGRES_DB=infraflow_db \
  -v postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:16-alpine
```

---

## Environment Variables

### Production Environment Variables

**Critical Variables** (must be set):

```bash
# Database
DATABASE_URL=postgresql://user:password@host:port/database

# Redis
REDIS_URL=redis://user:password@host:port

# Supabase
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_KEY=eyJxxx...

# AI Services
ANTHROPIC_API_KEY=sk-ant-xxx
OPENAI_API_KEY=sk-xxx

# Security
JWT_SECRET=your-32-char-secret
WEBHOOK_SECRET=your-32-char-secret
RATE_LIMIT_SECRET=your-32-char-secret

# Storage
AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=xxx
AWS_S3_BUCKET=infraflow-documents
```

### Setting Variables by Platform

**Vercel**:

```bash
vercel env add ANTHROPIC_API_KEY
```

**Railway**:

```bash
railway variables set ANTHROPIC_API_KEY=xxx
```

**Render**:

- Add via Dashboard → Environment tab

**AWS Elastic Beanstalk**:

```bash
eb setenv ANTHROPIC_API_KEY=xxx
```

---

## SSL/TLS Configuration

### Using Cloudflare

1. Add domain to Cloudflare
2. Enable SSL/TLS (Full mode)
3. Configure HTTPS redirects
4. Enable HTTP/2

### Using Let's Encrypt (Self-Hosted)

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d infraflow.ai -d www.infraflow.ai

# Auto-renewal
sudo certbot renew --dry-run
```

---

## Monitoring & Logging

### Sentry (Error Tracking)

```bash
# Add to .env
SENTRY_DSN=https://xxx@sentry.io/xxx
NEXT_PUBLIC_SENTRY_DSN=https://xxx@sentry.io/xxx
```

### PostHog (Analytics)

```bash
# Add to .env
NEXT_PUBLIC_POSTHOG_KEY=phc_xxx
NEXT_PUBLIC_POSTHOG_HOST=https://app.posthog.com
```

### Application Logs

```bash
# View Docker logs
docker-compose logs -f

# View Railway logs
railway logs

# View Render logs
# Via Render Dashboard
```

---

## Backup & Recovery

### Database Backups

```bash
# Automated daily backups (Supabase)
# Configured automatically in Supabase dashboard

# Manual backup
pg_dump -h host -U user -d infraflow_db > backup.sql

# Restore
psql -h host -U user -d infraflow_db < backup.sql
```

### File Storage Backups

```bash
# AWS S3
aws s3 sync s3://infraflow-documents ./backup/

# Restore
aws s3 sync ./backup/ s3://infraflow-documents
```

---

## Scaling

### Horizontal Scaling

**Backend**:

```bash
# Docker Compose
docker-compose up -d --scale backend=3

# Kubernetes
kubectl scale deployment/backend --replicas=3
```

**Frontend**:

- Vercel: Auto-scales
- Manual: Deploy multiple instances behind load balancer

### Vertical Scaling

- Increase container resources in docker-compose.yml
- Upgrade instance size on cloud provider

### Load Balancing

```bash
# Nginx configuration
upstream backend {
    server backend1:8000;
    server backend2:8000;
    server backend3:8000;
}
```

---

## Performance Optimization

1. **Enable Caching**:
   - Redis for API responses
   - CDN for static assets
   - Browser caching headers

2. **Database Optimization**:
   - Create indexes
   - Connection pooling
   - Query optimization

3. **CDN Configuration**:
   - Use Cloudflare/Vercel CDN
   - Optimize images
   - Enable compression

---

## Security Checklist

- [ ] Environment variables secured
- [ ] SSL/TLS enabled
- [ ] CORS configured properly
- [ ] Rate limiting enabled
- [ ] API authentication active
- [ ] Database encrypted
- [ ] File uploads validated
- [ ] Security headers configured
- [ ] Secrets rotated regularly
- [ ] Backups automated

---

## Troubleshooting

### Common Deployment Issues

**Build Failures**:

```bash
# Clear cache
docker-compose build --no-cache

# Check logs
docker-compose logs backend
```

**Database Connection**:

```bash
# Test connection
psql $DATABASE_URL

# Check firewall rules
```

**API Errors**:

```bash
# Check environment variables
env | grep API

# View application logs
railway logs -f
```

---

## Support

For deployment assistance:

- Email: <devops@infraflow.ai>
- Discord: [Join community](https://discord.gg/infraflow)
- Docs: [docs.infraflow.ai/deployment](https://docs.infraflow.ai/deployment)

---

**InfraFlow AI** - Deployment Guide
Last updated: 2025-01-23
