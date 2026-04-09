# Configuration Guide – The Summoner's Chronicle Development Pipeline

## Overview

This guide explains how to configure and manage environment variables for The Summoner's Chronicle development pipeline using the centralized configuration system.

**Key Points:**
- **Single source of truth**: All development configuration in `development.cfg`
- **Local overrides**: Sensitive values in `development.cfg.local` (gitignored)
- **Type-safe access**: Python utility (`config_loader.py`) for programmatic access
- **Environment variable support**: Override any config value with environment variables
- **Validation**: Automated checks ensure required configuration is present

---

## Configuration Files

### `development.cfg` (Main Configuration)
The default configuration file with all project settings. **Commit this to version control.**

**Location**: `C:\dev\league-of-legends\info-lol-v0.0.3\development.cfg`

**Contents**:
- Project metadata (name, version, environment)
- Technology stack (React frontend, Python backend)
- Service configurations (database, cache, API)
- Security settings (with placeholder values)
- Feature flags and performance thresholds
- Path configurations
- Quality and compliance settings

### `development.cfg.local.example` (Local Template)
Template showing what local configuration looks like. **DO NOT COMMIT sensitive values.**

**Location**: `C:\dev\league-of-legends\info-lol-v0.0.3\development.cfg.local.example`

**To Use**:
```bash
# Copy the template
cp development.cfg.local.example development.cfg.local

# Edit with your actual values
nano development.cfg.local  # or your preferred editor
```

### `development.cfg.local` (Your Local Overrides)
Your personal development configuration with actual API keys and secrets. **This file is gitignored and must NEVER be committed.**

**Key Sections to Configure**:
- `[api_integration]`: Riot Games API Key
- `[security]`: SECRET_KEY, JWT_SECRET
- `[ai_assistance]`: Claude API key (optional)
- `[monitoring]`: Sentry DSN (optional)

---

## Setup Instructions

### Step 1: Create Your Local Configuration

```bash
cd C:\dev\league-of-legends\info-lol-v0.0.3

# Copy the example template
cp development.cfg.local.example development.cfg.local
```

### Step 2: Get Your API Keys

#### Riot Games API Key
1. Go to https://developer.riotgames.com/
2. Sign in with your Riot account
3. Create a new API key
4. Copy the key and add to `development.cfg.local`:

```ini
[api_integration]
RIOT_API_KEY=RGAPI-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

#### Generate Security Keys
```bash
# Generate a SECRET_KEY
python -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))"

# Generate a JWT_SECRET
python -c "import secrets; print('JWT_SECRET=' + secrets.token_hex(32))"
```

Add to `development.cfg.local`:
```ini
[security]
SECRET_KEY=<your-generated-hex-string>
JWT_SECRET=<your-generated-hex-string>
```

#### Claude API Key (Optional, for AI Assistance)
1. Get your API key from https://console.anthropic.com/
2. Add to `development.cfg.local`:

```ini
[ai_assistance]
AI_API_KEY=sk-ant-<your-api-key>
```

### Step 3: Verify Configuration

```bash
# Run the configuration validator
python config_loader.py

# Expected output:
# ✓ Configuration loaded: Config(sections=26, keys=150, local=present)
# Configuration Sections:
# [project] (5 keys)
# [frontend] (8 keys)
# ...
# ✓ Configuration validation passed!
```

### Step 4: Create Required Directories

The configuration system automatically creates required directories:
- `./data/uploads/` - Temporary file storage
- `./data/outputs/` - Generated graphics output
- `./data/temp/` - Temporary processing files
- `./logs/` - Application logs
- `./reports/` - Quality and test reports

---

## Using Configuration in Code

### Python Backend

#### Load Configuration at Startup
```python
from config_loader import initialize_config

# Initialize and validate config
config = initialize_config()
```

#### Access Configuration Values
```python
from config_loader import Config

config = Config()

# String values
riot_api_key = config.get('api_integration', 'RIOT_API_KEY')
log_level = config.get('logging', 'LOG_LEVEL', fallback='INFO')

# Boolean values
debug_mode = config.get_bool('project', 'DEBUG_MODE')
cors_enabled = config.get_bool('backend', 'CORS_ENABLED')

# Integer values
frontend_port = config.get_int('frontend', 'FRONTEND_PORT')
cache_ttl = config.get_int('cache', 'CACHE_TTL')

# List values
allowed_origins = config.get_list('backend', 'CORS_ORIGINS')
supported_regions = config.get_list('api_integration', 'RIOT_REGIONS')

# Get all values in a section
backend_config = config.section_items('backend')

# Export all config as environment variables
env_vars = config.export_env_vars()
os.environ.update(env_vars)
```

#### Example Flask Application Setup
```python
from flask import Flask
from config_loader import initialize_config

# Initialize configuration
config = initialize_config()

# Create Flask app
app = Flask(__name__)

# Configure from config file
app.config['DEBUG'] = config.get_bool('project', 'DEBUG_MODE')
app.config['SECRET_KEY'] = config.get('security', 'SECRET_KEY')
app.config['CORS_ORIGINS'] = config.get_list('backend', 'CORS_ORIGINS')

# Set up logging
logging_level = config.get('logging', 'LOG_LEVEL')
log_file = config.get('logging', 'LOG_FILE_PATH')

@app.route('/health')
def health():
    return {
        'status': 'healthy',
        'environment': config.get('project', 'ENVIRONMENT'),
        'version': config.get('project', 'PROJECT_VERSION')
    }
```

### JavaScript Frontend

#### Load Environment Variables at Build Time
```javascript
// React component
const FRONTEND_FRAMEWORK = process.env.REACT_APP_FRONTEND_FRAMEWORK;
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;
const DEBUG_MODE = process.env.REACT_APP_DEBUG_MODE === 'true';

function App() {
  return (
    <div>
      <h1>{FRONTEND_FRAMEWORK} Application</h1>
      <p>API: {API_BASE_URL}</p>
    </div>
  );
}
```

#### Environment Variable Mapping
For frontend, create `.env.local` (gitignored) with:
```bash
# .env.local
REACT_APP_API_BASE_URL=http://localhost:5000
REACT_APP_DEBUG_MODE=true
REACT_APP_FRONTEND_PORT=3000
REACT_APP_LOG_LEVEL=debug
```

---

## Configuration Priority

Configuration values are resolved in this priority order (highest to lowest):

1. **Environment Variables** (e.g., `RIOT_API_KEY=...`)
   ```bash
   export RIOT_API_KEY=RGAPI-xxxx
   python my_app.py
   ```

2. **development.cfg.local** (local overrides, gitignored)
   ```ini
   [api_integration]
   RIOT_API_KEY=RGAPI-xxxx
   ```

3. **development.cfg** (default values)
   ```ini
   [api_integration]
   RIOT_API_KEY=RGAPI-YOUR-API-KEY-HERE
   ```

4. **Built-in Defaults** (in config_loader.py `get()` methods)
   ```python
   log_level = config.get('logging', 'LOG_LEVEL', fallback='INFO')
   ```

### Example: Overriding Configuration

```bash
# Using environment variable (highest priority)
export RIOT_API_KEY=RGAPI-override
python my_app.py

# Using development.cfg.local (second priority)
echo "[api_integration]" >> development.cfg.local
echo "RIOT_API_KEY=RGAPI-local" >> development.cfg.local

# Default in development.cfg (third priority)
# Already set to RGAPI-YOUR-API-KEY-HERE

# Fallback in code (lowest priority)
api_key = config.get('api_integration', 'RIOT_API_KEY', fallback='RGAPI-fallback')
```

---

## Configuration Sections Reference

### `[project]`
**Project metadata and environment**

| Key | Type | Example | Purpose |
|-----|------|---------|---------|
| PROJECT_NAME | string | "The Summoner's Chronicle" | Project identifier |
| PROJECT_VERSION | string | "0.0.3" | Current version |
| ENVIRONMENT | string | "development" | dev/staging/production |
| DEBUG_MODE | bool | true | Enable debug logging |

### `[frontend]`
**React frontend configuration**

| Key | Type | Example | Purpose |
|-----|------|---------|---------|
| FRONTEND_FRAMEWORK | string | "React" | Frontend framework |
| FRONTEND_PORT | int | 3000 | Development server port |
| FRONTEND_HOST | string | "localhost" | Development server host |
| REACT_VERSION | string | "18.2.0" | React version |

### `[backend]`
**Python backend configuration**

| Key | Type | Example | Purpose |
|-----|------|---------|---------|
| BACKEND_FRAMEWORK | string | "Flask" | Backend framework |
| BACKEND_LANGUAGE | string | "Python" | Backend language |
| BACKEND_PORT | int | 5000 | Backend server port |
| BACKEND_LOG_LEVEL | string | "DEBUG" | Log verbosity level |

### `[api_integration]`
**Third-party API configuration**

| Key | Type | Example | Purpose |
|-----|------|---------|---------|
| RIOT_API_KEY | string | "RGAPI-xxxx" | Riot Games API authentication |
| RIOT_API_BASE_URL | string | "https://na1.api.riotgames.com" | Riot API endpoint |
| RIOT_API_TIMEOUT | int | 10 | Request timeout in seconds |

### `[security]`
**Security and authentication**

| Key | Type | Example | Purpose |
|-----|------|---------|---------|
| SECRET_KEY | string | "random-hex-32" | Flask session key |
| JWT_SECRET | string | "random-hex-32" | JWT signing key |
| HTTPS_ENABLED | bool | false | Require HTTPS |
| SESSION_TIMEOUT | int | 3600 | Session timeout in seconds |

### `[database]`
**Database configuration**

| Key | Type | Example | Purpose |
|-----|------|---------|---------|
| DATABASE_TYPE | string | "SQLite" | Database engine |
| DATABASE_PATH | string | "./data/summoners_chronicle.db" | SQLite file path |
| DATABASE_HOST | string | "localhost" | Database server host |
| DATABASE_PORT | int | 5432 | Database server port |

### `[logging]`
**Application logging**

| Key | Type | Example | Purpose |
|-----|------|---------|---------|
| LOG_LEVEL | string | "DEBUG" | Log verbosity (DEBUG/INFO/WARNING/ERROR/CRITICAL) |
| LOG_FILE_PATH | string | "./logs/development.log" | Log file location |
| LOG_CONSOLE_OUTPUT | bool | true | Print logs to console |

### `[quality]`
**Code quality enforcement**

| Key | Type | Example | Purpose |
|-----|------|---------|---------|
| LINTING_ENABLED | bool | true | Enable code linting |
| CODE_FORMATTER | string | "Black" | Code formatter tool |
| TEST_COVERAGE_MINIMUM | int | 80 | Minimum test coverage % |
| COVERAGE_CRITICAL_PATHS | int | 90 | Critical path coverage % |

---

## Validation and Health Checks

### Run Configuration Validation

```bash
python config_loader.py
```

**Output Example**:
```
✓ Configuration loaded: Config(sections=26, keys=150, local=present)

Configuration Sections:
  [project] (5 keys)
  [frontend] (8 keys)
  [backend] (7 keys)
  ...

Sample Values:
  PROJECT_NAME: The Summoner's Chronicle
  ENVIRONMENT: development
  FRONTEND_FRAMEWORK: React
  BACKEND_LANGUAGE: Python
  FRONTEND_PORT: 3000
  DEBUG_MODE: True

Validating Configuration...
✓ Configuration validation passed!
```

### Common Configuration Errors

**Error: "Main configuration file not found"**
```
Solution: Ensure development.cfg exists in project root:
  C:\dev\league-of-legends\info-lol-v0.0.3\development.cfg
```

**Error: "Configuration key not found"**
```
Solution: Add the missing key to development.cfg or development.cfg.local:
  [section_name]
  KEY_NAME=value
```

**Error: "Placeholder value detected"**
```
Solution: Update the value in development.cfg.local with your actual credentials:
  # Before (placeholder):
  RIOT_API_KEY=RGAPI-YOUR-API-KEY-HERE
  
  # After (actual key):
  RIOT_API_KEY=RGAPI-xxxx-xxxx-xxxx-xxxx
```

---

## Security Best Practices

### ✅ DO

- ✅ Keep `development.cfg.local` in `.gitignore` (already configured)
- ✅ Store sensitive values in `development.cfg.local` only
- ✅ Regenerate security keys regularly
- ✅ Use environment variables for production deployments
- ✅ Rotate API keys periodically
- ✅ Use strong, random values for SECRET_KEY and JWT_SECRET

### ❌ DON'T

- ❌ Commit `development.cfg.local` to version control
- ❌ Hardcode API keys in application code
- ❌ Share `.local` files via email or chat
- ❌ Use placeholder values in production
- ❌ Reuse security keys across environments
- ❌ Store passwords in comments or documentation

### Emergency: Exposed API Key?

If you accidentally commit a secret:

```bash
# 1. Regenerate the key immediately at https://developer.riotgames.com/

# 2. Remove from git history
git filter-branch --tree-filter 'rm -f development.cfg.local' HEAD

# 3. Force push (use with caution!)
git push --force-with-lease

# 4. Add a pre-commit hook to prevent future accidents
# The .claude/settings.json already prevents hardcoded config commits
```

---

## CI/CD and Production Deployment

### GitHub Actions Example

```yaml
# .github/workflows/deploy.yml
name: Deploy

on: [push]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Load Configuration
        env:
          RIOT_API_KEY: ${{ secrets.RIOT_API_KEY }}
          SECRET_KEY: ${{ secrets.SECRET_KEY }}
          JWT_SECRET: ${{ secrets.JWT_SECRET }}
        run: |
          # Configuration is loaded from environment variables
          python config_loader.py
      
      - name: Run Tests
        run: |
          python -m pytest
      
      - name: Deploy
        run: |
          # Deployment uses environment variables
          python deploy.py
```

### Environment Variables in Production

```bash
# On production server, set environment variables:
export RIOT_API_KEY=RGAPI-prod-xxxx
export SECRET_KEY=prod-secret-key
export JWT_SECRET=prod-jwt-secret
export ENVIRONMENT=production
export DEBUG_MODE=false

# Then run application
python app.py
```

---

## Troubleshooting

### Configuration Not Loading

```python
# Check if config files exist
import os
from pathlib import Path

config_file = Path("development.cfg")
local_file = Path("development.cfg.local")

print(f"Main config exists: {config_file.exists()}")
print(f"Local config exists: {local_file.exists()}")
```

### Values Not Updating

```bash
# Check environment variable priority
echo $RIOT_API_KEY  # Environment takes priority
grep RIOT_API_KEY development.cfg.local  # Local overrides
grep RIOT_API_KEY development.cfg  # Defaults
```

### Permission Issues with Log Files

```bash
# Ensure logs directory is writable
mkdir -p logs
chmod 755 logs
touch logs/development.log
chmod 666 logs/development.log
```

---

## Integration with Quality Mandate

Configuration management is part of the **DEVELOPER_AGENT_QUALITY_MANDATE** (Pillar 5: Configuration & Environment):

- ✅ All environment-specific values externalized to configuration
- ✅ No hardcoded API keys, paths, or endpoints
- ✅ Configuration validation runs on startup
- ✅ Default configuration template provided
- ✅ Missing/invalid configuration causes graceful exit with diagnostics

See `.docs/DEVELOPER_AGENT_QUALITY_MANDATE.md` for full details.

---

## References

- **Configuration Files**: `development.cfg`, `development.cfg.local.example`
- **Config Loader**: `config_loader.py`
- **Quality Mandate**: `.docs/DEVELOPER_AGENT_QUALITY_MANDATE.md`
- **Settings Policy**: `.claude/settings.json`
- **Git Ignore**: `.gitignore`

---

**Last Updated**: 2026-04-10  
**Status**: Production-Ready
