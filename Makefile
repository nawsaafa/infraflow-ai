# ============================================================================
# InfraFlow AI - Makefile
# ============================================================================
# Convenient commands for development and deployment
# Usage: make [command]
# ============================================================================

.PHONY: help setup install dev prod stop clean restart logs test lint format

# Default target
.DEFAULT_GOAL := help

# ============================================================================
# HELP
# ============================================================================
help: ## Show this help message
	@echo "InfraFlow AI - Available Commands"
	@echo "=================================="
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Setup & Installation

setup: ## Initial setup - copy .env.example to .env
	@echo "Setting up InfraFlow AI..."
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "✓ Created .env file from .env.example"; \
		echo "⚠ Please update .env with your configuration"; \
	else \
		echo "✓ .env file already exists"; \
	fi
	@chmod +x start.sh
	@echo "✓ Made start.sh executable"
	@echo "✓ Setup complete!"

install: setup ## Install dependencies for local development
	@echo "Installing backend dependencies..."
	cd backend && python -m venv venv && . venv/bin/activate && pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd frontend && npm install
	@echo "✓ Dependencies installed!"

##@ Development

dev: ## Start development environment
	@echo "Starting InfraFlow AI in development mode..."
	@./start.sh dev

dev-full: ## Start full development environment with all services
	@echo "Starting full development environment..."
	@./start.sh full

dev-tools: ## Start with development tools (pgAdmin, Redis Commander)
	@echo "Starting with development tools..."
	@./start.sh tools

##@ Production

prod: ## Start production environment
	@echo "Starting InfraFlow AI in production mode..."
	@./start.sh prod

build: ## Build Docker images
	@echo "Building Docker images..."
	docker-compose build

build-no-cache: ## Build Docker images without cache
	@echo "Building Docker images (no cache)..."
	docker-compose build --no-cache

##@ Service Management

stop: ## Stop all services
	@echo "Stopping all services..."
	@./start.sh stop

restart: ## Restart all services
	@echo "Restarting all services..."
	@./start.sh restart

clean: ## Stop and remove all containers, volumes, and networks
	@echo "Cleaning up..."
	@./start.sh clean

##@ Logs & Monitoring

logs: ## Show logs from all services
	@./start.sh logs

logs-backend: ## Show backend logs
	docker-compose logs -f backend

logs-frontend: ## Show frontend logs
	docker-compose logs -f frontend

logs-postgres: ## Show PostgreSQL logs
	docker-compose logs -f postgres

logs-redis: ## Show Redis logs
	docker-compose logs -f redis

##@ Database Operations

db-migrate: ## Run database migrations
	@echo "Running database migrations..."
	docker-compose exec backend alembic upgrade head

db-rollback: ## Rollback last database migration
	@echo "Rolling back last migration..."
	docker-compose exec backend alembic downgrade -1

db-shell: ## Open PostgreSQL shell
	docker-compose exec postgres psql -U infraflow_user -d infraflow_db

db-backup: ## Backup database
	@echo "Backing up database..."
	@mkdir -p backups
	docker-compose exec -T postgres pg_dump -U infraflow_user infraflow_db > backups/backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "✓ Database backed up to backups/"

db-restore: ## Restore database from backup (requires BACKUP_FILE variable)
	@if [ -z "$(BACKUP_FILE)" ]; then \
		echo "Error: Please specify BACKUP_FILE=path/to/backup.sql"; \
		exit 1; \
	fi
	@echo "Restoring database from $(BACKUP_FILE)..."
	docker-compose exec -T postgres psql -U infraflow_user -d infraflow_db < $(BACKUP_FILE)
	@echo "✓ Database restored!"

##@ Testing

test: ## Run all tests
	@echo "Running tests..."
	@make test-backend
	@make test-frontend

test-backend: ## Run backend tests
	@echo "Running backend tests..."
	cd backend && . venv/bin/activate && pytest tests/ -v

test-frontend: ## Run frontend tests
	@echo "Running frontend tests..."
	cd frontend && npm test

test-coverage: ## Run tests with coverage
	@echo "Running tests with coverage..."
	cd backend && . venv/bin/activate && pytest tests/ -v --cov=. --cov-report=html

##@ Code Quality

lint: ## Run linters
	@echo "Running linters..."
	@make lint-backend
	@make lint-frontend

lint-backend: ## Lint backend code
	@echo "Linting backend..."
	cd backend && . venv/bin/activate && flake8 . && mypy .

lint-frontend: ## Lint frontend code
	@echo "Linting frontend..."
	cd frontend && npm run lint

format: ## Format code
	@echo "Formatting code..."
	@make format-backend
	@make format-frontend

format-backend: ## Format backend code with black
	@echo "Formatting backend..."
	cd backend && . venv/bin/activate && black .

format-frontend: ## Format frontend code with prettier
	@echo "Formatting frontend..."
	cd frontend && npx prettier --write .

##@ Docker Operations

ps: ## Show running containers
	docker-compose ps

stats: ## Show container resource usage
	docker stats

shell-backend: ## Open shell in backend container
	docker-compose exec backend /bin/bash

shell-frontend: ## Open shell in frontend container
	docker-compose exec frontend /bin/sh

shell-postgres: ## Open shell in PostgreSQL container
	docker-compose exec postgres /bin/bash

##@ Security

security-scan: ## Run security scans
	@echo "Running security scans..."
	cd backend && . venv/bin/activate && safety check
	cd frontend && npm audit

generate-secret: ## Generate a secure random secret
	@openssl rand -hex 32

##@ Utilities

health: ## Check health of all services
	@echo "Checking service health..."
	@echo "Backend: $$(curl -s http://localhost:8000/health | jq -r '.status // "unreachable"')"
	@echo "Frontend: $$(curl -s http://localhost:3000 > /dev/null 2>&1 && echo 'healthy' || echo 'unreachable')"
	@echo "PostgreSQL: $$(docker-compose exec -T postgres pg_isready -U infraflow_user | grep -q 'accepting' && echo 'healthy' || echo 'unhealthy')"
	@echo "Redis: $$(docker-compose exec -T redis redis-cli ping | grep -q 'PONG' && echo 'healthy' || echo 'unhealthy')"

status: ## Show detailed status of all services
	@./start.sh dev > /dev/null 2>&1 || true
	@echo ""
	@echo "Service Status:"
	@docker-compose ps

ports: ## Show exposed ports
	@echo "Exposed Ports:"
	@echo "  Frontend:        http://localhost:3000"
	@echo "  Backend API:     http://localhost:8000"
	@echo "  API Docs:        http://localhost:8000/api/docs"
	@echo "  PostgreSQL:      localhost:5432"
	@echo "  Redis:           localhost:6379"
	@echo "  pgAdmin:         http://localhost:5050  (with dev-tools profile)"
	@echo "  Redis Commander: http://localhost:8081  (with dev-tools profile)"
	@echo "  n8n:             http://localhost:5678  (with automation profile)"

##@ Documentation

docs: ## Generate documentation
	@echo "Documentation is available in:"
	@echo "  README.md         - Main documentation"
	@echo "  DEPLOYMENT.md     - Deployment guide"
	@echo "  API Docs:         http://localhost:8000/api/docs (when running)"

##@ Git Operations

git-init: ## Initialize git repository
	@if [ ! -d .git ]; then \
		git init; \
		git add .; \
		git commit -m "Initial commit - InfraFlow AI Platform"; \
		echo "✓ Git repository initialized"; \
	else \
		echo "✓ Git repository already exists"; \
	fi

##@ Quick Actions

quick-start: setup dev ## Quick start - setup and run development environment

quick-test: install test ## Install dependencies and run tests

quick-deploy: build prod ## Build and deploy to production

# ============================================================================
# END OF MAKEFILE
# ============================================================================
