# DevContainer Secrets Template

This file defines the secure secrets and parameters needed for the multi-agentic devcontainer.

## Required Secrets (Secure Injection)

### API Keys (Optional but Recommended)
```bash
# OpenAI API Key - For premium AI features
# Get from: https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-your-openai-key-here

# Hugging Face Token - For private models and higher rate limits
# Get from: https://huggingface.co/settings/tokens
HUGGINGFACE_TOKEN=hf_your-huggingface-token-here

# GitHub Token - For Copilot and repository access
# Get from: https://github.com/settings/tokens
GITHUB_TOKEN=ghp_your-github-token-here
```

### Service Endpoints
```bash
# Ollama Base URL (default: localhost)
OLLAMA_BASE_URL=http://localhost:11434

# Custom model endpoints (if using external services)
CUSTOM_MODEL_ENDPOINT=https://your-custom-endpoint.com
```

## Configuration Parameters

### Development Settings
```bash
# Debug mode
DEBUG=true

# Log level
LOG_LEVEL=info

# Performance settings
MAX_CONCURRENT_AGENTS=3
MEMORY_LIMIT_GB=8
CPU_CORES=4
```

### Security Settings
```bash
# Encryption keys (generate securely)
AGENT_ENCRYPTION_KEY=your-32-byte-encryption-key
SESSION_SECRET=your-session-secret-key

# Access controls
ALLOWED_USERS=user1,user2
ADMIN_USERS=admin1
```

### Network Settings
```bash
# Proxy settings (if needed)
HTTP_PROXY=http://proxy.company.com:8080
HTTPS_PROXY=http://proxy.company.com:8080
NO_PROXY=localhost,127.0.0.1

# Firewall rules
ALLOWED_IPS=192.168.1.0/24,10.0.0.0/8
```

## Secure Injection Methods

### Method 1: VS Code Dev Containers Secrets
```json
// .devcontainer/devcontainer.json
{
  "secrets": {
    "OPENAI_API_KEY": {
      "description": "OpenAI API Key for AI features"
    },
    "HUGGINGFACE_TOKEN": {
      "description": "Hugging Face token for model access"
    }
  }
}
```

### Method 2: Environment File
```bash
# Create .env file in workspace root
cp .env.example .env
# Edit with your secrets
```

### Method 3: Docker Secrets (Production)
```bash
# Use Docker secrets for production deployments
echo "your-secret" | docker secret create openai_key -
```

### Method 4: External Secret Management
```bash
# AWS Secrets Manager, HashiCorp Vault, etc.
# Configure in container startup scripts
```

## Security Best Practices

1. **Never commit secrets** to version control
2. **Use strong, unique keys** for each service
3. **Rotate keys regularly** (90 days recommended)
4. **Limit key permissions** to minimum required
5. **Monitor key usage** for anomalies
6. **Revoke compromised keys** immediately

## Validation

The container will validate secrets on startup:
- Check key format and basic validity
- Test API connectivity (non-destructive)
- Log validation results (without exposing secrets)

## Emergency Procedures

If secrets are compromised:
1. Immediately revoke all affected keys
2. Generate new keys
3. Update all systems using the keys
4. Audit access logs for unauthorized use
5. Notify relevant parties if data exposure occurred