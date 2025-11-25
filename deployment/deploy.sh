#!/bin/bash

# Simplified Cloud Run Deployment Script for Cabana Project
# Leverages environment files and Docker's production stage
# Usage: ./deploy.sh [PROJECT_ID] [REGION] [ENV_TYPE]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ID=${1:-"your-project-id"}
REGION=${2:-"us-central1"}
ENV_TYPE=${3:-"prod"}
SERVICE_NAME="cabana-project"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

print_usage() {
    echo -e "${BLUE}Cloud Run Deployment Script${NC}"
    echo ""
    echo "Usage: $0 [PROJECT_ID] [REGION] [ENV_TYPE]"
    echo ""
    echo "Parameters:"
    echo "  PROJECT_ID   - Your Google Cloud Project ID"
    echo "  REGION       - Deployment region (default: us-central1)"
    echo "  ENV_TYPE     - Environment type: prod or staging (default: prod)"
    echo ""
    echo "Examples:"
    echo "  ./deploy.sh my-project                    # Deploy to production"
    echo "  ./deploy.sh my-project us-west1          # Deploy to different region"
    echo "  ./deploy.sh my-project us-central1 prod  # Explicit production deploy"
}

validate_prerequisites() {
    echo -e "${BLUE}🔍 Validating prerequisites...${NC}"
    
    # Check if gcloud is installed
    if ! command -v gcloud &> /dev/null; then
        echo -e "${RED}❌ Error: gcloud CLI is not installed${NC}"
        echo "Please install it from: https://cloud.google.com/sdk/docs/install"
        exit 1
    fi
    
    # Check if environment files exist
    local env_file="env/.env.$ENV_TYPE"
    local secrets_file="env/.env.secrets.$ENV_TYPE"
    
    if [[ ! -f "$env_file" ]]; then
        echo -e "${RED}❌ Missing: $env_file${NC}"
        exit 1
    fi
    
    if [[ ! -f "$secrets_file" ]]; then
        echo -e "${RED}❌ Missing: $secrets_file${NC}"
        echo -e "${YELLOW}💡 Create from example: cp env/.env.secrets.$ENV_TYPE.example $secrets_file${NC}"
        exit 1
    fi
    
    # Check if user is authenticated
    if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | head -1 > /dev/null; then
        echo -e "${RED}❌ Not authenticated with gcloud${NC}"
        echo "Please run: gcloud auth login"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Prerequisites validated${NC}"
}

prepare_env_vars() {
    echo -e "${BLUE}🔐 Preparing environment variables...${NC}"
    
    local env_file="env/.env.$ENV_TYPE"
    local secrets_file="env/.env.secrets.$ENV_TYPE"
    
    # Check if both files exist
    if [[ ! -f "$env_file" ]]; then
        echo -e "${RED}❌ Environment file not found: $env_file${NC}"
        return 1
    fi
    
    if [[ ! -f "$secrets_file" ]]; then
        echo -e "${RED}❌ Secrets file not found: $secrets_file${NC}"
        return 1
    fi
    
    echo -e "${YELLOW}📄 Reading environment from: $env_file${NC}"
    echo -e "${YELLOW}🔐 Reading secrets from: $secrets_file${NC}"
    
    # Function to process env file and extract key=value pairs
    process_env_file() {
        local file="$1"
        while IFS='=' read -r key value || [[ -n "$key" ]]; do
            # Skip empty lines and comments
            [[ -z "$key" || "$key" =~ ^[[:space:]]*# ]] && continue
            
            # Remove leading/trailing whitespace
            key=$(echo "$key" | xargs)
            value=$(echo "$value" | xargs)
            
            # Remove quotes from value if present
            value=$(echo "$value" | sed 's/^["'\'']\|["'\'']$//g')
            
            # Add to env vars string with custom delimiter to handle special characters
            if [[ -n "$ENV_VARS" ]]; then
                ENV_VARS="$ENV_VARS|$key=$value"
            else
                ENV_VARS="$key=$value"
            fi
        done < <(grep -v '^[[:space:]]*$' "$file")
    }
    
    # Build environment variables string from both files
    ENV_VARS=""
    
    # Process regular environment file first
    process_env_file "$env_file"
    
    # Process secrets file
    process_env_file "$secrets_file"
    
    echo -e "${GREEN}✅ Environment variables prepared from both files${NC}"
}



setup_gcloud() {
    echo -e "${BLUE}📋 Setting up Google Cloud...${NC}"
    
    # Set the project
    gcloud config set project $PROJECT_ID
    
    # Enable required APIs
    echo -e "${YELLOW}🔧 Enabling required APIs...${NC}"
    gcloud services enable cloudbuild.googleapis.com
    gcloud services enable run.googleapis.com
    gcloud services enable containerregistry.googleapis.com
    gcloud services enable secretmanager.googleapis.com
    
    echo -e "${GREEN}✅ Google Cloud setup completed${NC}"
}



build_and_deploy() {
    echo -e "${BLUE}🏗️  Building and deploying...${NC}"
    
    # Build Docker image using production stage
    echo -e "${YELLOW}Building production Docker image...${NC}"
    gcloud builds submit --config deployment/cloudbuild.yaml --substitutions="_DOCKER_TARGET=production,_IMAGE_NAME=$IMAGE_NAME" .
    
    # Prepare environment variables from secrets file
    prepare_env_vars
    
    echo -e "${YELLOW}🚀 Deploying to Cloud Run with environment variables...${NC}"
    echo -e "${BLUE}Using custom delimiter to handle special characters in values${NC}"
    
    # Use custom delimiter syntax to handle commas and special characters
    # ^:^ means use ':' as delimiter instead of ','
    gcloud run deploy $SERVICE_NAME \
        --image $IMAGE_NAME \
        --region $REGION \
        --platform managed \
        --allow-unauthenticated \
        --set-env-vars "^|^$ENV_VARS" \
        --memory 1Gi \
        --cpu 1000m \
        --concurrency 100 \
        --timeout 300 \
        --port 8080
    
    echo -e "${GREEN}✅ Deployment completed successfully!${NC}"
}

show_results() {
    # Get the service URL
    SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format 'value(status.url)')
    
    echo ""
    echo -e "${GREEN}🎉 Deployment Summary${NC}"
    echo "=========================="
    echo -e "🌐 Service URL: ${BLUE}$SERVICE_URL${NC}"
    echo -e "🏥 Health check: ${BLUE}$SERVICE_URL/health/${NC}"
    echo -e "📍 Region: $REGION"
    echo -e "🏷️  Environment: $ENV_TYPE"
    echo ""
    echo -e "${YELLOW}📝 Next steps:${NC}"
    echo "1. Test the health endpoint to verify deployment"
    echo "2. Verify secrets are accessible from Secret Manager"
    echo "3. Set up monitoring and logging"
    echo "4. Configure custom domain if needed"
    echo "5. Set up CI/CD pipeline for automated deployments"
}

# Main script logic
if [[ "$PROJECT_ID" == "your-project-id" ]] || [[ "$1" == "--help" ]] || [[ "$1" == "-h" ]]; then
    print_usage
    exit 1
fi

echo -e "${BLUE}🚀 Deploying $SERVICE_NAME to Cloud Run${NC}"
echo "Project ID: $PROJECT_ID"
echo "Region: $REGION"  
echo "Environment: $ENV_TYPE"
echo "Image: $IMAGE_NAME"
echo ""

validate_prerequisites
setup_gcloud
build_and_deploy
show_results