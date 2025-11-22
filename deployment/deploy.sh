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

update_django_secrets() {
    echo -e "${BLUE}🔐 Updating Django secrets in Secret Manager...${NC}"
    
    local secrets_file="env/.env.secrets.$ENV_TYPE"
    local secret_name="django-secrets"
    
    # Check if secrets file exists
    if [[ ! -f "$secrets_file" ]]; then
        echo -e "${RED}❌ Secrets file not found: $secrets_file${NC}"
        return 1
    fi
    
    # Create a temporary JSON file for the secrets
    local temp_secrets_file=$(mktemp)
    echo "{" > "$temp_secrets_file"
    
    # Convert .env format to JSON format
    local first_entry=true
    while IFS='=' read -r key value || [[ -n "$key" ]]; do
        # Skip empty lines and comments
        [[ -z "$key" || "$key" =~ ^[[:space:]]*# ]] && continue
        
        # Remove leading/trailing whitespace
        key=$(echo "$key" | xargs)
        value=$(echo "$value" | xargs)
        
        # Remove quotes from value if present
        value=$(echo "$value" | sed 's/^["'\'']\|["'\'']$//g')
        
        # Add comma if not first entry
        if [[ "$first_entry" == "false" ]]; then
            echo "," >> "$temp_secrets_file"
        fi
        first_entry=false
        
        # Escape quotes in value and add to JSON
        value=$(echo "$value" | sed 's/"/\\"/g')
        echo -n "  \"$key\": \"$value\"" >> "$temp_secrets_file"
        
    done < <(grep -v '^[[:space:]]*$' "$secrets_file")
    
    echo "" >> "$temp_secrets_file"
    echo "}" >> "$temp_secrets_file"
    
    echo -e "${YELLOW}📄 Secrets JSON content:${NC}"
    cat "$temp_secrets_file"
    echo ""
    
    # Check if secret already exists
    if gcloud secrets describe "$secret_name" --project="$PROJECT_ID" &>/dev/null; then
        echo -e "${YELLOW}🔄 Updating existing secret: $secret_name${NC}"
        gcloud secrets versions add "$secret_name" --data-file="$temp_secrets_file" --project="$PROJECT_ID"
    else
        echo -e "${YELLOW}🆕 Creating new secret: $secret_name${NC}"
        gcloud secrets create "$secret_name" --data-file="$temp_secrets_file" --project="$PROJECT_ID"
    fi
    
    # Clean up temporary file
    rm "$temp_secrets_file"
    
    echo -e "${GREEN}✅ Django secrets updated successfully${NC}"
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

update_yaml_with_secrets() {
    echo -e "${BLUE}🔐 Updating YAML with secrets from environment file...${NC}"
    
    local secrets_file="env/.env.secrets.$ENV_TYPE"
    local yaml_file="deployment/cloudrun-service.yaml"
    
    if [[ ! -f "$secrets_file" ]]; then
        echo -e "${YELLOW}⚠️  Secrets file not found: $secrets_file${NC}"
        echo -e "${YELLOW}Using existing YAML configuration${NC}"
        return 0
    fi
    
    echo -e "${YELLOW}📄 Reading secrets from: $secrets_file${NC}"
    
    # Create a backup of the original YAML
    cp "$yaml_file" "$yaml_file.backup"
    
    # Generate secret environment variables
    local secret_vars=""
    while IFS='=' read -r key value || [[ -n "$key" ]]; do
        # Skip empty lines and comments
        [[ -z "$key" || "$key" =~ ^[[:space:]]*# ]] && continue
        
        # Remove leading/trailing whitespace
        key=$(echo "$key" | xargs)
        
        # Add secret reference
        secret_vars+="            - name: $key
              valueFrom:
                secretKeyRef:
                  name: django-secrets
                  key: $key
"
    done < <(grep -v '^[[:space:]]*$' "$secrets_file")
    
    # Create a temporary file with the updated content
    local temp_file=$(mktemp)
    
    # Read the YAML file and replace the secrets section
    awk -v secrets="$secret_vars" -v secrets_file="$secrets_file" '
    /^          env:/ {
        print $0
        print "            # All secrets from Secret Manager - auto-generated from " secrets_file
        print secrets
        # Skip until we find the non-secret environment variables comment
        while (getline > 0 && !/# Non-secret environment variables/) {
            continue
        }
        print "            # Non-secret environment variables from .env files"
        next
    }
    /# All secrets from Secret Manager/,/# Non-secret environment variables/ {
        next
    }
    { print }
    ' "$yaml_file" > "$temp_file"
    
    # Replace the original file
    mv "$temp_file" "$yaml_file"
    
    local secret_count=$(echo "$secret_vars" | grep -c "name:" || echo "0")
    echo -e "${GREEN}✅ Updated $yaml_file with $secret_count secret references${NC}"
    echo -e "${BLUE}💾 Backup saved as $yaml_file.backup${NC}"
}

build_and_deploy() {
    echo -e "${BLUE}🏗️  Building and deploying...${NC}"
    
    # Build Docker image using production stage
    echo -e "${YELLOW}Building production Docker image...${NC}"
    gcloud builds submit --tag $IMAGE_NAME --substitutions="_DOCKER_TARGET=production" .
    
    # Update the YAML file with current secrets from the secrets file
    update_yaml_with_secrets
    
    # Create a temporary YAML file with PROJECT_ID substituted
    echo -e "${YELLOW}📝 Preparing Cloud Run service configuration...${NC}"
    local temp_yaml=$(mktemp)
    sed "s/PROJECT_ID/$PROJECT_ID/g" deployment/cloudrun-service.yaml > "$temp_yaml"
    
    echo -e "${YELLOW}🚀 Deploying to Cloud Run using YAML configuration...${NC}"
    gcloud run services replace "$temp_yaml" --region $REGION
    
    # Clean up temporary file
    rm "$temp_yaml"
    
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
update_django_secrets
build_and_deploy
show_results