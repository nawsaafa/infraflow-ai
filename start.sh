#!/bin/bash

# ============================================================================
# InfraFlow AI - One-Command Startup Script
# ============================================================================
# This script handles the complete setup and launch of the InfraFlow AI platform
# Usage: ./start.sh [mode] [options]
#
# Modes:
#   dev          - Start in development mode (default)
#   prod         - Start in production mode
#   tools        - Start with development tools (pgAdmin, Redis Commander)
#   full         - Start everything including n8n and Weaviate
#   stop         - Stop all containers
#   clean        - Stop and remove all containers, volumes, and networks
#   logs         - Show logs from all containers
#   restart      - Restart all containers
# ============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${SCRIPT_DIR}/.env"
ENV_EXAMPLE="${SCRIPT_DIR}/.env.example"

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

print_banner() {
    echo -e "${BLUE}"
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║                                                               ║"
    echo "║                    INFRAFLOW AI PLATFORM                      ║"
    echo "║          Infrastructure Finance Intelligence Platform         ║"
    echo "║                                                               ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# ============================================================================
# PREREQUISITE CHECKS
# ============================================================================

check_prerequisites() {
    log_info "Checking prerequisites..."

    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker first."
        log_info "Visit: https://docs.docker.com/get-docker/"
        exit 1
    fi

    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        log_error "Docker Compose is not installed. Please install Docker Compose first."
        log_info "Visit: https://docs.docker.com/compose/install/"
        exit 1
    fi

    # Check if Docker daemon is running
    if ! docker info &> /dev/null; then
        log_error "Docker daemon is not running. Please start Docker first."
        exit 1
    fi

    log_success "All prerequisites met!"
}

# ============================================================================
# ENVIRONMENT SETUP
# ============================================================================

setup_environment() {
    log_info "Setting up environment..."

    # Check if .env exists
    if [ ! -f "$ENV_FILE" ]; then
        log_warning ".env file not found. Creating from .env.example..."

        if [ ! -f "$ENV_EXAMPLE" ]; then
            log_error ".env.example not found!"
            exit 1
        fi

        cp "$ENV_EXAMPLE" "$ENV_FILE"
        log_success ".env file created!"
        log_warning "Please update .env with your actual configuration values."
        log_info "Opening .env file for editing..."

        # Try to open with default editor
        if [ -n "$EDITOR" ]; then
            $EDITOR "$ENV_FILE"
        else
            log_info "Edit .env manually: $ENV_FILE"
        fi

        read -p "Press Enter when you've updated .env file..."
    else
        log_success ".env file found!"
    fi

    # Generate secrets if they don't exist
    generate_secrets
}

generate_secrets() {
    log_info "Checking for required secrets..."

    # Check if secrets need to be generated
    if grep -q "your-.*-here\|change_me" "$ENV_FILE"; then
        log_warning "Found placeholder values in .env file."
        read -p "Generate random secrets for development? (y/N): " -n 1 -r
        echo

        if [[ $REPLY =~ ^[Yy]$ ]]; then
            # Generate JWT_SECRET
            if grep -q "your-jwt-secret-key-here" "$ENV_FILE"; then
                JWT_SECRET=$(openssl rand -hex 32)
                sed -i.bak "s/your-jwt-secret-key-here/$JWT_SECRET/" "$ENV_FILE"
                log_success "Generated JWT_SECRET"
            fi

            # Generate WEBHOOK_SECRET
            if grep -q "your-webhook-secret-here" "$ENV_FILE"; then
                WEBHOOK_SECRET=$(openssl rand -hex 32)
                sed -i.bak "s/your-webhook-secret-here/$WEBHOOK_SECRET/" "$ENV_FILE"
                log_success "Generated WEBHOOK_SECRET"
            fi

            # Generate RATE_LIMIT_SECRET
            if grep -q "your-rate-limit-secret-here" "$ENV_FILE"; then
                RATE_LIMIT_SECRET=$(openssl rand -hex 32)
                sed -i.bak "s/your-rate-limit-secret-here/$RATE_LIMIT_SECRET/" "$ENV_FILE"
                log_success "Generated RATE_LIMIT_SECRET"
            fi

            # Remove backup file
            rm -f "$ENV_FILE.bak"
        fi
    fi
}

# ============================================================================
# DOCKER OPERATIONS
# ============================================================================

start_services() {
    local MODE=$1
    local COMPOSE_CMD="docker-compose"

    # Check if using docker compose v2
    if docker compose version &> /dev/null; then
        COMPOSE_CMD="docker compose"
    fi

    cd "$SCRIPT_DIR"

    case $MODE in
        dev)
            log_info "Starting InfraFlow AI in DEVELOPMENT mode..."
            $COMPOSE_CMD up -d postgres redis backend frontend
            ;;
        prod)
            log_info "Starting InfraFlow AI in PRODUCTION mode..."
            BUILD_TARGET=production $COMPOSE_CMD up -d postgres redis backend frontend
            ;;
        tools)
            log_info "Starting with DEVELOPMENT TOOLS..."
            $COMPOSE_CMD --profile dev-tools up -d
            ;;
        full)
            log_info "Starting FULL STACK (including n8n and Weaviate)..."
            $COMPOSE_CMD --profile dev-tools --profile automation --profile vector-db up -d
            ;;
        *)
            log_error "Invalid mode: $MODE"
            show_usage
            exit 1
            ;;
    esac

    # Wait for services to be ready
    wait_for_services

    # Show status
    show_status
}

stop_services() {
    log_info "Stopping all services..."
    docker-compose down
    log_success "All services stopped!"
}

clean_environment() {
    log_warning "This will remove all containers, volumes, and networks!"
    read -p "Are you sure? (y/N): " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "Cleaning up..."
        docker-compose down -v --remove-orphans
        log_success "Environment cleaned!"
    else
        log_info "Cleanup cancelled."
    fi
}

restart_services() {
    log_info "Restarting services..."
    docker-compose restart
    wait_for_services
    show_status
}

show_logs() {
    log_info "Showing logs (Ctrl+C to exit)..."
    docker-compose logs -f
}

# ============================================================================
# SERVICE HEALTH CHECKS
# ============================================================================

wait_for_services() {
    log_info "Waiting for services to be ready..."

    # Wait for PostgreSQL
    log_info "Waiting for PostgreSQL..."
    timeout 60 bash -c 'until docker-compose exec -T postgres pg_isready -U infraflow_user > /dev/null 2>&1; do sleep 2; done' || {
        log_error "PostgreSQL failed to start"
        exit 1
    }
    log_success "PostgreSQL is ready!"

    # Wait for Redis
    log_info "Waiting for Redis..."
    timeout 60 bash -c 'until docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; do sleep 2; done' || {
        log_error "Redis failed to start"
        exit 1
    }
    log_success "Redis is ready!"

    # Wait for Backend
    log_info "Waiting for Backend API..."
    timeout 120 bash -c 'until curl -sf http://localhost:8000/health > /dev/null 2>&1; do sleep 3; done' || {
        log_error "Backend API failed to start"
        log_info "Check logs with: docker-compose logs backend"
        exit 1
    }
    log_success "Backend API is ready!"

    # Wait for Frontend
    log_info "Waiting for Frontend..."
    timeout 120 bash -c 'until curl -sf http://localhost:3000 > /dev/null 2>&1; do sleep 3; done' || {
        log_error "Frontend failed to start"
        log_info "Check logs with: docker-compose logs frontend"
        exit 1
    }
    log_success "Frontend is ready!"

    log_success "All services are running!"
}

# ============================================================================
# STATUS & INFORMATION
# ============================================================================

show_status() {
    echo ""
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║               INFRAFLOW AI IS NOW RUNNING!                    ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BLUE}Services:${NC}"
    echo -e "  Frontend:           ${GREEN}http://localhost:3000${NC}"
    echo -e "  Backend API:        ${GREEN}http://localhost:8000${NC}"
    echo -e "  API Documentation:  ${GREEN}http://localhost:8000/api/docs${NC}"
    echo -e "  PostgreSQL:         ${GREEN}localhost:5432${NC}"
    echo -e "  Redis:              ${GREEN}localhost:6379${NC}"
    echo ""

    # Check if optional services are running
    if docker-compose ps | grep -q "infraflow-pgadmin"; then
        echo -e "  pgAdmin:            ${GREEN}http://localhost:5050${NC}"
    fi

    if docker-compose ps | grep -q "infraflow-redis-commander"; then
        echo -e "  Redis Commander:    ${GREEN}http://localhost:8081${NC}"
    fi

    if docker-compose ps | grep -q "infraflow-n8n"; then
        echo -e "  n8n Automation:     ${GREEN}http://localhost:5678${NC}"
    fi

    if docker-compose ps | grep -q "infraflow-weaviate"; then
        echo -e "  Weaviate Vector DB: ${GREEN}http://localhost:8080${NC}"
    fi

    echo ""
    echo -e "${BLUE}Useful Commands:${NC}"
    echo -e "  View logs:          ${YELLOW}./start.sh logs${NC}"
    echo -e "  Stop services:      ${YELLOW}./start.sh stop${NC}"
    echo -e "  Restart services:   ${YELLOW}./start.sh restart${NC}"
    echo -e "  Clean up:           ${YELLOW}./start.sh clean${NC}"
    echo ""
}

show_usage() {
    echo "Usage: ./start.sh [mode] [options]"
    echo ""
    echo "Modes:"
    echo "  dev          - Start in development mode (default)"
    echo "  prod         - Start in production mode"
    echo "  tools        - Start with development tools (pgAdmin, Redis Commander)"
    echo "  full         - Start everything including n8n and Weaviate"
    echo "  stop         - Stop all containers"
    echo "  clean        - Stop and remove all containers, volumes, and networks"
    echo "  logs         - Show logs from all containers"
    echo "  restart      - Restart all containers"
    echo ""
    echo "Examples:"
    echo "  ./start.sh              # Start in development mode"
    echo "  ./start.sh dev          # Start in development mode"
    echo "  ./start.sh prod         # Start in production mode"
    echo "  ./start.sh tools        # Start with development tools"
    echo "  ./start.sh full         # Start full stack"
    echo "  ./start.sh logs         # View logs"
    echo ""
}

# ============================================================================
# MAIN SCRIPT
# ============================================================================

main() {
    print_banner

    # Parse command line arguments
    MODE=${1:-dev}

    case $MODE in
        dev|prod|tools|full)
            check_prerequisites
            setup_environment
            start_services "$MODE"
            ;;
        stop)
            stop_services
            ;;
        clean)
            clean_environment
            ;;
        logs)
            show_logs
            ;;
        restart)
            restart_services
            ;;
        help|--help|-h)
            show_usage
            ;;
        *)
            log_error "Unknown command: $MODE"
            show_usage
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
