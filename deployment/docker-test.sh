#!/bin/bash

# Simplified Docker Testing Script for Cabana Project
# Leverages Docker Compose and multi-stage Dockerfile
# Usage: ./docker-test.sh [dev|prod|test|stop|clean|logs|health|shell]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_usage() {
    echo -e "${BLUE}Cabana Docker Testing Script${NC}"
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  dev      - Start development environment (with live reload)"
    echo "  prod     - Start production-like environment for testing"
    echo "  test     - Run full test suite (build + health checks)"
    echo "  stop     - Stop all running services"
    echo "  clean    - Stop and remove all containers, images, and volumes"
    echo "  logs     - Show logs for all services"
    echo "  health   - Test health endpoints"
    echo "  shell    - Open interactive shell in development container"
    echo ""
    echo "Examples:"
    echo "  ./docker-test.sh dev     # Start development with live reload"
    echo "  ./docker-test.sh prod    # Test production-like deployment"
    echo "  ./docker-test.sh test    # Full validation suite"
}

validate_environment() {
    echo -e "${YELLOW}🔍 Validating environment files...${NC}"
    
    local env_type=$1
    local env_file="env/.env.$env_type"
    local secrets_file="env/.env.secrets.$env_type"
    
    if [[ ! -f "$env_file" ]]; then
        echo -e "${RED}❌ Missing: $env_file${NC}"
        return 1
    fi
    
    if [[ ! -f "$secrets_file" ]]; then
        echo -e "${RED}❌ Missing: $secrets_file${NC}"
        echo -e "${YELLOW}💡 Create from example: cp env/.env.secrets.$env_type.example $secrets_file${NC}"
        return 1
    fi
    
    echo -e "${GREEN}✅ Environment files validated${NC}"
}

start_dev() {
    echo -e "${BLUE}🚀 Starting Development Environment${NC}"
    
    validate_environment "dev" || exit 1
    
    echo -e "${YELLOW}Building and starting development services...${NC}"
    cd deployment
    docker-compose up --build web
}

start_prod() {
    echo -e "${BLUE}🚀 Starting Production-like Environment${NC}"
    
    validate_environment "prod" || exit 1
    
    echo -e "${YELLOW}Building and starting production-like services...${NC}"
    cd deployment
    docker-compose up --build web-prod
}

run_tests() {
    echo -e "${BLUE}🧪 Running Full Test Suite${NC}"
    
    # Validate both environments
    validate_environment "dev" || exit 1
    validate_environment "prod" || exit 1
    
    echo -e "${YELLOW}Building images...${NC}"
    cd deployment
    docker-compose build
    
    echo -e "${YELLOW}Testing development environment...${NC}"
    docker-compose up -d web
    sleep 10
    test_health "8080" "development"
    
    echo -e "${YELLOW}Testing production-like environment...${NC}"
    docker-compose up -d web-prod
    sleep 10
    test_health "8081" "production"
    
    echo -e "${GREEN}✅ All tests passed!${NC}"
    stop_all
}

test_health() {
    local port=${1:-8080}
    local env_name=${2:-"environment"}
    
    echo -e "${YELLOW}🏥 Testing health endpoint for $env_name (port $port)...${NC}"
    
    # Wait for service to be ready
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s http://localhost:$port/health/ > /dev/null; then
            local response=$(curl -s http://localhost:$port/health/)
            echo -e "${GREEN}✅ Health check passed for $env_name!${NC}"
            echo -e "${GREEN}Response: $response${NC}"
            
            # Test main page
            if curl -s http://localhost:$port/ > /dev/null; then
                echo -e "${GREEN}✅ Main page accessible!${NC}"
                return 0
            else
                echo -e "${RED}❌ Main page not accessible${NC}"
                return 1
            fi
        fi
        
        echo -e "${YELLOW}⏳ Attempt $attempt/$max_attempts - waiting for service...${NC}"
        sleep 2
        ((attempt++))
    done
    
    echo -e "${RED}❌ Health check failed for $env_name after $max_attempts attempts${NC}"
    show_logs
    return 1
}

stop_all() {
    echo -e "${YELLOW}🛑 Stopping all services...${NC}"
    cd deployment
    docker-compose down
    echo -e "${GREEN}✅ All services stopped${NC}"
}

clean_all() {
    echo -e "${YELLOW}🧹 Cleaning up everything...${NC}"
    cd deployment
    docker-compose down --volumes --remove-orphans
    docker-compose down --rmi all --volumes --remove-orphans 2>/dev/null || true
    docker system prune -f
    echo -e "${GREEN}✅ Cleanup completed${NC}"
}

show_logs() {
    echo -e "${YELLOW}📋 Showing service logs...${NC}"
    cd deployment
    docker-compose logs --tail=50
}

open_shell() {
    echo -e "${YELLOW}🐚 Opening shell in development container...${NC}"
    cd deployment
    docker-compose exec web bash || {
        echo -e "${RED}❌ Development container not running. Start with: ./docker-test.sh dev${NC}"
        exit 1
    }
}

# Main script logic
case "${1:-}" in
    dev)
        start_dev
        ;;
    prod)
        start_prod
        ;;
    test)
        run_tests
        ;;
    stop)
        stop_all
        ;;
    clean)
        clean_all
        ;;
    logs)
        show_logs
        ;;
    health)
        test_health "${2:-8080}" "${3:-environment}"
        ;;
    shell)
        open_shell
        ;;
    *)
        print_usage
        exit 1
        ;;
esac