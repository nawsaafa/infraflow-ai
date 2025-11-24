# InfraFlow AI - Verification Checklist

Use this checklist to verify that all DevOps deliverables are properly set up.

## Pre-Flight Checks

### Prerequisites Installed
- [ ] Docker (version 20.10+)
- [ ] Docker Compose (version 2.0+)
- [ ] Git
- [ ] Text editor (VS Code, vim, nano, etc.)

### System Requirements
- [ ] 8GB+ RAM available
- [ ] 20GB+ disk space available
- [ ] Internet connection (for pulling images and dependencies)

## File Verification

### Docker Configuration Files
- [ ] `docker-compose.yml` exists and is valid
- [ ] `backend/Dockerfile` exists
- [ ] `frontend/Dockerfile` exists
- [ ] `backend/.dockerignore` exists
- [ ] `frontend/.dockerignore` exists

### Environment Configuration
- [ ] `.env.example` exists and is comprehensive
- [ ] `.env` file created (copy from .env.example)
- [ ] Critical environment variables set in `.env`

### Launch Scripts
- [ ] `start.sh` exists
- [ ] `start.sh` is executable (`chmod +x start.sh`)
- [ ] `Makefile` exists

### Database Setup
- [ ] `init-scripts/01-init-db.sql` exists
- [ ] SQL file is valid (no syntax errors)

### Documentation
- [ ] `README.md` exists and is comprehensive
- [ ] `DEPLOYMENT.md` exists
- [ ] `DEVOPS_HANDOFF.md` exists
- [ ] `SETUP_SUMMARY.txt` exists

### CI/CD Pipeline
- [ ] `.github/workflows/ci-cd.yml` exists
- [ ] `.github/workflows/security-scan.yml` exists

### Source Code
- [ ] `backend/main.py` exists
- [ ] `backend/requirements.txt` exists
- [ ] `frontend/package.json` exists

## Functionality Tests

### Quick Start Test
```bash
cd 00-pivot
./start.sh
```

- [ ] Script runs without errors
- [ ] Environment variables are set up
- [ ] Services start successfully
- [ ] Health checks pass

### Service Accessibility Tests

After running `./start.sh`, verify:

- [ ] Frontend accessible at http://localhost:3000
- [ ] Backend API accessible at http://localhost:8000
- [ ] API docs accessible at http://localhost:8000/api/docs
- [ ] PostgreSQL accepting connections on port 5432
- [ ] Redis accepting connections on port 6379

### Health Check Tests

Run these commands:

```bash
# Backend health
curl http://localhost:8000/health
# Should return: {"status":"healthy",...}

# PostgreSQL health
docker-compose exec postgres pg_isready
# Should return: accepting connections

# Redis health
docker-compose exec redis redis-cli ping
# Should return: PONG
```

- [ ] Backend health check returns "healthy"
- [ ] PostgreSQL is accepting connections
- [ ] Redis responds to ping

### Database Verification

```bash
# Connect to database
docker-compose exec postgres psql -U infraflow_user -d infraflow_db

# Check tables exist
\dt

# Exit
\q
```

- [ ] Can connect to database
- [ ] All 11 tables created
- [ ] No errors in database logs

### Docker Services Status

```bash
docker-compose ps
```

- [ ] All core services are "Up"
- [ ] No services in "Exit" or "Restarting" state
- [ ] Health checks showing as "healthy"

## Makefile Commands Test

Test key Makefile commands:

```bash
make help        # Shows all available commands
make status      # Shows service status
make health      # Checks health of all services
make ports       # Shows all exposed ports
```

- [ ] `make help` displays command list
- [ ] `make status` shows services running
- [ ] `make health` shows all services healthy
- [ ] `make ports` displays correct URLs

## Advanced Features Test

### Development Tools Profile

```bash
./start.sh tools
```

- [ ] pgAdmin accessible at http://localhost:5050
- [ ] Redis Commander accessible at http://localhost:8081

### Full Stack Profile

```bash
./start.sh full
```

- [ ] n8n accessible at http://localhost:5678
- [ ] Weaviate accessible at http://localhost:8080

## Service Management Tests

### Stop Services

```bash
./start.sh stop
```

- [ ] All services stop cleanly
- [ ] No containers left running

### Restart Services

```bash
./start.sh restart
```

- [ ] Services restart successfully
- [ ] All health checks pass after restart

## Database Operations Test

### Database Backup

```bash
make db-backup
```

- [ ] Backup file created in `backups/` directory
- [ ] Backup file is valid SQL

### Database Shell Access

```bash
make db-shell
```

- [ ] Can access PostgreSQL shell
- [ ] Can query tables

## Code Quality Tests (Optional)

If you have backend and frontend code:

```bash
make lint          # Run all linters
make format        # Format code
make test          # Run tests
```

## Security Checks

### Environment Variables

- [ ] No secrets committed to git
- [ ] `.env` file is in `.gitignore`
- [ ] `.env.example` has no real secrets

### Container Security

- [ ] Production containers run as non-root user
- [ ] No unnecessary packages in images
- [ ] Health checks configured

## Documentation Review

### README.md
- [ ] Quick start section is clear
- [ ] All commands are correct
- [ ] Troubleshooting section is helpful

### DEPLOYMENT.md
- [ ] Cloud deployment guides are complete
- [ ] Environment configuration is clear
- [ ] Security checklist is comprehensive

## Performance Checks

### Resource Usage

```bash
docker stats
```

- [ ] Memory usage is within acceptable limits
- [ ] CPU usage is reasonable
- [ ] No container constantly restarting

### Startup Time

- [ ] Platform starts in under 3 minutes
- [ ] All health checks pass within 2 minutes

## Final Verification

### Complete Workflow Test

1. **Clean Start**
   ```bash
   ./start.sh clean
   ./start.sh dev
   ```
   - [ ] Clean start works

2. **Access All Services**
   - [ ] Frontend loads
   - [ ] API docs accessible
   - [ ] Can make API request

3. **Database Operations**
   ```bash
   make db-backup
   make db-shell
   ```
   - [ ] Database operations work

4. **View Logs**
   ```bash
   ./start.sh logs
   ```
   - [ ] Logs are accessible
   - [ ] No critical errors

5. **Stop Services**
   ```bash
   ./start.sh stop
   ```
   - [ ] Services stop cleanly

## Deployment Readiness

### Production Checklist

- [ ] `.env` configured with production values
- [ ] SSL/TLS certificates obtained
- [ ] Domain name configured
- [ ] Monitoring set up (Sentry, PostHog)
- [ ] Backup strategy in place
- [ ] CI/CD pipeline tested
- [ ] Security scan completed
- [ ] Load testing performed (optional)

### Team Handoff

- [ ] Documentation shared with team
- [ ] Team members trained on startup scripts
- [ ] Access credentials distributed securely
- [ ] Support channels established

## Issue Tracking

If any checks fail, document here:

### Issues Found
1. 
2. 
3. 

### Resolved Issues
1. 
2. 
3. 

## Sign-Off

**Verified by:** _________________________

**Date:** _________________________

**Status:** [ ] PASS  [ ] FAIL (with issues documented)

**Notes:**




---

## Quick Troubleshooting

### Issue: Port already in use
**Solution:**
```bash
lsof -ti:3000 | xargs kill -9
lsof -ti:8000 | xargs kill -9
```

### Issue: Permission denied
**Solution:**
```bash
chmod +x start.sh
sudo chown -R $USER:$USER .
```

### Issue: Build fails
**Solution:**
```bash
make clean
make build-no-cache
```

### Issue: Database connection fails
**Solution:**
```bash
docker-compose logs postgres
docker-compose restart postgres
```

---

**InfraFlow AI - Verification Complete**

All systems ready for deployment!
