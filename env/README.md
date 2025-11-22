# Environment Configuration Directory

This directory contains all environment configuration files for the Cabana project.

## File Structure

```
env/
├── .env.dev                   # Development environment variables ✅ COMMIT
├── .env.prod                  # Production environment variables ✅ COMMIT
├── .env.secrets.dev           # Development secrets ❌ DO NOT COMMIT
├── .env.secrets.prod          # Production secrets ❌ DO NOT COMMIT
├── .env.secrets.dev.example   # Development secrets template ✅ COMMIT
└── .env.secrets.prod.example  # Production secrets template ✅ COMMIT
```

## Quick Setup

### 1. Create Your Secret Files

```powershell
# Copy example files to create your actual secret files
copy env\.env.secrets.dev.example env\.env.secrets.dev
copy env\.env.secrets.prod.example env\.env.secrets.prod
```

### 2. Edit Your Secrets

```powershell
# Add your actual API keys and secrets
notepad env\.env.secrets.dev
notepad env\.env.secrets.prod
```

### 3. Start Development

```powershell
# Docker will automatically use env/.env.dev + env/.env.secrets.dev
.\deployment\docker-test.ps1 dev
```

## File Types

### Environment Variables (.env.dev, .env.prod)
- **Safe to commit to Git** ✅
- Contains non-sensitive configuration
- DEBUG settings, allowed hosts, feature flags
- Database connection strings (without passwords)

### Secrets (.env.secrets.dev, .env.secrets.prod)
- **NEVER commit to Git** ❌
- Contains sensitive data
- API keys, passwords, tokens
- Database passwords, OAuth secrets

## Benefits of This Structure

✅ **Organized**: All environment files in one directory
✅ **Visible**: All files show with .env prefix in VS Code
✅ **Secure**: Clear separation of public config vs secrets
✅ **Scalable**: Easy to add new environments (staging, test)
✅ **Team-friendly**: Example files help onboarding

## VS Code Icons

All files now start with `.env` so they'll show with the environment variable icon in VS Code Explorer, making them easy to identify and work with.

## Security

The `.gitignore` file is configured to:
- ✅ Commit: `.env.dev`, `.env.prod`, `.env.secrets.*.example`
- ❌ Ignore: `.env.secrets.dev`, `.env.secrets.prod`

## Usage in Scripts

- **Docker Development**: Uses `env/.env.dev + env/.env.secrets.dev`
- **Docker Production**: Uses `env/.env.prod + env/.env.secrets.prod`
- **Cloud Deployment**: Automatically reads from `env/` directory based on environment