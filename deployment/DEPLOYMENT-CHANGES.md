# Deployment Process Updates

## Changes Made

### 1. Single Source of Truth

- The deployment now uses `cloudrun-service.yaml` as the single source of truth for Cloud Run configuration
- Removed inline `gcloud run deploy` flags in favor of declarative YAML configuration

### 2. Automatic Secrets Management

- Created `update-secrets-yaml.sh` script that automatically reads your `.env.secrets.*` files and generates the corresponding secret references in the YAML
- The deployment script now automatically updates the YAML with all secrets before deploying
- No need to manually maintain multiple lists of secrets

### 3. Environment Variables Structure

The YAML now contains:

- **Secrets**: Automatically pulled from Secret Manager based on your `.env.secrets.*` files
- **Non-secret config**: Environment variables from your `.env.*` files (DEBUG, ALLOWED_HOSTS, etc.)

## How It Works

1. **Before deployment**: The `deploy.sh` script automatically reads your `env/.env.secrets.{ENV_TYPE}` file
2. **Generates secret references**: Creates Secret Manager references for each secret in your file
3. **Updates YAML**: Updates the `cloudrun-service.yaml` with all current secrets
4. **Deploys**: Uses `gcloud run services replace` with the updated YAML file

## Usage

### Standard Deployment

```bash
./deploy.sh my-project-id us-central1 prod
```

The deployment script automatically handles everything - no need for separate commands!

## Benefits

1. **Single source of truth**: All Cloud Run configuration in one YAML file
2. **Automatic secret management**: Add/remove secrets in `.env.secrets.*` and they're automatically included
3. **Version controlled**: Your deployment configuration is fully tracked in Git
4. **Consistent deployments**: Same configuration every time
5. **Easy maintenance**: No need to update multiple places when secrets change

## File Structure

```
deployment/
├── deploy.sh                    # Main deployment script (includes secrets auto-update)
├── cloudrun-service.yaml       # Cloud Run configuration (single source of truth)
└── DEPLOYMENT-CHANGES.md       # This documentation

env/
├── .env.prod                   # Non-secret production config
├── .env.dev                    # Non-secret development config
├── .env.secrets.prod.example   # Example secrets file
└── .env.secrets.prod           # Actual secrets (not in Git)
```

## Next Steps

1. Make sure your `.env.secrets.{ENV_TYPE}` files contain all the secrets you need
2. Run the deployment script - it will automatically pick up all secrets
3. If you add/remove secrets, just redeploy - the script handles it automatically

The system is now much more maintainable and follows infrastructure-as-code best practices!
