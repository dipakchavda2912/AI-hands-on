# Configuration Guide

Complete guide to configuring CodeBaseOpsAI-v3 for development, testing, and production environments.

---

## Table of Contents

1. [Configuration Overview](#configuration-overview)
2. [Environment Variables](#environment-variables)
3. [Configuration File (config.py)](#configuration-file-configpy)
4. [LLM Configuration](#llm-configuration)
5. [GitHub Integration](#github-integration)
6. [Agent Configuration](#agent-configuration)
7. [Logging and Monitoring](#logging-and-monitoring)
8. [Environment-Specific Settings](#environment-specific-settings)
9. [Security Best Practices](#security-best-practices)
10. [Performance Tuning](#performance-tuning)
11. [Troubleshooting Configuration](#troubleshooting-configuration)

---

## Configuration Overview

CodeBaseOpsAI-v3 uses a **layered configuration approach**:

```
Priority (highest to lowest):
1. Environment variables (.env file or system)
2. Default values in config.py
3. Hardcoded fallbacks
```

### Configuration Files

| File | Purpose | Example Location |
|------|---------|------------------|
| `.env` | Environment-specific secrets and settings | Project root |
| `config.py` | Configuration schema and validation | Project root |
| `.env.example` | Template for .env file | Project root |

### Why This Approach?

**Benefits:**
- **Security:** Secrets in `.env` (not committed to git)
- **Flexibility:** Different settings per environment
- **Validation:** Pydantic ensures type safety
- **Documentation:** Settings self-documented in code

---

## Environment Variables

### Creating Your .env File

```bash
# Copy template
cp .env.example .env

# Edit with your values
nano .env  # or use your preferred editor
```

### Complete .env Reference

```bash
# .env file - DO NOT COMMIT TO GIT

# =============================================================================
# LLM Configuration
# =============================================================================

# Google API Key (REQUIRED)
# Get from: https://aistudio.google.com/app/apikey
GOOGLE_API_KEY=AIzaSyD_your_actual_key_here

# Model Selection
# Options: gemini-2.0-flash-exp, gemini-1.5-flash, gemini-1.5-pro
# Recommendation: gemini-2.0-flash-exp (fastest, good quality)
MODEL_NAME=gemini-2.0-flash-exp

# Temperature (0.0 = deterministic, 1.0 = creative, 2.0 = very creative)
# Recommendation: 0.0 for consistent code analysis
TEMPERATURE=0.0

# Max Retries (number of retry attempts on failure)
MAX_RETRIES=3

# Timeout (seconds to wait for LLM response)
TIMEOUT=60.0

# =============================================================================
# GitHub Configuration
# =============================================================================

# GitHub Token (OPTIONAL - for private repos and higher rate limits)
# Get from: https://github.com/settings/tokens
# Scopes needed: repo (for private repos), public_repo (for public)
GITHUB_TOKEN=ghp_your_token_here

# GitHub API URL (change for GitHub Enterprise)
GITHUB_API_URL=https://api.github.com

# =============================================================================
# Agent Configuration
# =============================================================================

# Enable state checkpointing (conversation memory)
# true = agent remembers context, false = stateless
ENABLE_CHECKPOINTING=true

# Max iterations (prevents infinite loops)
# Recommendation: 15 for most tasks
MAX_ITERATIONS=15

# =============================================================================
# Logging Configuration
# =============================================================================

# Log Level
# Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
# Recommendation: INFO for production, DEBUG for development
LOG_LEVEL=INFO

# =============================================================================
# Observability (OPTIONAL - for production monitoring)
# =============================================================================

# Enable LangSmith tracing
# Requires LangSmith account: https://smith.langchain.com/
ENABLE_TRACING=false

# LangSmith API Key
LANGSMITH_API_KEY=ls__your_langsmith_key

# LangSmith Project Name
LANGSMITH_PROJECT=codebaseopsai

# =============================================================================
# API Server Configuration (if using FastAPI)
# =============================================================================

# Server host
API_HOST=0.0.0.0

# Server port
API_PORT=8000

# Enable auto-reload (development only)
API_RELOAD=true

# CORS origins (comma-separated)
CORS_ORIGINS=http://localhost:3000,http://localhost:8080

# =============================================================================
# Production-Specific Settings
# =============================================================================

# Redis URL (for production state persistence)
# REDIS_URL=redis://localhost:6379/0

# PostgreSQL URL (for production state persistence)
# POSTGRES_URL=postgresql://user:password@localhost:5432/codebaseopsai

# Worker concurrency
# WORKER_CONCURRENCY=4

# Max concurrent requests
# MAX_CONCURRENT_REQUESTS=100
```

### Environment Variable Loading

```python
# How environment variables are loaded

from dotenv import load_dotenv
import os

# 1. Load from .env file (if exists)
load_dotenv()

# 2. Access with fallback
api_key = os.getenv("GOOGLE_API_KEY", "default_value")

# 3. Type conversion
temperature = float(os.getenv("TEMPERATURE", "0.0"))
max_retries = int(os.getenv("MAX_RETRIES", "3"))
enable_feature = os.getenv("ENABLE_FEATURE", "false").lower() == "true"
```

---

## Configuration File (config.py)

### Understanding config.py

```python
# config.py - Configuration schema with validation

from pydantic import BaseModel, Field, field_validator

class AppConfig(BaseModel):
    """
    Application configuration with Pydantic validation.
    
    Why Pydantic?
    - Type validation (prevents runtime errors)
    - Default values
    - Documentation
    - IDE autocomplete
    """
    
    # Example field with validation
    temperature: float = Field(
        default=float(os.getenv("TEMPERATURE", "0.0")),
        ge=0.0,  # Greater than or equal to 0.0
        le=2.0,  # Less than or equal to 2.0
        description="Model temperature"
    )
    
    # Custom validation
    @field_validator('log_level')
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Ensure log level is valid."""
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        v = v.upper()
        if v not in valid_levels:
            raise ValueError(f"Log level must be one of {valid_levels}")
        return v
```

### Using Configuration

```python
# Method 1: Import global config
from config import config

print(f"Model: {config.model_name}")
print(f"Temperature: {config.temperature}")

# Method 2: Get fresh instance
from config import get_config

config = get_config()
print(f"Timeout: {config.timeout}")

# Method 3: Use in classes
from config import AppConfig

class MyAgent:
    def __init__(self, config: AppConfig = None):
        self.config = config or get_config()
        print(f"Using model: {self.config.model_name}")
```

### Modifying Configuration

```python
# Option 1: Environment variables (recommended)
# Set in .env file or shell
export MODEL_NAME=gemini-1.5-pro

# Option 2: Programmatically (for testing)
from config import config

config.model_name = "gemini-1.5-flash"
config.temperature = 0.5

# Option 3: Create custom config
from config import AppConfig

custom_config = AppConfig(
    model_name="gemini-1.5-pro",
    temperature=0.7,
    max_retries=5
)
```

---

## LLM Configuration

### Model Selection Guide

| Model | Speed | Quality | Cost | Use Case |
|-------|-------|---------|------|----------|
| `gemini-2.0-flash-exp` | ⚡⚡⚡ | ⭐⭐⭐ | $ | **Recommended** - Fast, good quality |
| `gemini-1.5-flash` | ⚡⚡ | ⭐⭐⭐ | $ | Stable alternative |
| `gemini-1.5-pro` | ⚡ | ⭐⭐⭐⭐⭐ | $$$ | Complex reasoning needed |

**Example Configuration:**

```bash
# Fast and efficient (recommended)
MODEL_NAME=gemini-2.0-flash-exp
TEMPERATURE=0.0

# Higher quality for complex tasks
MODEL_NAME=gemini-1.5-pro
TEMPERATURE=0.3

# Creative responses
MODEL_NAME=gemini-1.5-flash
TEMPERATURE=0.9
```

### Temperature Settings

```python
"""
Temperature controls randomness in responses.

0.0 = Deterministic, consistent
    - Best for: Code analysis, structured data extraction
    - Example: "Parse this JSON" → same result every time

0.3-0.5 = Slightly creative
    - Best for: Documentation generation, explanations
    - Example: "Explain this function" → varied but consistent

0.7-1.0 = Creative
    - Best for: Brainstorming, ideation
    - Example: "Suggest improvements" → diverse ideas

1.0-2.0 = Very creative
    - Best for: Creative writing, exploration
    - Example: "Generate code alternatives" → highly varied
"""

# Set in .env
TEMPERATURE=0.0  # For production consistency
```

### Retry Configuration

```python
"""
Retry configuration handles transient failures.

Scenarios:
- Network hiccups
- Rate limiting (429 errors)
- Temporary service issues
"""

# .env settings
MAX_RETRIES=3           # Number of retry attempts
TIMEOUT=60.0           # Seconds to wait per request

# How it works:
# Attempt 1: Immediate
# Attempt 2: Wait ~1 second
# Attempt 3: Wait ~2 seconds
# Attempt 4: Wait ~4 seconds (exponential backoff)
```

**Advanced Retry Configuration:**

```python
# config.py - Add custom retry settings

class AppConfig(BaseModel):
    # ... existing fields ...
    
    retry_min_seconds: int = Field(
        default=int(os.getenv("RETRY_MIN_SECONDS", "1")),
        description="Minimum retry delay"
    )
    retry_max_seconds: int = Field(
        default=int(os.getenv("RETRY_MAX_SECONDS", "10")),
        description="Maximum retry delay"
    )
    retry_multiplier: float = Field(
        default=float(os.getenv("RETRY_MULTIPLIER", "2.0")),
        description="Backoff multiplier"
    )
```

---

## GitHub Integration

### GitHub Token Setup

**Why do you need a token?**
- Access private repositories
- Higher rate limits (5000 req/hour vs 60 req/hour)
- Required for write operations

**Creating a token:**

1. Go to [GitHub Settings → Tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Select scopes:
   - `repo` - For private repository access
   - `public_repo` - For public repository access
   - `read:org` - To read organization data
4. Generate and copy the token

**Add to .env:**
```bash
GITHUB_TOKEN=ghp_YourActualTokenHere1234567890
```

### GitHub API Configuration

```bash
# Default (GitHub.com)
GITHUB_API_URL=https://api.github.com

# GitHub Enterprise
GITHUB_API_URL=https://github.yourcompany.com/api/v3
```

### Using GitHub Configuration

```python
# In your tools
from config import config

def clone_repository(owner: str, repo: str):
    """Clone repository using configured token."""
    
    # Build authenticated URL
    if config.github_token:
        url = f"https://{config.github_token}@github.com/{owner}/{repo}.git"
    else:
        url = f"https://github.com/{owner}/{repo}.git"
    
    # Use configured API URL
    api_url = f"{config.github_api_url}/repos/{owner}/{repo}"
```

---

## Agent Configuration

### Checkpointing (Conversation Memory)

```bash
# Enable conversation memory
ENABLE_CHECKPOINTING=true
```

**What does checkpointing do?**

```python
# With checkpointing (ENABLE_CHECKPOINTING=true)
agent = GithubAgent(enable_checkpointing=True)

result1 = agent.run("Read repository microsoft/vscode")
# Agent: "I analyzed microsoft/vscode..."

result2 = agent.run("What languages does it use?")
# Agent: "Based on the repository I just analyzed, it uses TypeScript, JavaScript..."
# ✓ Agent remembers previous context

# Without checkpointing (ENABLE_CHECKPOINTING=false)
agent = GithubAgent(enable_checkpointing=False)

result1 = agent.run("Read repository microsoft/vscode")
result2 = agent.run("What languages does it use?")
# Agent: "I don't have information about any specific repository..."
# ✗ Agent doesn't remember
```

**Memory backends:**

```python
# Development: In-memory (MemorySaver)
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()
# Pros: Fast, simple
# Cons: Lost on restart, not shared across processes

# Production: Redis
from langgraph.checkpoint.redis import RedisSaver

checkpointer = RedisSaver.from_conn_string(
    os.getenv("REDIS_URL", "redis://localhost:6379/0")
)
# Pros: Persistent, shared, scalable
# Cons: Requires Redis server

# Production: PostgreSQL
from langgraph.checkpoint.postgres import PostgresSaver

checkpointer = PostgresSaver.from_conn_string(
    os.getenv("POSTGRES_URL")
)
# Pros: Persistent, SQL queries on state
# Cons: Requires PostgreSQL
```

### Max Iterations

```bash
# Prevent infinite loops
MAX_ITERATIONS=15
```

**What are iterations?**

```
User: "Read repository microsoft/vscode"

Iteration 1: Agent decides to use read_repository tool
Iteration 2: Tool executes, returns results
Iteration 3: Agent processes results
Iteration 4: Agent formulates final response
→ Total: 4 iterations

If agent gets stuck in a loop:
Iteration 1-5: Valid reasoning
Iteration 6-15: Repeating same steps
At iteration 16: Stops with error
```

**Tuning guidelines:**

- Simple queries: 5-10 iterations
- Complex multi-step: 15-20 iterations
- Very complex: 25-30 iterations

---

## Logging and Monitoring

### Log Levels

```bash
# Development
LOG_LEVEL=DEBUG    # Everything (verbose)

# Staging
LOG_LEVEL=INFO     # Important events

# Production
LOG_LEVEL=WARNING  # Only warnings and errors
```

**Log level comparison:**

```python
import logging

# DEBUG - Detailed diagnostic info
logger.debug(f"Processing file {filename} with config {config}")

# INFO - Confirmation things are working
logger.info("Agent successfully processed 5 repositories")

# WARNING - Something unexpected but recoverable
logger.warning("API rate limit approaching (450/1000 used)")

# ERROR - Something failed but application continues
logger.error(f"Failed to clone repository {repo}: {error}")

# CRITICAL - Severe error, application may not continue
logger.critical("Database connection lost, shutting down")
```

### LangSmith Integration (Production Monitoring)

**What is LangSmith?**
- Observability platform for LLM applications
- Track agent execution, costs, performance
- Debug failures in production

**Setup:**

1. Create account at [smith.langchain.com](https://smith.langchain.com/)
2. Get API key from settings
3. Configure .env:

```bash
ENABLE_TRACING=true
LANGSMITH_API_KEY=ls__your_api_key_here
LANGSMITH_PROJECT=codebaseopsai-production
```

**What you get:**

```
LangSmith Dashboard shows:
- Every agent invocation
- Token usage and cost
- Latency per step
- Tool calls and results
- Error traces
- Performance trends
```

**Example code:**

```python
from config import config

if config.enable_tracing:
    import os
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"] = config.langsmith_api_key
    os.environ["LANGCHAIN_PROJECT"] = config.langsmith_project

# Now all agent calls are traced automatically
agent = GithubAgent()
result = agent.run("query")  # Automatically tracked in LangSmith
```

**External Reference:** [LangSmith Documentation](https://docs.smith.langchain.com/)

---

## Environment-Specific Settings

### Development Environment

```bash
# .env.development

# Use cheaper, faster model
MODEL_NAME=gemini-2.0-flash-exp
TEMPERATURE=0.0

# Verbose logging
LOG_LEVEL=DEBUG

# In-memory checkpointing
ENABLE_CHECKPOINTING=true

# No tracing (keep it simple)
ENABLE_TRACING=false

# Short timeouts (fail fast)
TIMEOUT=30.0
MAX_RETRIES=2
```

### Staging Environment

```bash
# .env.staging

# Production-like model
MODEL_NAME=gemini-2.0-flash-exp
TEMPERATURE=0.0

# Moderate logging
LOG_LEVEL=INFO

# Redis checkpointing
ENABLE_CHECKPOINTING=true
REDIS_URL=redis://staging-redis:6379/0

# Enable tracing
ENABLE_TRACING=true
LANGSMITH_API_KEY=${LANGSMITH_API_KEY}
LANGSMITH_PROJECT=codebaseopsai-staging

# Production-like timeouts
TIMEOUT=60.0
MAX_RETRIES=3
```

### Production Environment

```bash
# .env.production

# Optimized model
MODEL_NAME=gemini-2.0-flash-exp
TEMPERATURE=0.0

# Minimal logging (performance)
LOG_LEVEL=WARNING

# PostgreSQL checkpointing (persistent, queryable)
ENABLE_CHECKPOINTING=true
POSTGRES_URL=postgresql://user:pass@prod-db:5432/codebaseopsai

# Full tracing
ENABLE_TRACING=true
LANGSMITH_API_KEY=${LANGSMITH_API_KEY}
LANGSMITH_PROJECT=codebaseopsai-production

# Generous timeouts (user experience)
TIMEOUT=120.0
MAX_RETRIES=5

# Performance tuning
WORKER_CONCURRENCY=8
MAX_CONCURRENT_REQUESTS=200
```

### Loading Environment-Specific Config

```bash
# Method 1: Use different .env files
cp .env.development .env    # Development
cp .env.staging .env        # Staging
cp .env.production .env     # Production

# Method 2: Environment variable override
export ENV=production
python main.py

# Method 3: Docker Compose
# docker-compose.yml
services:
  app:
    env_file:
      - .env.${ENV:-development}
```

---

## Security Best Practices

### Protecting Secrets

```bash
# ✓ DO: Use .env file (add to .gitignore)
# .gitignore
.env
.env.*
!.env.example

# ✗ DON'T: Hardcode secrets
api_key = "AIzaSyD..."  # NEVER DO THIS

# ✗ DON'T: Commit .env to git
git add .env  # NEVER DO THIS
```

### .env.example Template

```bash
# .env.example - Safe to commit

# =============================================================================
# LLM Configuration
# =============================================================================

GOOGLE_API_KEY=your_api_key_here

# =============================================================================
# GitHub Configuration (optional)
# =============================================================================

# GITHUB_TOKEN=your_github_token_here

# ... more example values ...
```

### Validating Secrets at Startup

```python
# config.py

class AppConfig(BaseModel):
    google_api_key: str = Field(
        default_factory=lambda: os.getenv("GOOGLE_API_KEY", ""),
        description="Google API Key"
    )
    
    @field_validator('google_api_key')
    @classmethod
    def validate_api_key(cls, v: str) -> str:
        """Ensure API key is present and valid format."""
        if not v:
            raise ValueError(
                "GOOGLE_API_KEY is required. "
                "Get one from https://aistudio.google.com/app/apikey"
            )
        
        if not v.startswith("AIzaSy"):
            raise ValueError(
                "GOOGLE_API_KEY has invalid format. "
                "It should start with 'AIzaSy'"
            )
        
        return v
```

### Environment Variable Best Practices

```python
# ✓ DO: Use descriptive names
GOOGLE_API_KEY=...
GITHUB_TOKEN=...
DATABASE_URL=...

# ✗ DON'T: Use ambiguous names
API_KEY=...  # Which API?
TOKEN=...    # Which token?
URL=...      # Which URL?

# ✓ DO: Group related settings
# GitHub settings
GITHUB_TOKEN=...
GITHUB_API_URL=...

# Database settings
DB_HOST=...
DB_PORT=...
DB_NAME=...

# ✗ DON'T: Use random organization
TOKEN1=...
URL2=...
KEY3=...
```

---

## Performance Tuning

### Response Time Optimization

```bash
# Faster model
MODEL_NAME=gemini-2.0-flash-exp  # vs gemini-1.5-pro

# Lower temperature (less sampling)
TEMPERATURE=0.0  # vs 0.7

# Shorter timeout for faster failure
TIMEOUT=30.0  # vs 120.0

# Reduce max iterations
MAX_ITERATIONS=10  # vs 20
```

### Concurrency Settings

```python
# For API server (api_server.py)

# Number of worker processes
WORKER_CONCURRENCY=4  # = number of CPU cores

# Max concurrent requests per worker
MAX_CONCURRENT_REQUESTS=100

# Connection pool size (if using database)
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=10
```

### Caching Configuration

```python
# Add to config.py

class AppConfig(BaseModel):
    # ... existing fields ...
    
    # Enable result caching
    enable_cache: bool = Field(
        default=os.getenv("ENABLE_CACHE", "true").lower() == "true",
        description="Enable result caching"
    )
    
    # Cache TTL (time to live) in seconds
    cache_ttl: int = Field(
        default=int(os.getenv("CACHE_TTL", "3600")),  # 1 hour
        description="Cache expiration time"
    )
    
    # Cache backend
    cache_backend: str = Field(
        default=os.getenv("CACHE_BACKEND", "memory"),  # or "redis"
        description="Cache storage backend"
    )
```

### Memory Management

```python
# Limit checkpointer memory usage

class AppConfig(BaseModel):
    # ... existing fields ...
    
    # Max threads to keep in memory
    max_checkpoint_threads: int = Field(
        default=int(os.getenv("MAX_CHECKPOINT_THREADS", "1000")),
        description="Maximum conversation threads to cache"
    )
    
    # Checkpoint cleanup interval
    checkpoint_cleanup_interval: int = Field(
        default=int(os.getenv("CHECKPOINT_CLEANUP_INTERVAL", "3600")),
        description="Seconds between checkpoint cleanup"
    )
```

---

## Troubleshooting Configuration

### Configuration Not Loading

**Problem:** Environment variables not being read.

**Diagnosis:**

```python
# test_config.py
import os
from dotenv import load_dotenv

print("Before load_dotenv:")
print(f"  GOOGLE_API_KEY: {os.getenv('GOOGLE_API_KEY')}")

load_dotenv()

print("\nAfter load_dotenv:")
print(f"  GOOGLE_API_KEY: {os.getenv('GOOGLE_API_KEY')}")

# Check .env file location
from pathlib import Path
env_path = Path(".env")
print(f"\n.env exists: {env_path.exists()}")
print(f".env path: {env_path.absolute()}")
```

**Solutions:**

1. Ensure `.env` is in project root (same directory as `main.py`)
2. Check `.env` file format (no quotes, no spaces around `=`)
3. Restart Python process after changing `.env`

### Validation Errors

**Problem:** Pydantic validation fails.

```python
# Error example
pydantic_core._pydantic_core.ValidationError: 1 validation error for AppConfig
temperature
  Input should be less than or equal to 2.0 [type=less_than_equal, input_value=3.0, input_type=float]
```

**Solution:**

```python
# Check your .env values
TEMPERATURE=0.5  # ✓ Valid (0.0 - 2.0)
TEMPERATURE=3.0  # ✗ Invalid (exceeds 2.0)

# Check type conversion
MAX_RETRIES=3    # ✓ Valid integer
MAX_RETRIES=abc  # ✗ Invalid (not an integer)
```

### Configuration Not Applied

**Problem:** Changes to `.env` don't take effect.

**Common causes:**

1. **Cached config:**
   ```python
   # Config is loaded once at import
   from config import config  # Loaded here
   
   # Changing .env after this has no effect
   ```

2. **Environment variable override:**
   ```bash
   # Shell environment overrides .env
   export MODEL_NAME=override-value
   
   # .env value ignored
   MODEL_NAME=env-file-value
   ```

**Solutions:**

```python
# Option 1: Reload config explicitly
from config import AppConfig
config = AppConfig()  # Fresh instance

# Option 2: Restart application
# Changes only take effect on restart

# Option 3: Use explicit env file
from dotenv import load_dotenv
load_dotenv(override=True)  # Reload and override
```

---

## Configuration Examples

### Minimal Configuration

```bash
# .env - Bare minimum

GOOGLE_API_KEY=your_key_here
```

### Recommended Development

```bash
# .env - Good development setup

GOOGLE_API_KEY=your_key_here
MODEL_NAME=gemini-2.0-flash-exp
TEMPERATURE=0.0
LOG_LEVEL=INFO
ENABLE_CHECKPOINTING=true
```

### Full Production

```bash
# .env - Complete production setup

# LLM
GOOGLE_API_KEY=${GOOGLE_API_KEY}
MODEL_NAME=gemini-2.0-flash-exp
TEMPERATURE=0.0
MAX_RETRIES=5
TIMEOUT=120.0

# GitHub
GITHUB_TOKEN=${GITHUB_TOKEN}
GITHUB_API_URL=https://api.github.com

# Agent
ENABLE_CHECKPOINTING=true
MAX_ITERATIONS=20

# Logging
LOG_LEVEL=WARNING

# Tracing
ENABLE_TRACING=true
LANGSMITH_API_KEY=${LANGSMITH_API_KEY}
LANGSMITH_PROJECT=codebaseopsai-prod

# State persistence
POSTGRES_URL=postgresql://user:pass@db:5432/codebaseopsai

# Performance
WORKER_CONCURRENCY=8
MAX_CONCURRENT_REQUESTS=200
ENABLE_CACHE=true
CACHE_TTL=3600
```

---

**Document Information:**
- **Created:** January 2, 2026
- **Version:** 1.0
- **Lines:** 900+
- **Related:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md), [DEPLOYMENT.md](../deployment/DEPLOYMENT.md)

**External References:**
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [python-dotenv Documentation](https://github.com/theskumar/python-dotenv)
- [Google AI API Keys](https://aistudio.google.com/app/apikey)
- [GitHub Personal Access Tokens](https://github.com/settings/tokens)
- [LangSmith Setup](https://docs.smith.langchain.com/)
