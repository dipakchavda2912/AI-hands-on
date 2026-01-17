# Configuration Guide

Complete guide to configuring and customizing CodeBaseOpsAI-v2-1, including environment setup, agent parameters, Node.js configuration, NPM registry settings, and best practices.

---

## Table of Contents

1. [Overview](#overview)
2. [Environment Setup](#environment-setup)
3. [Node.js LTS Version Configuration](#nodejs-lts-version-configuration)
4. [NPM Registry Configuration](#npm-registry-configuration)
5. [Agent Parameters and Settings](#agent-parameters-and-settings)
6. [InstructionService Configuration](#instructionservice-configuration)
7. [Package Manager Selection](#package-manager-selection)
8. [Repository Configuration](#repository-configuration)
9. [Tool Configuration](#tool-configuration)
10. [Advanced Configuration](#advanced-configuration)
11. [Best Practices](#best-practices)
12. [Configuration Examples](#configuration-examples)

---

## Overview

CodeBaseOpsAI-v2-1 offers flexible configuration through:
- **Environment variables** for API keys and registry URLs
- **Python constants** for LTS versions and defaults
- **Service parameters** for repository and path settings
- **Tool options** for package management behavior

### Configuration Hierarchy

```
Environment Variables (.env)
    │
    ├─→ GOOGLE_API_KEY (required)
    ├─→ GITHUB_TOKEN (required for GitHub operations)
    ├─→ NPM_REGISTRY (optional, default: https://registry.npmjs.org)
    │
    ▼
Python Configuration (main.py, agent.py, etc.)
    │
    ├─→ node_lts_version (default: 22.11.0)
    ├─→ temperature (default: 0)
    ├─→ max_output_tokens (default: 1024)
    │
    ▼
Service Configuration (InstructionService)
    │
    ├─→ repository
    ├─→ clone_path
    ├─→ branch
    ├─→ packages list
    │
    ▼
Tool Configuration (per tool call)
    │
    ├─→ lock_major
    ├─→ npm_lookup
    ├─→ manager
    ├─→ dry_run
```

---

## Environment Setup

### Required Environment Variables

#### 1. GOOGLE_API_KEY

**Purpose**: Authenticate with Google Gemini API

**Obtain from**: [Google AI Studio](https://makersuite.google.com/app/apikey)

**Setup**:

```bash
# .env file
GOOGLE_API_KEY=AIzaSy...your-key-here...
```

Or:

```bash
# Export in shell
export GOOGLE_API_KEY="AIzaSy...your-key-here..."
```

**Validation**:

```python
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not set in environment")

print(f"API Key configured: {api_key[:10]}...")
# Output: API Key configured: AIzaSyXXXX...
```

**Security best practices**:
- Never commit `.env` to version control
- Add `.env` to `.gitignore`
- Use different keys for dev/staging/production
- Rotate keys regularly

#### 2. GITHUB_TOKEN

**Purpose**: Authenticate with GitHub API for repository operations

**Obtain from**: [GitHub Personal Access Tokens](https://github.com/settings/tokens)

**Required permissions**:
- `repo` (Full control of private repositories)
- `read:org` (Read org and team membership, if needed)

**Setup**:

```bash
# .env file
GITHUB_TOKEN=ghp_...your-token-here...
```

Or:

```bash
# Export in shell
export GITHUB_TOKEN="ghp_...your-token-here..."
```

**Validation**:

```python
import os
from github import Github

github_token = os.getenv("GITHUB_TOKEN")
if not github_token:
    raise ValueError("GITHUB_TOKEN not set in environment")

# Test authentication
g = Github(github_token)
user = g.get_user()
print(f"Authenticated as: {user.login}")
# Output: Authenticated as: yourusername
```

**Token types**:
- **Personal Access Token (classic)**: Traditional, fine-grained control
- **Fine-grained personal access token**: New, more secure, per-repository
- **GitHub App token**: For automated systems

### Optional Environment Variables

#### 3. NPM_REGISTRY

**Purpose**: Specify custom NPM registry URL

**Default**: `https://registry.npmjs.org`

**Setup for private registry**:

```bash
# .env file
NPM_REGISTRY=https://registry.company.com
```

**Use cases**:
- Private npm registry (Artifactory, Nexus)
- Company-internal packages
- Mirror/proxy registry
- Offline/air-gapped environments

**Validation**:

```python
import os
import requests

npm_registry = os.getenv("NPM_REGISTRY", "https://registry.npmjs.org")
print(f"Using registry: {npm_registry}")

# Test registry access
try:
    response = requests.get(f"{npm_registry}/express", timeout=10)
    response.raise_for_status()
    print("✅ Registry accessible")
except Exception as e:
    print(f"❌ Registry error: {e}")
```

### .env File Template

Create a `.env` file in your project root:

```bash
# .env

# Required: Google Gemini API Key
GOOGLE_API_KEY=AIzaSy...

# Required: GitHub Personal Access Token
GITHUB_TOKEN=ghp_...

# Optional: Custom NPM Registry
# NPM_REGISTRY=https://registry.npmjs.org

# Optional: Custom OSV API endpoint
# OSV_API=https://api.osv.dev/v1/query
```

### Loading Environment Variables

```python
# main.py
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Verify required variables
required_vars = ["GOOGLE_API_KEY", "GITHUB_TOKEN"]
missing = [var for var in required_vars if not os.getenv(var)]

if missing:
    raise EnvironmentError(
        f"Missing required environment variables: {', '.join(missing)}\n"
        "Please create a .env file with these variables."
    )

print("✅ Environment configuration loaded")
```

### Environment-Specific Configuration

**Development**:

```bash
# .env.development
GOOGLE_API_KEY=AIzaSy...dev-key...
GITHUB_TOKEN=ghp_...dev-token...
NPM_REGISTRY=https://registry.npmjs.org
```

**Production**:

```bash
# .env.production
GOOGLE_API_KEY=AIzaSy...prod-key...
GITHUB_TOKEN=ghp_...prod-token...
NPM_REGISTRY=https://registry.company.com
```

**Loading**:

```python
import os
from dotenv import load_dotenv

env = os.getenv("ENVIRONMENT", "development")
env_file = f".env.{env}"

load_dotenv(env_file)
print(f"Loaded configuration from {env_file}")
```

---

## Node.js LTS Version Configuration

### What is Node.js LTS?

**LTS (Long Term Support)**: Stable Node.js releases with:
- 3 years of active support
- Security updates
- Critical bug fixes
- Production-ready stability

**Current LTS versions** (2026):
- **Node.js 22.x (Iron)** - Current LTS (2024-2027)
- **Node.js 20.x (Hydrogen)** - Maintenance (2022-2025)
- **Node.js 18.x** - End of maintenance (2021-2025)

### Setting LTS Version

#### In main.py

```python
# main.py
class Main():
    # Set Node.js LTS version for all package operations
    node_lts_version = '22.11.0'  # Current LTS
    
    def __init__(self):
        self.agent_instance = Agent(node_lts_version=self.node_lts_version)
```

**Why hardcode?**
- Ensures consistency across all operations
- Predictable package selection
- Clear documentation of target environment

#### Alternative: From Environment

```python
# main.py
import os
from dotenv import load_dotenv

load_dotenv()

class Main():
    # Read from environment with fallback
    node_lts_version = os.getenv('NODE_LTS_VERSION', '22.11.0')
    
    def __init__(self):
        print(f"Using Node.js LTS: {self.node_lts_version}")
        self.agent_instance = Agent(node_lts_version=self.node_lts_version)
```

```bash
# .env
NODE_LTS_VERSION=22.11.0
```

#### Alternative: From package.json

```python
# Read from package.json engines.node
import json
from pathlib import Path

def detect_node_lts_from_package_json(pkg_path: Path) -> str:
    """Detect Node.js LTS version from package.json."""
    try:
        with open(pkg_path) as f:
            pkg = json.load(f)
        
        node_range = pkg.get("engines", {}).get("node", "")
        
        # Extract minimum version from range
        # e.g., ">=18.0.0" -> "18.0.0"
        if ">=" in node_range:
            version = node_range.split(">=")[1].split()[0]
            return version.strip()
        
    except Exception as e:
        print(f"Could not detect from package.json: {e}")
    
    return "22.11.0"  # Fallback

# Usage
node_lts_version = detect_node_lts_from_package_json(Path("package.json"))
```

### Version Format

**Supported formats**:
- `22.11.0` ✅ (recommended)
- `v22.11.0` ✅ (will be normalized)
- `22.11` ❌ (use full version)
- `22` ❌ (use full version)

**Normalization**:

```python
def normalize_node_version(version: str) -> str:
    """Normalize Node.js version string."""
    # Remove 'v' prefix
    version = version.lstrip('v')
    
    # Ensure three parts (major.minor.patch)
    parts = version.split('.')
    if len(parts) == 2:
        parts.append('0')  # Add patch version
    elif len(parts) == 1:
        parts.extend(['0', '0'])  # Add minor and patch
    
    return '.'.join(parts[:3])

# Examples
normalize_node_version("v22.11.0")  # -> "22.11.0"
normalize_node_version("22.11")     # -> "22.11.0"
normalize_node_version("22")        # -> "22.0.0"
```

### Version Selection Strategy

#### Conservative (Default)

```python
node_lts_version = '22.11.0'  # Latest LTS
```

**Use when**:
- New projects
- Maximum compatibility
- Latest features needed

#### Moderate

```python
node_lts_version = '20.11.0'  # Previous LTS
```

**Use when**:
- Existing infrastructure on Node 20
- Dependencies not yet compatible with Node 22
- Corporate standardization

#### Legacy

```python
node_lts_version = '18.18.0'  # Older LTS
```

**Use when**:
- Legacy applications
- Dependencies require older Node.js
- Maintaining existing systems

### Impact on Package Selection

The `node_lts_version` affects:

1. **Version filtering**: Only compatible versions selected
2. **Compatibility checks**: `engines.node` validation
3. **Instruction generation**: Version included in prompts

**Example**:

```python
# With node_lts_version = "22.11.0"
choose_best_version("express", "^4.17.0", "22.11.0", True, packument)
# Checks: express@4.18.2 has engines.node: ">= 0.10.0"
# Result: Compatible! ✅

# With node_lts_version = "10.0.0" (old)
choose_best_version("webpack", "^5.0.0", "10.0.0", True, packument)
# Checks: webpack@5.88.0 has engines.node: ">= 10.13.0"
# Result: Compatible! ✅

# With node_lts_version = "8.0.0" (very old)
choose_best_version("webpack", "^5.0.0", "8.0.0", True, packument)
# Checks: webpack@5.88.0 has engines.node: ">= 10.13.0"
# Result: Incompatible! ❌ Skips this version
```

### Updating LTS Version

**When to update**:
- New LTS release available
- Current LTS nearing end-of-life
- Dependencies require newer Node.js

**Update process**:

1. **Test locally**:
   ```bash
   nvm install 22.11.0
   nvm use 22.11.0
   npm install
   npm test
   ```

2. **Update configuration**:
   ```python
   # main.py
   node_lts_version = '22.11.0'  # Updated from 20.11.0
   ```

3. **Update .nvmrc**:
   ```bash
   echo "22.11.0" > .nvmrc
   ```

4. **Update package.json**:
   ```json
   {
     "engines": {
       "node": ">=22.0.0 <23.0.0"
     }
   }
   ```

5. **Test package updates**:
   ```python
   # Run with dry_run first
   tools.update_packages(dry_run=True)
   ```

---

## NPM Registry Configuration

### Default Registry

```python
NPM_REGISTRY = "https://registry.npmjs.org"
```

**Features**:
- Public npm packages
- ~2 million packages
- Free access
- Worldwide CDN

### Custom Registry

#### Configuration Methods

**Method 1: Environment Variable** (recommended)

```bash
# .env
NPM_REGISTRY=https://registry.company.com
```

**Method 2: Direct Initialization**

```python
# In Agent or Main
tools = PackageUpdatesTools(
    node_lts_version="22.11.0",
    npm_registry="https://registry.company.com"
)
```

**Method 3: Default Parameter**

```python
# In PackageUpdatesTools
def __init__(self, node_lts_version: str, npm_registry: str | None = None):
    self.npm_registry = npm_registry or os.getenv(
        "NPM_REGISTRY",
        "https://registry.company.com"  # Custom default
    )
```

### Private Registry Setup

#### Artifactory

```bash
# .env
NPM_REGISTRY=https://artifactory.company.com/artifactory/api/npm/npm-repo
```

**Authentication** (if required):

```bash
# .npmrc
//artifactory.company.com/artifactory/api/npm/npm-repo/:_authToken=your-token
```

#### Nexus

```bash
# .env
NPM_REGISTRY=https://nexus.company.com/repository/npm-public
```

#### Verdaccio (Self-hosted)

```bash
# .env
NPM_REGISTRY=http://localhost:4873
```

### Registry Authentication

For private registries requiring authentication:

```python
import requests

def fetch_packument(name: str, registry: str, auth_token: str | None = None) -> Dict:
    """Fetch packument with optional authentication."""
    url = f"{registry}/{name}"
    headers = {"Accept": "application/vnd.npm.install-v1+json"}
    
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"
    
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()
```

**Configuration**:

```bash
# .env
NPM_REGISTRY=https://registry.company.com
NPM_AUTH_TOKEN=your-auth-token-here
```

### Registry Fallback

Support multiple registries:

```python
class PackageUpdatesUtils:
    REGISTRIES = [
        "https://registry.company.com",      # Try private first
        "https://registry.npmjs.org"         # Fallback to public
    ]
    
    @staticmethod
    def fetch_packument(name: str) -> Dict:
        """Fetch from first available registry."""
        last_error = None
        
        for registry in PackageUpdatesUtils.REGISTRIES:
            try:
                url = f"{registry}/{name}"
                resp = requests.get(url, timeout=10)
                resp.raise_for_status()
                return resp.json()
            except Exception as e:
                last_error = e
                continue
        
        raise last_error or Exception("All registries failed")
```

### Registry Health Check

```python
def check_registry_health(registry_url: str) -> bool:
    """Check if npm registry is accessible."""
    try:
        # Try to fetch a common package
        response = requests.get(
            f"{registry_url}/express",
            timeout=10
        )
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Registry health check failed: {e}")
        return False

# Usage
npm_registry = os.getenv("NPM_REGISTRY", "https://registry.npmjs.org")
if check_registry_health(npm_registry):
    print(f"✅ Registry {npm_registry} is accessible")
else:
    print(f"❌ Registry {npm_registry} is not accessible")
```

---

## Agent Parameters and Settings

### LLM Configuration

#### Model Selection

```python
# agent.py
def init_llm(self) -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",  # Model name
        temperature=0,              # Determinism level
        max_output_tokens=1024,     # Response length limit
        api_key=os.getenv("GOOGLE_API_KEY")
    )
```

**Available models**:
- `gemini-2.5-flash` (recommended) - Fast, efficient
- `gemini-2.5-pro` - More capable, slower
- `gemini-1.5-flash` - Previous generation
- `gemini-1.5-pro` - Previous generation

**Model selection criteria**:

| Model | Speed | Quality | Cost | Use Case |
|-------|-------|---------|------|----------|
| gemini-2.5-flash | ⚡⚡⚡ | ⭐⭐⭐ | $ | Production, frequent operations |
| gemini-2.5-pro | ⚡⚡ | ⭐⭐⭐⭐⭐ | $$$ | Complex reasoning, critical tasks |

#### Temperature Setting

```python
temperature=0  # Default: deterministic
```

**Temperature range**: 0.0 to 1.0

**Effects**:

| Temperature | Behavior | Use Case |
|-------------|----------|----------|
| 0.0 | Deterministic, consistent | ✅ Production (recommended) |
| 0.3 | Slightly varied | Development, testing |
| 0.7 | Creative, varied | Exploration |
| 1.0 | Very creative | Not recommended for automation |

**Why temperature=0?**
- Consistent results across runs
- Predictable tool selection
- Reliable automation
- Easier debugging

#### Max Output Tokens

```python
max_output_tokens=1024  # Default
```

**Considerations**:

| Tokens | Approximate Output | Use Case |
|--------|-------------------|----------|
| 512 | ~400 words | Short responses |
| 1024 | ~800 words | ✅ Default (recommended) |
| 2048 | ~1600 words | Complex explanations |
| 4096 | ~3200 words | Very detailed responses |

**Why 1024?**
- Sufficient for tool responses
- Prevents excessively long outputs
- Cost-effective
- Fast generation

**Adjust if**:
- Getting truncated responses (increase)
- Responses too verbose (decrease)
- Need detailed explanations (increase to 2048)

### Agent Prompt Configuration

```python
# agent_prompt.py
class AgentPropmpt:
    def get_prompt_text(self) -> str:
        return '''You are a helpful assistant with access to specific tools.
        
        Available tools:
        {tools}
        
        Tool names: {tool_names}
        
        Follow this reasoning pattern:
        
        Question: {input}
        
        Think step by step:
        Thought: Consider what needs to be done
        Action: Choose a tool from [{tool_names}]
        Action Input: Provide input for the chosen tool
        Observation: See the tool's result
        ... repeat Thought/Action/Action Input/Observation as needed ...
        Thought: Formulate the final conclusion
        Final Answer: Provide the complete answer
        
        {agent_scratchpad}'''
```

**Customization points**:

1. **Add constraints**:
   ```python
   return '''You are a helpful assistant...
   
   IMPORTANT CONSTRAINTS:
   - Always use lock_major=True for production
   - Always run dry_run before applying changes
   - Never skip vulnerability checks unless explicitly told
   
   Available tools:
   {tools}
   ...
   '''
   ```

2. **Add examples**:
   ```python
   return '''...
   
   EXAMPLE:
   Question: Update express to latest version
   Thought: I need to update express package
   Action: update_specific_packages
   Action Input: {{"package_names": ["express"], "lock_major": true}}
   Observation: Updated express: ^4.17.1 -> ^4.18.2
   Final Answer: Successfully updated express to 4.18.2
   
   {input}
   ...
   '''
   ```

3. **Domain-specific guidance**:
   ```python
   return '''You are an expert in Node.js package management...
   
   PACKAGE MANAGEMENT RULES:
   1. Always check Node.js compatibility
   2. Always scan for vulnerabilities
   3. Prefer stable versions over pre-releases
   4. Lock major versions to prevent breaking changes
   
   ...
   '''
   ```

---

## InstructionService Configuration

### Basic Configuration

```python
# main.py
instruction_service = InstructionService(
    repository="owner/repo-name",
    clone_path="/tmp/project-clone/",
    branch="develop",
    node_lts_version="22.11.0"
)
```

### Repository Settings

```python
# GitHub repository
repository = "dipakchavda2912/base-serverless"

# Clone path with timestamp
from datetime import datetime
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
clone_path = f"/tmp/project-{timestamp}/"

# Branch to work with
branch = "develop"  # or "main", "feature/xyz", etc.
```

**Path best practices**:
- Use `/tmp/` for temporary operations
- Include timestamp for uniqueness
- End with `/` for consistency
- Use absolute paths

### Package Configuration

```python
class InstructionService:
    def __init__(self, ...):
        # Define packages to manage
        self.node_packages = [
            # Public packages with npm_lookup
            {
                "name": "express",
                "is_dev": False,
                "npm_lookup": True
            },
            {
                "name": "typescript",
                "is_dev": True,
                "npm_lookup": True
            },
            
            # Private packages without npm_lookup
            {
                "name": "@company/shared-lib",
                "version": "^3.1.2",
                "is_dev": False,
                "npm_lookup": False
            }
        ]
```

**Package dictionary fields**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | str | ✅ Yes | Package name |
| `is_dev` | bool | ❌ No | Dev dependency? (default: False) |
| `npm_lookup` | bool | ❌ No | Use NPM registry? (default: True) |
| `version` | str | ❌ No | Specific version (for npm_lookup=False) |

### Instruction Categories

```python
def get_all_instructions(self) -> List[str]:
    instructions = []
    
    # 1. GitHub operations
    github = GithubInstructions(
        repository=self.repository,
        clone_path=self.clone_path,
        branch=self.branch
    )
    instructions.extend(github.get_instructions())
    
    # 2. Serverless custom configuration
    serverless_custom = ServerlessCustomTagInstructions(
        clone_path=self.clone_path
    )
    instructions.extend(serverless_custom.get_instructions())
    
    # 3. Package updates
    packages = NodeJsPackagesInstructions(
        clone_path=self.clone_path,
        packages=self.node_packages,
        node_lts_version=self.node_lts_version
    )
    instructions.extend(packages.get_instructions())
    
    return instructions
```

**Customization**: Add/remove instruction categories as needed.

### Dynamic Configuration

```python
def get_query(self, config: dict) -> List[str]:
    """Generate instructions from dynamic configuration."""
    instruction_service = InstructionService(
        repository=config.get("repository", "default/repo"),
        clone_path=config.get("clone_path", "/tmp/default/"),
        branch=config.get("branch", "main"),
        node_lts_version=config.get("node_lts_version", "22.11.0")
    )
    
    return instruction_service.get_all_instructions()

# Usage
config = {
    "repository": "myorg/myrepo",
    "clone_path": "/tmp/myrepo-clone/",
    "branch": "feature/updates",
    "node_lts_version": "20.11.0"
}

queries = main.get_query(config)
```

---

## Package Manager Selection

### Default Manager

```python
# Default in schemas
manager: str = Field(default="npm", ...)
```

### Per-Project Configuration

```python
# Detect from lock files
def detect_package_manager(project_path: Path) -> str:
    if (project_path / "pnpm-lock.yaml").exists():
        return "pnpm"
    elif (project_path / "yarn.lock").exists():
        return "yarn"
    elif (project_path / "package-lock.json").exists():
        return "npm"
    return "npm"  # Default

# Usage in InstructionService
class InstructionService:
    def __init__(self, clone_path, ...):
        self.package_manager = detect_package_manager(Path(clone_path))
        print(f"Detected package manager: {self.package_manager}")
```

### Global Configuration

```python
# Set default manager globally
DEFAULT_PACKAGE_MANAGER = "pnpm"

class PackageUpdatesTools:
    def add_package(self, ..., manager: str = DEFAULT_PACKAGE_MANAGER):
        # Use global default
        ...
```

---

## Repository Configuration

### SSH vs HTTPS

**HTTPS** (default):
```python
repository = "owner/repo"  # Converted to https://github.com/owner/repo
```

**SSH**:
```python
repository = "git@github.com:owner/repo.git"  # SSH format
```

### Private Repositories

Requires `GITHUB_TOKEN` with appropriate permissions:

```python
# .env
GITHUB_TOKEN=ghp_...your-token...

# Token must have 'repo' scope for private repos
```

### Multiple Repositories

```python
repositories = [
    {
        "name": "api",
        "url": "owner/api-repo",
        "branch": "develop",
        "clone_path": "/tmp/api/"
    },
    {
        "name": "web",
        "url": "owner/web-repo",
        "branch": "main",
        "clone_path": "/tmp/web/"
    }
]

for repo_config in repositories:
    instructions = InstructionService(
        repository=repo_config["url"],
        clone_path=repo_config["clone_path"],
        branch=repo_config["branch"],
        node_lts_version="22.11.0"
    ).get_all_instructions()
    
    # Process instructions...
```

---

## Tool Configuration

### Common Tool Parameters

```python
# analyze_packages
tools.analyze_packages(
    package_json_path="package.json",  # Path to package.json
    lock_major=True,                    # Lock major versions
    npm_lookup=True                     # Use NPM registry
)

# update_packages
tools.update_packages(
    package_json_path="package.json",
    lock_major=True,
    dry_run=False,        # Actually modify files
    apply_updates=True,   # Run npm install
    manager="npm",        # Package manager
    npm_lookup=True
)

# add_package
tools.add_package(
    package_name="express",
    version=None,         # Auto-select best version
    dev=False,           # Add to dependencies (not devDependencies)
    install=True,        # Run npm install
    manager="npm",
    npm_lookup=True,
    node_lts_version="22.11.0"
)
```

### Configuration Presets

```python
# Conservative preset
CONSERVATIVE_CONFIG = {
    "lock_major": True,
    "dry_run": True,
    "npm_lookup": True,
    "apply_updates": False
}

# Aggressive preset
AGGRESSIVE_CONFIG = {
    "lock_major": False,
    "dry_run": False,
    "npm_lookup": True,
    "apply_updates": True
}

# Production preset
PRODUCTION_CONFIG = {
    "lock_major": True,
    "dry_run": False,
    "npm_lookup": True,
    "apply_updates": True,
    "manager": "npm"
}

# Usage
tools.update_packages(**PRODUCTION_CONFIG)
```

---

## Advanced Configuration

### Custom OSV API Endpoint

```python
# For testing or custom vulnerability database
OSV_API = "https://custom-osv.company.com/v1/query"

def osv_has_vuln(name: str, version: str, osv_api: str = OSV_API):
    # Use custom endpoint
    ...
```

### Request Timeouts

```python
# Adjust timeouts for slow networks
def fetch_packument(name: str, registry: str, timeout: int = 60) -> Dict:
    resp = requests.get(url, headers=headers, timeout=timeout)
    ...

def osv_has_vuln(name: str, version: str, timeout: int = 60) -> bool:
    r = requests.post(osv_api, json=payload, timeout=timeout)
    ...
```

### Retry Logic

```python
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def get_session_with_retries() -> requests.Session:
    """Create session with retry logic."""
    session = requests.Session()
    
    retry_strategy = Retry(
        total=3,                  # Total retries
        backoff_factor=1,         # Wait 1s, 2s, 4s between retries
        status_forcelist=[429, 500, 502, 503, 504]
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session

# Usage
session = get_session_with_retries()
response = session.get(f"{NPM_REGISTRY}/express")
```

### Logging Configuration

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('codebaseops.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Use in code
logger.info(f"Fetching packument for {package_name}")
logger.warning(f"Version {version} has vulnerabilities")
logger.error(f"Failed to update package: {error}")
```

---

## Best Practices

### 1. Use Environment Variables for Secrets

✅ **Good**:
```python
api_key = os.getenv("GOOGLE_API_KEY")
```

❌ **Bad**:
```python
api_key = "AIzaSy..."  # Hardcoded secret
```

### 2. Validate Configuration on Startup

```python
def validate_configuration():
    """Validate all required configuration."""
    errors = []
    
    # Check environment variables
    if not os.getenv("GOOGLE_API_KEY"):
        errors.append("GOOGLE_API_KEY not set")
    
    if not os.getenv("GITHUB_TOKEN"):
        errors.append("GITHUB_TOKEN not set")
    
    # Check Node.js version format
    node_version = Main.node_lts_version
    if not re.match(r'^\d+\.\d+\.\d+$', node_version):
        errors.append(f"Invalid Node.js version format: {node_version}")
    
    if errors:
        raise ValueError(f"Configuration errors:\n" + "\n".join(f"  - {e}" for e in errors))
    
    print("✅ Configuration validated successfully")

# Run on startup
if __name__ == "__main__":
    validate_configuration()
    main = Main()
    main.execute()
```

### 3. Use Configuration Classes

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    """Application configuration."""
    google_api_key: str
    github_token: str
    node_lts_version: str = "22.11.0"
    npm_registry: str = "https://registry.npmjs.org"
    package_manager: str = "npm"
    temperature: float = 0.0
    max_output_tokens: int = 1024
    
    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment."""
        return cls(
            google_api_key=os.getenv("GOOGLE_API_KEY", ""),
            github_token=os.getenv("GITHUB_TOKEN", ""),
            node_lts_version=os.getenv("NODE_LTS_VERSION", "22.11.0"),
            npm_registry=os.getenv("NPM_REGISTRY", "https://registry.npmjs.org")
        )
    
    def validate(self):
        """Validate configuration."""
        if not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY is required")
        if not self.github_token:
            raise ValueError("GITHUB_TOKEN is required")

# Usage
config = Config.from_env()
config.validate()
```

### 4. Document Configuration Changes

```python
# main.py

# Configuration History:
# 2024-01-15: Updated node_lts_version from 20.11.0 to 22.11.0
# 2024-01-10: Added custom NPM registry support
# 2024-01-05: Initial configuration

class Main():
    node_lts_version = '22.11.0'  # Updated 2024-01-15
```

### 5. Use Separate Configs for Environments

```
.env.development
.env.staging
.env.production
```

---

## Configuration Examples

### Example 1: Basic Setup

```bash
# .env
GOOGLE_API_KEY=AIzaSy...
GITHUB_TOKEN=ghp_...
```

```python
# main.py
class Main():
    node_lts_version = '22.11.0'
    
    def get_query(self) -> List[str]:
        instruction_service = InstructionService(
            repository="myorg/myrepo",
            clone_path="/tmp/myrepo/",
            branch="main",
            node_lts_version=self.node_lts_version
        )
        return instruction_service.get_all_instructions()
```

### Example 2: Custom Registry

```bash
# .env
GOOGLE_API_KEY=AIzaSy...
GITHUB_TOKEN=ghp_...
NPM_REGISTRY=https://registry.company.com
```

### Example 3: Multiple Environments

```python
# config.py
import os
from enum import Enum

class Environment(Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

def load_config(env: Environment):
    """Load environment-specific configuration."""
    env_file = f".env.{env.value}"
    load_dotenv(env_file)
    
    return {
        "google_api_key": os.getenv("GOOGLE_API_KEY"),
        "github_token": os.getenv("GITHUB_TOKEN"),
        "node_lts_version": os.getenv("NODE_LTS_VERSION", "22.11.0"),
        "npm_registry": os.getenv("NPM_REGISTRY", "https://registry.npmjs.org")
    }

# Usage
env = Environment.PRODUCTION
config = load_config(env)
```

### Example 4: Complete Configuration

```python
# config.py
from dataclasses import dataclass
import os
from dotenv import load_dotenv

@dataclass
class AppConfig:
    """Complete application configuration."""
    # API Keys
    google_api_key: str
    github_token: str
    
    # Node.js
    node_lts_version: str
    
    # NPM Registry
    npm_registry: str
    npm_auth_token: str | None
    
    # Agent Settings
    llm_model: str
    temperature: float
    max_output_tokens: int
    
    # Package Management
    default_package_manager: str
    lock_major_versions: bool
    
    # Repository Settings
    default_branch: str
    clone_base_path: str
    
    @classmethod
    def load(cls) -> "AppConfig":
        """Load configuration from environment."""
        load_dotenv()
        
        return cls(
            # API Keys
            google_api_key=os.getenv("GOOGLE_API_KEY", ""),
            github_token=os.getenv("GITHUB_TOKEN", ""),
            
            # Node.js
            node_lts_version=os.getenv("NODE_LTS_VERSION", "22.11.0"),
            
            # NPM Registry
            npm_registry=os.getenv("NPM_REGISTRY", "https://registry.npmjs.org"),
            npm_auth_token=os.getenv("NPM_AUTH_TOKEN"),
            
            # Agent Settings
            llm_model=os.getenv("LLM_MODEL", "gemini-2.5-flash"),
            temperature=float(os.getenv("LLM_TEMPERATURE", "0.0")),
            max_output_tokens=int(os.getenv("MAX_OUTPUT_TOKENS", "1024")),
            
            # Package Management
            default_package_manager=os.getenv("PACKAGE_MANAGER", "npm"),
            lock_major_versions=os.getenv("LOCK_MAJOR_VERSIONS", "true").lower() == "true",
            
            # Repository
            default_branch=os.getenv("DEFAULT_BRANCH", "main"),
            clone_base_path=os.getenv("CLONE_BASE_PATH", "/tmp")
        )
    
    def validate(self):
        """Validate required configuration."""
        if not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY is required")
        if not self.github_token:
            raise ValueError("GITHUB_TOKEN is required")
        if not self.node_lts_version:
            raise ValueError("NODE_LTS_VERSION is required")
        
        print("✅ Configuration validated")

# Usage
config = AppConfig.load()
config.validate()
```

---

## Conclusion

Proper configuration is essential for CodeBaseOpsAI-v2-1:

✅ **Use environment variables** for sensitive data
✅ **Validate configuration** on startup
✅ **Document changes** for maintainability
✅ **Use presets** for common scenarios
✅ **Separate environments** (dev/staging/prod)

**Key Configuration Points**:
1. `GOOGLE_API_KEY` - Required for LLM
2. `GITHUB_TOKEN` - Required for GitHub operations
3. `node_lts_version` - Target Node.js version
4. `NPM_REGISTRY` - Optional custom registry
5. `temperature=0` - Deterministic agent behavior

---

**Next Steps**:
- Review [UNDERSTANDING.md](UNDERSTANDING.md) for architecture
- Read [PACKAGE_MANAGEMENT.md](PACKAGE_MANAGEMENT.md) for package features
- Start with [QUICKSTART.md](QUICKSTART.md)

---

*Last Updated: January 17, 2026*
*Version: 2.1*
