# Cabana Deployment Guide

Complete deployment and development setup with Docker, environment management, and Cloud Run deployment.

## 📁 Directory Structure

```
deployment/
├── README.md                   # This comprehensive guide
├── Dockerfile                  # Multi-stage Docker build (dev + production)
├── docker-compose.yml          # Local development orchestration
├── docker-test.sh             # Local testing and validation script
├── deploy.sh                  # Cloud Run deployment script
├── cloudrun-service.yaml      # Cloud Run service configuration
└── .dockerignore              # Docker build context exclusions
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Google Cloud CLI (gcloud) for production deployment
- Environment files configured (see [Environment Setup](#environment-setup))

### First Time Setup

```bash
# Build the Docker images (do this once)
./deployment/docker-test.sh dev --build

# For subsequent runs (much faster)
./deployment/docker-test.sh dev
```

### Local Development

```bash
# Start development environment (quick start, no rebuild)
./deployment/docker-test.sh dev

# Start development environment with rebuild (first time or after changes)
./deployment/docker-test.sh dev --build

# Start production-like testing environment
./deployment/docker-test.sh prod

# Start production-like testing with rebuild
./deployment/docker-test.sh prod --build

# Run comprehensive tests
./deployment/docker-test.sh test
```

### Cloud Deployment

```bash
# Deploy to Google Cloud Run
./deployment/deploy.sh YOUR_PROJECT_ID us-central1 prod
```

## 🔧 Environment Setup

The application supports multiple environment configurations with proper separation of secrets and configuration.

### File Structure

```
env/
├── .env.dev                   # Development environment variables (SAFE TO COMMIT)
├── .env.prod                  # Production environment variables (SAFE TO COMMIT)
├── .env.secrets.dev           # Development secrets (DO NOT COMMIT)
├── .env.secrets.prod          # Production secrets (DO NOT COMMIT)
├── .env.secrets.dev.example   # Development secrets template (COMMIT)
└── .env.secrets.prod.example  # Production secrets template (COMMIT)
```

### Initial Setup

1. **Copy the example files:**

   ```bash
   cp env/.env.secrets.dev.example env/.env.secrets.dev
   cp env/.env.secrets.prod.example env/.env.secrets.prod
   ```

2. **Edit with your actual API keys:**

   ```bash
   # Add your development keys
   nano env/.env.secrets.dev

   # Add your production keys
   nano env/.env.secrets.prod
   ```

### Environment Variables vs Secrets

**Environment Variables** (.env.dev, .env.prod) - Safe to commit:

- DEBUG settings
- ALLOWED_HOSTS
- Database connection settings (without passwords)
- Feature flags
- Non-sensitive configuration

**Secrets** (.env.secrets.dev, .env.secrets.prod) - Never commit:

- API keys (Google Maps, OpenAI, etc.)
- Database passwords
- SECRET_KEY
- Third-party service credentials

### Example Files

**env/.env.dev:**

```env
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
ENABLE_DEBUG_TOOLBAR=True
```

**env/.env.secrets.dev:**

```env
SECRET_KEY=dev-secret-key-here
GOOGLE_MAPS_API_KEY=your-dev-maps-key
OPENAI_API_KEY=your-dev-openai-key
```

**env/.env.prod:**

```env
DEBUG=False
ALLOWED_HOSTS=*.run.app,yourdomain.com
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
SECURE_SSL_REDIRECT=True
ENABLE_DEBUG_TOOLBAR=False
```

**env/.env.secrets.prod:**

```env
SECRET_KEY=super-long-production-secret-key
GOOGLE_MAPS_API_KEY=your-production-maps-key
OPENAI_API_KEY=your-production-openai-key
```

## 🏗️ Architecture

### Multi-Stage Dockerfile

- **Base Stage**: Common dependencies and setup
- **Development Stage**: Development server with frequent health checks
- **Production Stage**: Static file collection, Gunicorn server, optimized health checks

### Docker Compose Services

- **web**: Development service with live code mounting
- **web-prod**: Production-like testing service
- **db**: Optional PostgreSQL for local development
- **redis**: Optional Redis for caching

## 🔄 When to Use --build Flag

### Use `--build` when:
- **First time setup**: Initial project setup
- **Requirements changed**: Modified `requirements.txt`
- **Dockerfile modified**: Changed Docker configuration
- **Base image updates**: Want latest Python/system packages
- **Debugging**: Something seems broken, fresh build might help

### Skip `--build` for:
- **Daily development**: Code changes (handled by volume mounting)
- **Quick testing**: Just want to run the app
- **Restarting**: After stopping the container

### Typical Workflow:
```bash
# Monday morning - fresh start
./deployment/docker-test.sh dev --build

# Rest of the week - quick starts
./deployment/docker-test.sh dev
./deployment/docker-test.sh stop
./deployment/docker-test.sh dev  # Fast restart
```

## 📋 Development Commands

### Basic Commands

```bash
# Start development (quick start - uses existing container)
./deployment/docker-test.sh dev

# Start development with rebuild (first time or after dependency changes)
./deployment/docker-test.sh dev --build

# Start production-like testing (quick start)
./deployment/docker-test.sh prod

# Start production-like testing with rebuild
./deployment/docker-test.sh prod --build

# Run full test suite (always rebuilds for testing)
./deployment/docker-test.sh test

# View logs
./deployment/docker-test.sh logs

# Get shell access
./deployment/docker-test.sh shell

# Stop all services
./deployment/docker-test.sh stop

# Clean up everything (containers, images, volumes)
./deployment/docker-test.sh clean

# Health check
./deployment/docker-test.sh health
```

### Manual Docker Commands

If you prefer manual Docker commands:

```bash
# Build the image
docker build -f deployment/Dockerfile -t cabana-local .

# Run development container with volume mounting
docker run -p 8080:8080 \
  --env-file env/.env.dev \
  --env-file env/.env.secrets.dev \
  -v $(pwd):/app \
  --name cabana-dev \
  cabana-local \
  python manage.py runserver 0.0.0.0:8080

# Run production-like container
docker run -p 8080:8080 \
  --env-file env/.env.prod \
  --env-file env/.env.secrets.prod \
  --name cabana-prod \
  cabana-local
```

## 🌐 Cloud Run Deployment

### Deployment Script Usage

```bash
# Basic deployment
./deployment/deploy.sh PROJECT_ID

# Specify region and environment
./deployment/deploy.sh PROJECT_ID us-central1 prod

# Available regions: us-central1, us-east1, us-west1, europe-west1, asia-east1
```

### What Happens During Deployment

1. **Validation**: Checks prerequisites and environment files
2. **Environment Loading**: Reads `.env.prod` and `.env.secrets.prod`
3. **Secret Management**: Uploads secrets to Google Secret Manager
4. **Container Build**: Builds and pushes Docker image to Google Container Registry
5. **Service Deployment**: Deploys to Cloud Run with proper configuration
6. **Health Check**: Verifies deployment success

### Prerequisites for Cloud Run Deployment

Before deploying, ensure you have:

1. **Google Cloud SDK**: Install and configure gcloud CLI
2. **Docker**: Required for local building (optional, Cloud Build can handle this)
3. **Google Cloud Project**: With billing enabled

**Set up Google Cloud Project:**

```bash
# Set your project ID
export PROJECT_ID="your-project-id"
gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### Manual Deployment Commands

For fine-grained control:

```bash
# Build and push image
docker build -f deployment/Dockerfile -t gcr.io/$PROJECT_ID/cabana-project .
docker push gcr.io/$PROJECT_ID/cabana-project

# Deploy to Cloud Run
gcloud run deploy cabana-project \
    --image gcr.io/$PROJECT_ID/cabana-project \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --set-env-vars="DEBUG=False,ALLOWED_HOSTS=*.run.app" \
    --set-secrets="SECRET_KEY=cabana-secrets-prod:latest:SECRET_KEY,GOOGLE_MAPS_API_KEY=cabana-secrets-prod:latest:GOOGLE_MAPS_API_KEY"
```

## 🔒 Security Best Practices

### ✅ DO

- Keep secrets in `.env.secrets.*` files
- Add `.env.secrets.*` to `.gitignore`
- Use different keys for development and production
- Rotate production keys regularly
- Use test/sandbox keys for development
- Use Google Secret Manager for production secrets

### ❌ DON'T

- Commit secrets to Git
- Use production keys in development
- Share secrets via email or chat
- Store secrets in code comments
- Use the same secret key across environments

## 🔧 Adding New Environment Variables

### Step 1: Add to Environment Files

**Non-sensitive configuration** (add to `.env.dev` and/or `.env.prod`):

```env
NEW_FEATURE_ENABLED=True
MAX_UPLOAD_SIZE=10485760
CACHE_TIMEOUT=300
```

**Sensitive data** (add to `.env.secrets.dev` and/or `.env.secrets.prod`):

```env
NEW_API_KEY=your-secret-api-key
DATABASE_PASSWORD=your-db-password
```

### Step 2: Update Django Settings

Update `settings.py` to use the new variables:

```python
# Environment variables
NEW_FEATURE_ENABLED = os.getenv('NEW_FEATURE_ENABLED', 'False').lower() == 'true'
MAX_UPLOAD_SIZE = int(os.getenv('MAX_UPLOAD_SIZE', '5242880'))

# Secrets
NEW_API_KEY = os.getenv('NEW_API_KEY')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
```

### Step 3: Deploy Changes

```bash
# Test locally first
./deployment/docker-test.sh dev

# Then deploy to production
./deployment/deploy.sh YOUR_PROJECT_ID
```

## 🐛 Troubleshooting

### Common Issues

**Port already in use:**

```bash
# Find and kill process using port 8080
lsof -ti:8080 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :8080   # Windows
```

**Missing environment files:**

```
❌ Error: Missing env/.env.secrets.dev
```

Solution: Copy from example file and add your keys

```bash
cp env/.env.secrets.dev.example env/.env.secrets.dev
```

**Container won't start:**

```bash
# Check logs for errors
docker logs container-name
./deployment/docker-test.sh logs
```

**Variables not loading:**

1. Check file location (should be in project root)
2. Check file syntax (no spaces around `=`, no quotes needed)
3. Check Django settings (ensure `os.getenv('VARIABLE_NAME')` exists)
4. Check deployment logs with `gcloud logs read`

**Cloud Run specific issues:**

1. **Build failures**: Check `requirements.txt` and `deployment/Dockerfile`
2. **502 errors**: Verify health check endpoint and port configuration
3. **Permission errors**: Ensure service account has proper permissions

**Useful Cloud Run Commands:**

```bash
# View service logs
gcloud logs read --service=cabana-project

# Scale service
gcloud run services update cabana-project --max-instances=20

# Update environment variables
gcloud run services update cabana-project --set-env-vars="KEY=value"
```

### Testing Endpoints

Once running locally, test these endpoints:

- **Main Application**: http://localhost:8080
- **Health Check**: http://localhost:8080/health/
- **Admin Panel**: http://localhost:8080/admin/ (if enabled)

```bash
# Test health endpoint
curl http://localhost:8080/health/
# Expected: {"status": "healthy", "service": "cabana-project"}
```

**Windows PowerShell:**

```powershell
Invoke-RestMethod -Uri "http://localhost:8080/health/"
```

## 📊 Performance and Monitoring

### Production Monitoring and Logging

- **Health check endpoint**: `/health/`
- **Cloud Logging**: Logs are sent to Cloud Logging automatically
- **Configure alerting**: Set up alerting policies in Google Cloud Console

### Cost Optimization

Cloud Run automatically provides cost optimization:

- **Auto-scaling**: Service scales to zero when not in use
- **Resource allocation**: 1 vCPU, 1 GiB memory by default
- **Maximum instances**: 10 (configurable)
- **Pay-per-use**: Only pay for actual request processing time

### Local Performance Testing

```bash
# Simple load test (requires apache-bench)
ab -n 1000 -c 10 http://localhost:8080/health/

# Basic response time testing
for i in {1..10}; do curl -o /dev/null -s -w "%{time_total}\n" http://localhost:8080/health/; done
```

### Docker Container Management

```bash
# List running containers
docker ps

# View container logs
docker logs cabana-container

# Execute commands in running container
docker exec -it cabana-container bash

# Check container resource usage
docker stats cabana-container

# Container cleanup
docker system prune -a  # Remove unused containers, images, networks
```

## 🔄 Migration from Legacy Setup

If migrating from a single `.env` file:

1. **Backup** your current `.env` file
2. **Create** the new environment file structure
3. **Split** variables into environment vs secrets
4. **Test** locally with new structure
5. **Update** deployment process

The system maintains backward compatibility - if the new files don't exist, it falls back to the legacy `.env` file.

## 📚 Script Reference

| Script           | Purpose                    | Key Features                                                        |
| ---------------- | -------------------------- | ------------------------------------------------------------------- |
| `docker-test.sh` | Local testing & validation | Environment validation, health checks, Docker Compose orchestration |
| `deploy.sh`      | Cloud Run deployment       | Environment-aware deployment, prerequisite validation               |

## 🏷️ Environment Comparison

| Setting       | Development           | Production                |
| ------------- | --------------------- | ------------------------- |
| DEBUG         | True                  | False                     |
| ALLOWED_HOSTS | localhost,127.0.0.1   | \*.run.app,yourdomain.com |
| Database      | SQLite                | Cloud SQL/PostgreSQL      |
| Email         | Console backend       | SMTP                      |
| Cache         | Local memory          | Redis                     |
| SSL           | Disabled              | Enabled                   |
| API Keys      | Test/development keys | Production keys           |
| Server        | Django dev server     | Gunicorn                  |
| Static files  | Django serves         | WhiteNoise                |
| Logging       | Console               | Cloud Logging             |

## 🏗️ Django Configuration for Production

### Static Files

- Uses **WhiteNoise** for serving static files in production
- Static files are collected during Docker build
- No additional CDN setup required for basic deployment

### Database Considerations

- **Development**: SQLite (default)
- **Production**: Consider Cloud SQL (PostgreSQL recommended)
- Set `DATABASE_URL` environment variable for production database

### Security Features

Production security settings are automatically enabled when `DEBUG=False`:

- SSL redirect
- Secure cookies
- XSS protection
- Content type nosniff
- CSRF trusted origins

This unified documentation provides everything needed for both development and deployment of the Cabana project while maintaining security best practices and clear separation of concerns.

### Cloud Deployment

```bash
# Deploy to production
./deployment/deploy.sh my-project-id us-central1 prod

# Deploy to staging region
./deployment/deploy.sh my-project-id us-west1 prod
```

## 🔍 Health Checks

The system includes comprehensive health monitoring:

- **Docker health checks**: Built into both development and production stages
- **Script health validation**: Automated endpoint testing during deployment
- **Cloud Run health checks**: Automatic service health monitoring

## 🧹 Cleanup

```bash
# Stop all services
./deployment/docker-test.sh stop

# Remove all containers, images, and volumes
./deployment/docker-test.sh clean
```

## 🔐 Security

- Environment variables loaded at runtime (not baked into images)
- Secrets separated from configuration
- Production validation prevents insecure defaults
- Non-root user in Docker containers

## 🎯 Design Principles

1. **Single Responsibility**: Each script has a clear, focused purpose
2. **Environment Agnostic**: Same Docker image runs in all environments
3. **Fail Fast**: Comprehensive validation prevents silent failures
4. **Developer Experience**: Simple commands for complex operations
5. **Production Ready**: Built-in security and operational best practices
