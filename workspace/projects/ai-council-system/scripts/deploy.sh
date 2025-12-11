#!/bin/bash
# AI Council System - Automated Deployment Script
#
# Supports multiple deployment modes:
# - Development (local)
# - Docker (containerized)
# - Production (systemd + docker)
# - Kubernetes (k8s cluster)
#
# Usage: ./scripts/deploy.sh [mode] [options]

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="ai-council-system"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEPLOY_MODE="${1:-development}"

# Functions
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

check_requirements() {
    log_info "Checking requirements..."

    # Check Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 not found!"
        exit 1
    fi

    # Check Docker if needed
    if [ "$DEPLOY_MODE" != "development" ]; then
        if ! command -v docker &> /dev/null; then
            log_error "Docker not found! Install Docker first."
            exit 1
        fi

        if ! command -v docker-compose &> /dev/null; then
            log_error "Docker Compose not found! Install Docker Compose first."
            exit 1
        fi
    fi

    log_success "Requirements check passed"
}

create_directories() {
    log_info "Creating necessary directories..."

    mkdir -p "$PROJECT_DIR/recordings"
    mkdir -p "$PROJECT_DIR/voice_cache"
    mkdir -p "$PROJECT_DIR/avatar_cache"
    mkdir -p "$PROJECT_DIR/background_cache"
    mkdir -p "$PROJECT_DIR/logs"
    mkdir -p "$PROJECT_DIR/data"

    log_success "Directories created"
}

setup_environment() {
    log_info "Setting up environment..."

    if [ ! -f "$PROJECT_DIR/.env" ]; then
        if [ -f "$PROJECT_DIR/.env.example" ]; then
            cp "$PROJECT_DIR/.env.example" "$PROJECT_DIR/.env"
            log_warning ".env file created from template"
            log_warning "Please edit .env and add your API keys!"
        else
            log_error ".env.example not found!"
            exit 1
        fi
    else
        log_info ".env file already exists"
    fi
}

deploy_development() {
    log_info "Deploying in DEVELOPMENT mode..."

    # Install dependencies
    log_info "Installing Python dependencies..."
    pip install -q --upgrade pip
    pip install -q -r "$PROJECT_DIR/requirements.txt"

    log_success "Development deployment complete!"
    log_info ""
    log_info "To start the system:"
    log_info "  ./quick-start.sh"
    log_info "  OR"
    log_info "  python examples/demo_debate.py"
}

deploy_docker() {
    log_info "Deploying with DOCKER..."

    # Build images
    log_info "Building Docker images..."
    docker-compose -f "$PROJECT_DIR/docker-compose.yml" build

    # Start services
    log_info "Starting Docker services..."
    docker-compose -f "$PROJECT_DIR/docker-compose.yml" up -d

    log_success "Docker deployment complete!"
    log_info ""
    log_info "Services running:"
    docker-compose -f "$PROJECT_DIR/docker-compose.yml" ps
    log_info ""
    log_info "To stop services:"
    log_info "  docker-compose down"
}

deploy_production() {
    log_info "Deploying in PRODUCTION mode..."

    # Check if running as root for systemd
    if [ "$EUID" -ne 0 ] && [ "$2" == "--systemd" ]; then
        log_error "Production deployment with systemd requires root!"
        log_info "Run with: sudo ./scripts/deploy.sh production --systemd"
        exit 1
    fi

    # Build production images
    log_info "Building production Docker images..."
    docker-compose -f "$PROJECT_DIR/deployment/docker-compose.production.yml" build

    # Start production services
    log_info "Starting production services..."
    docker-compose -f "$PROJECT_DIR/deployment/docker-compose.production.yml" up -d

    # Install systemd service if requested
    if [ "$2" == "--systemd" ]; then
        log_info "Installing systemd service..."

        cp "$PROJECT_DIR/deployment/ai-council.service" /etc/systemd/system/
        systemctl daemon-reload
        systemctl enable ai-council
        systemctl start ai-council

        log_success "Systemd service installed and started"
    fi

    log_success "Production deployment complete!"
    log_info ""
    log_info "Access points:"
    log_info "  API: http://localhost:8000"
    log_info "  Grafana: http://localhost:3000 (admin/admin)"
    log_info "  Prometheus: http://localhost:9090"
    log_info ""
    log_info "To check status:"
    log_info "  docker-compose -f deployment/docker-compose.production.yml ps"
    if [ "$2" == "--systemd" ]; then
        log_info "  systemctl status ai-council"
    fi
}

deploy_kubernetes() {
    log_info "Deploying to KUBERNETES..."

    log_warning "Kubernetes deployment not fully implemented yet"
    log_info "Manual steps required - see deployment/kubernetes/ directory"

    exit 1
}

run_health_check() {
    log_info "Running health check..."

    # Wait for services to start
    sleep 5

    # Check if API is responding
    if command -v curl &> /dev/null; then
        if curl -sf http://localhost:8000/health > /dev/null 2>&1; then
            log_success "Health check passed!"
        else
            log_warning "Health check failed - services may still be starting"
        fi
    else
        log_warning "curl not found - skipping health check"
    fi
}

print_usage() {
    echo "Usage: $0 [mode] [options]"
    echo ""
    echo "Modes:"
    echo "  development        Local development setup"
    echo "  docker             Docker containerized deployment"
    echo "  production         Production deployment with Docker Compose"
    echo "  kubernetes         Kubernetes cluster deployment"
    echo ""
    echo "Options:"
    echo "  --systemd          Install systemd service (production mode only)"
    echo "  --skip-health      Skip health check after deployment"
    echo ""
    echo "Examples:"
    echo "  $0 development"
    echo "  $0 docker"
    echo "  $0 production --systemd"
    echo ""
}

# Main execution
main() {
    clear

    echo "=================================="
    echo "  AI Council System Deployment"
    echo "  Mode: $DEPLOY_MODE"
    echo "=================================="
    echo ""

    # Validate mode
    case "$DEPLOY_MODE" in
        development|docker|production|kubernetes)
            ;;
        help|--help|-h)
            print_usage
            exit 0
            ;;
        *)
            log_error "Invalid deployment mode: $DEPLOY_MODE"
            echo ""
            print_usage
            exit 1
            ;;
    esac

    # Run deployment steps
    check_requirements
    create_directories
    setup_environment

    # Deploy based on mode
    case "$DEPLOY_MODE" in
        development)
            deploy_development
            ;;
        docker)
            deploy_docker
            ;;
        production)
            deploy_production
            ;;
        kubernetes)
            deploy_kubernetes
            ;;
    esac

    # Health check (unless skipped)
    if [ "$2" != "--skip-health" ] && [ "$DEPLOY_MODE" != "development" ]; then
        run_health_check
    fi

    echo ""
    log_success "Deployment complete! 🚀"
    echo ""
}

# Run main
main "$@"
