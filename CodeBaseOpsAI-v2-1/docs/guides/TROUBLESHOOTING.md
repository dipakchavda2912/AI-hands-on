# 🔧 Troubleshooting Guide - CodeBaseOpsAI-v2-1

**Common issues, solutions, and debugging tips for CodeBaseOpsAI-v2-1.**

---

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [Environment Setup Problems](#environment-setup-problems)
3. [Import Errors](#import-errors)
4. [API Key Issues](#api-key-issues)
5. [Package Management Errors](#package-management-errors)
6. [npm_lookup Failures](#npm_lookup-failures)
7. [Vulnerability Scanning Issues](#vulnerability-scanning-issues)
8. [Agent Execution Errors](#agent-execution-errors)
9. [Tool Execution Failures](#tool-execution-failures)
10. [GitHub Operations Issues](#github-operations-issues)
11. [YAML/JSON Manipulation Errors](#yamljson-manipulation-errors)
12. [Debugging Tips](#debugging-tips)
13. [Performance Issues](#performance-issues)
14. [Advanced Troubleshooting](#advanced-troubleshooting)

---

## Installation Issues

### Issue: `pip install -r requirements.txt` Fails

**Symptoms:**
```
ERROR: Could not find a version that satisfies the requirement langchain==1.2.0
ERROR: Failed building wheel for some-package
```

**Solutions:**

#### 1. Python Version Incompatibility

```bash
# Check your Python version
python --version

# Should be Python 3.11 or higher
# If not, install a newer version
```

**Fix:**
```bash
# Install Python 3.11 or higher
# On macOS with Homebrew:
brew install python@3.11

# Create venv with specific Python version
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### 2. Outdated pip

```bash
# Upgrade pip first
pip install --upgrade pip

# Then try again
pip install -r requirements.txt
```

#### 3. Network/Proxy Issues

```bash
# Use a different PyPI mirror
pip install -r requirements.txt -i https://pypi.org/simple/

# Or set timeout
pip install -r requirements.txt --timeout 100
```

#### 4. Platform-Specific Build Issues

```bash
# Install build dependencies
# On macOS:
xcode-select --install

# On Ubuntu/Debian:
sudo apt-get update
sudo apt-get install python3-dev build-essential

# On Windows:
# Install Microsoft C++ Build Tools from:
# https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

### Issue: Virtual Environment Not Activating

**Symptoms:**
```bash
source .venv/bin/activate
# No (.venv) prefix appears
```

**Solutions:**

#### 1. Wrong Shell

```bash
# For bash/zsh
source .venv/bin/activate

# For fish shell
source .venv/bin/activate.fish

# For Windows PowerShell
.venv\Scripts\Activate.ps1

# For Windows CMD
.venv\Scripts\activate.bat
```

#### 2. Recreate Virtual Environment

```bash
# Remove existing venv
rm -rf .venv

# Create new one
python3 -m venv .venv
source .venv/bin/activate
```

### Issue: ImportError After Installation

**Symptoms:**
```python
ModuleNotFoundError: No module named 'langchain'
```

**Solutions:**

#### 1. Verify Virtual Environment is Active

```bash
# Should show (.venv) prefix
which python
# Should point to: /path/to/project/.venv/bin/python
```

#### 2. Reinstall in Correct Environment

```bash
# Activate venv first
source .venv/bin/activate

# Verify pip location
which pip
# Should point to: /path/to/project/.venv/bin/pip

# Reinstall
pip install -r requirements.txt
```

---

## Environment Setup Problems

### Issue: `.env` File Not Loaded

**Symptoms:**
```python
KeyError: 'GOOGLE_API_KEY'
# or
None when accessing os.getenv("GOOGLE_API_KEY")
```

**Solutions:**

#### 1. Verify .env File Exists

```bash
# Check if .env file exists
ls -la .env

# If not, create from example
cp env.example .env
```

#### 2. Check .env File Format

The `.env` file must have proper format:

**❌ Wrong:**
```env
GOOGLE_API_KEY = "your-api-key"  # No quotes needed
GITHUB_TOKEN= your-token         # No space before =
export NPM_REGISTRY=...          # No export keyword
```

**✅ Correct:**
```env
GOOGLE_API_KEY=your-api-key-here
GITHUB_TOKEN=your-github-token
NPM_REGISTRY=https://registry.npmjs.org
```

#### 3. Verify .env File Location

```bash
# .env must be in project root
CodeBaseOpsAI-v2-1/
├── .env              # ← Should be here
├── main.py
└── src/
```

#### 4. Check File Permissions

```bash
# Ensure .env is readable
chmod 600 .env

# Verify contents
cat .env
```

#### 5. Verify dotenv Loading

```python
# In your code, ensure dotenv is loaded
from dotenv import load_dotenv
import os

load_dotenv()  # Must be called before accessing env vars

# Test loading
print(f"API Key loaded: {os.getenv('GOOGLE_API_KEY') is not None}")
```

### Issue: Environment Variables Not Recognized

**Symptoms:**
```python
# Returns None even though .env has the key
api_key = os.getenv("GOOGLE_API_KEY")
print(api_key)  # None
```

**Solutions:**

#### 1. Check for Typos

```bash
# In .env file
GOOGLE_API_KEY=abc123

# In code - must match exactly
os.getenv("GOOGLE_API_KEY")  # ✅
os.getenv("GOOGLE_APIKEY")   # ❌ Wrong
os.getenv("google_api_key")  # ❌ Case sensitive
```

#### 2. Check for Hidden Characters

```bash
# Remove potential hidden characters
cat -A .env

# Should show:
GOOGLE_API_KEY=your-key$
# Not:
GOOGLE_API_KEY=your-key ^M$  # ❌ Carriage return
```

**Fix:**
```bash
# Convert line endings
dos2unix .env
# or
sed -i 's/\r$//' .env
```

#### 3. Force Reload

```python
from dotenv import load_dotenv

# Force reload even if already loaded
load_dotenv(override=True)
```

---

## Import Errors

### Issue: `ModuleNotFoundError: No module named 'src'`

**Symptoms:**
```python
from src.agent import Agent
ModuleNotFoundError: No module named 'src'
```

**Solutions:**

#### 1. Run from Project Root

```bash
# Wrong - running from src/ directory
cd src/
python agent.py  # ❌ Will fail

# Correct - run from project root
cd /path/to/CodeBaseOpsAI-v2-1/
python main.py  # ✅ Works
```

#### 2. Set PYTHONPATH

```bash
# Temporary fix
export PYTHONPATH=/path/to/CodeBaseOpsAI-v2-1:$PYTHONPATH
python main.py

# Or in your script
import sys
sys.path.insert(0, '/path/to/CodeBaseOpsAI-v2-1')
```

#### 3. Install as Package (Development Mode)

```bash
# Create setup.py in project root
cat > setup.py << 'EOF'
from setuptools import setup, find_packages

setup(
    name="codebase_ops_ai",
    version="2.1.0",
    packages=find_packages(),
)
EOF

# Install in editable mode
pip install -e .
```

### Issue: `ImportError: cannot import name 'create_agent'`

**Symptoms:**
```python
from langchain.agents import create_agent
ImportError: cannot import name 'create_agent' from 'langchain.agents'
```

**Solutions:**

#### 1. Verify LangChain Version

```bash
pip list | grep langchain

# Should show:
# langchain            1.2.0
# langchain-google-genai   4.1.2
# langchain-classic    1.0.1
```

#### 2. Reinstall Correct Versions

```bash
pip uninstall langchain langchain-google-genai langchain-classic -y
pip install langchain==1.2.0 langchain-google-genai==4.1.2 langchain-classic==1.0.1
```

#### 3. Check Import Path

```python
# Correct import
from langchain.agents import create_agent  # ✅

# Wrong imports (old versions)
from langchain.agents import initialize_agent  # ❌ Deprecated
from langchain_classic.agents import create_react_agent  # ❌ Wrong for v2.1
```

### Issue: Pydantic Validation Errors

**Symptoms:**
```python
ValidationError: 1 validation error for AnalyzePackagesInput
pydantic.error_wrappers.ValidationError
```

**Solutions:**

#### 1. Check Pydantic Version Compatibility

```bash
# Check version
pip show pydantic

# LangChain 1.2.0 requires Pydantic v2
pip install "pydantic>=2.0.0"
```

#### 2. Verify Schema Imports

```python
# Correct - using Pydantic v2
from pydantic import BaseModel, Field

# Wrong - Pydantic v1 style
from pydantic import BaseSettings  # ❌ Removed in v2
```

---

## API Key Issues

### Issue: Google API Key Invalid

**Symptoms:**
```python
google.api_core.exceptions.PermissionDenied: 403 API key not valid
```

**Solutions:**

#### 1. Verify API Key Format

```bash
# Google API keys start with "AIza"
echo $GOOGLE_API_KEY | grep "^AIza"

# If no match, key is invalid
```

#### 2. Check API Key Status

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Verify key is active and not expired
3. Check if key has been rate-limited

#### 3. Regenerate API Key

```bash
# Generate new key at:
# https://aistudio.google.com/app/apikey

# Update .env file
sed -i 's/GOOGLE_API_KEY=.*/GOOGLE_API_KEY=your-new-key/' .env
```

#### 4. Check API Quota

```python
# Rate limit errors
google.api_core.exceptions.ResourceExhausted: 429 Quota exceeded

# Solution: Wait or upgrade quota
```

**Check quota at**: [Google Cloud Console](https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/quotas)

### Issue: GitHub Token Authentication Failed

**Symptoms:**
```python
github.GithubException.BadCredentialsException: 401 Bad credentials
```

**Solutions:**

#### 1. Verify Token Permissions

```bash
# Check token has 'repo' scope
curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/user

# Look for "X-OAuth-Scopes: repo" in headers
```

#### 2. Regenerate Token

1. Go to [GitHub Settings](https://github.com/settings/tokens)
2. Delete old token
3. Generate new token with `repo` scope
4. Update `.env`:

```bash
GITHUB_TOKEN=ghp_newTokenHere
```

#### 3. Check Token Expiration

```bash
# Test token
curl -I -H "Authorization: token YOUR_TOKEN" https://api.github.com/user

# Look for response:
# HTTP/2 200  ✅ Valid
# HTTP/2 401  ❌ Invalid/Expired
```

### Issue: Rate Limiting

**Symptoms:**
```python
github.GithubException.RateLimitExceededException: 403 API rate limit exceeded
```

**Solutions:**

#### 1. Check Rate Limit Status

```python
from github import Github

g = Github(os.getenv("GITHUB_TOKEN"))
rate_limit = g.get_rate_limit()
print(f"Remaining: {rate_limit.core.remaining}")
print(f"Reset at: {rate_limit.core.reset}")
```

#### 2. Wait for Reset

```bash
# Calculate wait time
python3 -c "
from github import Github
import os, time
from dotenv import load_dotenv
load_dotenv()
g = Github(os.getenv('GITHUB_TOKEN'))
reset_time = g.get_rate_limit().core.reset
wait_seconds = (reset_time - time.time())
print(f'Wait {int(wait_seconds/60)} minutes')
"
```

#### 3. Use Personal Access Token

```bash
# Authenticated users get higher limits:
# - 60/hour → 5000/hour with token
# Ensure GITHUB_TOKEN is set in .env
```

---

## Package Management Errors

### Issue: `package.json` Not Found

**Symptoms:**
```python
Error: package.json not found at /path/to/package.json
```

**Solutions:**

#### 1. Verify File Path

```bash
# Check if file exists
ls -la package.json

# If in subdirectory
ls -la /tmp/repo-clone/package.json
```

#### 2. Use Absolute Path

```python
# Wrong - relative path may fail
analyze_packages(package_json_path="package.json")

# Correct - absolute path
import os
clone_path = "/tmp/base-serverless-clone/"
package_path = os.path.join(clone_path, "package.json")
analyze_packages(package_json_path=package_path)
```

#### 3. Clone Repository First

```python
# Ensure repository is cloned before accessing package.json
# Step 1: Clone
clone_repository(
    repository="owner/repo",
    clone_path="/tmp/repo"
)

# Step 2: Then access package.json
analyze_packages(
    package_json_path="/tmp/repo/package.json"
)
```

### Issue: Invalid `package.json` Format

**Symptoms:**
```python
json.decoder.JSONDecodeError: Expecting ',' delimiter
```

**Solutions:**

#### 1. Validate JSON

```bash
# Use jq to validate
jq . package.json

# Or Python
python3 -c "import json; json.load(open('package.json'))"
```

#### 2. Common JSON Errors

```json
// ❌ Trailing commas
{
  "name": "my-package",
  "version": "1.0.0",  // ← Remove this comma
}

// ❌ Comments (not allowed in JSON)
{
  // This is a comment  ← Remove comments
  "name": "my-package"
}

// ✅ Correct
{
  "name": "my-package",
  "version": "1.0.0"
}
```

#### 3. Fix Encoding Issues

```bash
# Check file encoding
file package.json

# Convert to UTF-8 if needed
iconv -f ISO-8859-1 -t UTF-8 package.json > package.json.utf8
mv package.json.utf8 package.json
```

### Issue: Node Version Compatibility

**Symptoms:**
```python
[WARN] package-name: no compatible version found
```

**Solutions:**

#### 1. Check Node Version Configuration

```python
# Verify node_lts_version in agent initialization
agent = Agent(node_lts_version='22.11.0')  # Current LTS

# Or update in main.py
node_lts_version = '22.11.0'  # Update to latest LTS
```

#### 2. Check Package Requirements

```bash
# View package engines requirement
npm view package-name engines

# Example output:
{ node: '>=18.0.0' }
```

#### 3. Override Version Check

```python
# Add package with specific version
add_package(
    package_name="problematic-package",
    version="^1.0.0",  # Specify compatible version
    npm_lookup=False   # Skip compatibility check
)
```

---

## npm_lookup Failures

### Issue: npm Registry Timeout

**Symptoms:**
```python
[SKIP] package-name: registry fetch failed: HTTPSConnectionPool timeout
```

**Solutions:**

#### 1. Increase Timeout

```python
# In package_updates_utils.py, increase timeout
import requests

response = requests.get(
    url,
    timeout=30  # Increase from default 10
)
```

#### 2. Use Alternative Registry

```bash
# Set custom registry in .env
NPM_REGISTRY=https://registry.npmjs.cf/  # Cloudflare mirror

# Or in code
from src.tools import PackageUpdatesTools

tools = PackageUpdatesTools(
    node_lts_version="22.11.0",
    npm_registry="https://registry.npmjs.cf/"
)
```

#### 3. Retry Logic

```python
import time

max_retries = 3
for attempt in range(max_retries):
    try:
        result = analyze_packages(package_json_path="package.json")
        break
    except Exception as e:
        if attempt < max_retries - 1:
            time.sleep(2 ** attempt)  # Exponential backoff
            continue
        raise
```

#### 4. Disable npm_lookup Temporarily

```python
# Skip registry lookups if unavailable
analyze_packages(
    package_json_path="package.json",
    npm_lookup=False  # Skip npm registry
)
```

### Issue: Package Not Found in Registry

**Symptoms:**
```python
[SKIP] @scope/package: registry fetch failed: 404 Not Found
```

**Solutions:**

#### 1. Verify Package Name

```bash
# Search for package
npm search package-name

# Or check directly
curl https://registry.npmjs.org/@scope/package-name
```

#### 2. Check Scoped Package Access

```bash
# Private scoped packages require authentication
# Add .npmrc in home directory
cat > ~/.npmrc << EOF
//registry.npmjs.org/:_authToken=YOUR_NPM_TOKEN
EOF
```

#### 3. Handle Missing Packages

```python
# Remove obsolete packages first
remove_package(
    package_name="@obsolete/package",
    package_json_path="package.json"
)

# Then update remaining
update_packages(package_json_path="package.json")
```

### Issue: Packument Parse Error

**Symptoms:**
```python
KeyError: 'versions' in packument
```

**Solutions:**

#### 1. Verify Registry Response

```bash
# Check raw registry data
curl https://registry.npmjs.org/package-name | jq '.versions | keys'
```

#### 2. Add Error Handling

```python
# In your utils, add try-except
try:
    versions = packument.get('versions', {})
    if not versions:
        raise ValueError(f"No versions found for {package_name}")
except Exception as e:
    # Log and skip
    print(f"Error parsing packument: {e}")
```

---

## Vulnerability Scanning Issues

### Issue: `npm audit` Not Found

**Symptoms:**
```python
FileNotFoundError: [Errno 2] No such file or directory: 'npm'
```

**Solutions:**

#### 1. Install Node.js and npm

```bash
# Check if npm is installed
which npm
npm --version

# Install if missing
# On macOS:
brew install node

# On Ubuntu:
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs

# On Windows:
# Download from: https://nodejs.org/
```

#### 2. Add npm to PATH

```bash
# Find npm location
find /usr -name npm 2>/dev/null

# Add to PATH
export PATH="/usr/local/bin:$PATH"

# Make permanent
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Issue: `npm audit` Returns Errors

**Symptoms:**
```python
npm ERR! code ENOLOCK
npm ERR! audit This command requires an existing lockfile.
```

**Solutions:**

#### 1. Generate Lockfile

```bash
# Navigate to project directory
cd /tmp/repo-clone/

# Generate package-lock.json
npm install

# Then run audit
npm audit
```

#### 2. Use `--package-lock-only`

```bash
# Generate lockfile without installing
npm install --package-lock-only

# Then audit
npm audit
```

#### 3. Skip Audit if No Lockfile

```python
import os
from pathlib import Path

def audit_packages(package_json_path: str):
    package_dir = Path(package_json_path).parent
    lockfile = package_dir / "package-lock.json"
    
    if not lockfile.exists():
        return "Skipping audit: no package-lock.json found"
    
    # Continue with audit...
```

### Issue: High Severity Vulnerabilities

**Symptoms:**
```bash
found 5 vulnerabilities (2 moderate, 3 high)
```

**Solutions:**

#### 1. Auto-Fix Vulnerabilities

```bash
# Try automatic fix
npm audit fix

# Force fix (may cause breaking changes)
npm audit fix --force
```

#### 2. Update Specific Packages

```python
# Identify vulnerable packages
audit_packages(package_json_path="package.json")

# Update them
update_specific_packages(
    package_names=["vulnerable-package"],
    package_json_path="package.json",
    lock_major=False,  # Allow major version updates
    apply_updates=True
)
```

#### 3. Filter by Severity

```python
# Only show critical/high
audit_packages(
    package_json_path="package.json",
    min_severity="high"
)
```

---

## Agent Execution Errors

### Issue: Agent Fails to Execute Tools

**Symptoms:**
```python
Agent stopped due to max iterations
Agent did not return a tool response
```

**Solutions:**

#### 1. Check Tool Registration

```python
# Verify tools are registered
agent = Agent(node_lts_version="22.11.0")
tools = agent.tools

print(f"Registered tools: {len(tools)}")
for tool in tools:
    print(f"  - {tool.name}")

# Should show all tools:
# - read_repository
# - clone_repository
# - analyze_packages
# etc.
```

#### 2. Verify Prompt Format

```python
# Check agent prompt
from src.agent_prompt import AgentPropmpt

prompt = AgentPropmpt()
print(prompt.get_prompt_text())

# Ensure it has proper tool placeholders
```

#### 3. Increase Max Iterations

```python
# In agent.py, when creating agent
from langchain.agents import create_agent

agent = create_agent(
    model=self.llm,
    tools=self.tools,
    system_prompt=self.agent_prompt.get_prompt_text(),
    # Add max_iterations (if supported)
)
```

#### 4. Check LLM Response

```python
# Add debugging
response = executor.invoke({"messages": [{"role": "user", "content": query}]})

print("=== LLM Response ===")
print(response)

# Check for:
# - Tool calls
# - Error messages
# - Reasoning steps
```

### Issue: Token Limit Exceeded

**Symptoms:**
```python
google.api_core.exceptions.InvalidArgument: 400 Request payload size exceeds the limit
```

**Solutions:**

#### 1. Reduce Output Tokens

```python
# In agent.py
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    max_output_tokens=1024,  # Reduce if needed (default 8192)
    api_key=os.getenv("GOOGLE_API_KEY")
)
```

#### 2. Chunk Large Operations

```python
# Instead of processing all packages at once
packages = ["pkg1", "pkg2", "pkg3", ..., "pkg50"]

# Process in batches
batch_size = 10
for i in range(0, len(packages), batch_size):
    batch = packages[i:i+batch_size]
    update_specific_packages(
        package_names=batch,
        package_json_path="package.json"
    )
```

#### 3. Simplify Instructions

```python
# Instead of long, complex instruction
instruction = """
Clone repository X, checkout branch Y, analyze all packages,
update everything, audit for vulnerabilities, generate report...
"""

# Break into smaller steps
instructions = [
    "Clone repository X to /tmp/repo",
    "Checkout branch Y",
    "Analyze packages in /tmp/repo/package.json",
    # ... separate instructions
]

for instruction in instructions:
    executor.invoke({"messages": [{"role": "user", "content": instruction}]})
```

### Issue: Agent Loops Infinitely

**Symptoms:**
```python
# Agent repeats same action multiple times
[UPDATE] package1: ...
[UPDATE] package1: ...
[UPDATE] package1: ...
```

**Solutions:**

#### 1. Add Loop Detection

```python
# In main.py
seen_actions = set()

def execute_with_loop_detection(query):
    action_hash = hash(query)
    
    if action_hash in seen_actions:
        print(f"⚠️  Loop detected, skipping: {query}")
        return
    
    seen_actions.add(action_hash)
    response = executor.invoke({"messages": [{"role": "user", "content": query}]})
    return response
```

#### 2. Improve Prompt Clarity

```python
# Make instructions more specific
# ❌ Vague
"Update the packages"

# ✅ Specific
"Update packages in /tmp/repo/package.json with lock_major=True, then stop"
```

---

## Tool Execution Failures

### Issue: GitHub Clone Fails

**Symptoms:**
```python
Error cloning repository: Authentication failed
```

**Solutions:**

#### 1. Public Repository

```python
# For public repos, no token needed
clone_repository(
    repository="https://github.com/owner/repo.git",
    clone_path="/tmp/repo"
)
```

#### 2. Private Repository

```bash
# Ensure GITHUB_TOKEN is set
echo $GITHUB_TOKEN

# Clone with token
git clone https://${GITHUB_TOKEN}@github.com/owner/repo.git
```

#### 3. SSH Authentication

```bash
# Set up SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"
cat ~/.ssh/id_ed25519.pub
# Add to GitHub: Settings → SSH Keys

# Clone with SSH
clone_repository(
    repository="git@github.com:owner/repo.git",
    clone_path="/tmp/repo"
)
```

### Issue: YAML Update Fails

**Symptoms:**
```python
Error: Key 'custom.providers' not found in YAML
```

**Solutions:**

#### 1. Ensure Parent Keys Exist

```python
# Create parent key first
ensure_dict_key(
    yaml_file_path="serverless.yml",
    key_path="custom"
)

# Then add attributes
add_yaml_attributes(
    yaml_file_path="serverless.yml",
    parent_key="custom",
    attributes_yaml="providers:\n  aws: true"
)
```

#### 2. Check Path Syntax

```python
# ❌ Wrong
update_yaml_attribute(
    yaml_file_path="serverless.yml",
    attribute_path="custom/providers/aws",  # Wrong separator
    new_value="true"
)

# ✅ Correct
update_yaml_attribute(
    yaml_file_path="serverless.yml",
    attribute_path="custom.providers.aws",  # Dot separator
    new_value="true"
)
```

### Issue: JSON Tool Errors

**Symptoms:**
```python
TypeError: Object of type datetime is not JSON serializable
```

**Solutions:**

#### 1. Convert Non-Serializable Types

```python
import json
from datetime import datetime

# Custom encoder
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

# Use when saving
save_json_to_file(
    json_data=data,
    file_path="output.json",
    cls=DateTimeEncoder  # Add if supported
)
```

#### 2. Pre-Process Data

```python
# Convert datetime to string before saving
data = {
    "timestamp": datetime.now().isoformat(),
    "value": 123
}

save_json_to_file(json_data=data, file_path="output.json")
```

---

## GitHub Operations Issues

### Issue: Branch Checkout Fails

**Symptoms:**
```python
Error checking out branch: pathspec 'develop' did not match any file(s)
```

**Solutions:**

#### 1. Verify Branch Exists

```bash
# List all branches
cd /tmp/repo
git branch -r

# Fetch all branches
git fetch --all
```

#### 2. Create Branch if Missing

```python
def checkout_or_create_branch(repo_path: str, branch: str):
    import subprocess
    
    try:
        # Try checkout
        subprocess.run(
            ["git", "checkout", branch],
            cwd=repo_path,
            check=True
        )
    except subprocess.CalledProcessError:
        # Create and checkout
        subprocess.run(
            ["git", "checkout", "-b", branch],
            cwd=repo_path,
            check=True
        )
```

### Issue: Repository List Files Fails

**Symptoms:**
```python
Error listing files: Not a git repository
```

**Solutions:**

#### 1. Verify Repository Path

```bash
# Check if .git exists
ls -la /tmp/repo/.git

# If not, path is wrong or not cloned
```

#### 2. Re-clone Repository

```python
import shutil

# Remove invalid clone
shutil.rmtree("/tmp/repo", ignore_errors=True)

# Clone again
clone_repository(
    repository="owner/repo",
    clone_path="/tmp/repo"
)
```

---

## YAML/JSON Manipulation Errors

### Issue: YAML Indentation Errors

**Symptoms:**
```python
yaml.scanner.ScannerError: mapping values are not allowed here
```

**Solutions:**

#### 1. Use Proper YAML Format

```python
# ❌ Wrong - invalid YAML
attributes_yaml = "key1: value1\nkey2: value2"  # Missing proper formatting

# ✅ Correct
attributes_yaml = """
key1: value1
key2:
  nested: value2
"""
```

#### 2. Validate YAML Before Adding

```python
import yaml

def validate_yaml_string(yaml_str: str):
    try:
        yaml.safe_load(yaml_str)
        return True
    except yaml.YAMLError as e:
        print(f"Invalid YAML: {e}")
        return False

# Use before adding
if validate_yaml_string(attributes_yaml):
    add_yaml_attributes(...)
```

### Issue: JSON Encoding Errors

**Symptoms:**
```python
TypeError: keys must be str, int, float, bool or None, not tuple
```

**Solutions:**

```python
# ❌ Wrong - tuple keys
data = {
    ("key", "tuple"): "value"
}

# ✅ Correct - string keys
data = {
    "key_tuple": "value"
}

save_json_to_file(json_data=data, file_path="output.json")
```

---

## Debugging Tips

### Enable Debug Logging

```python
import logging

# Set up detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Enable LangChain debug
import langchain
langchain.debug = True
```

### Inspect Tool Outputs

```python
# Add verbose output
def debug_tool_execution(tool_name: str, **kwargs):
    print(f"\n=== Executing: {tool_name} ===")
    print(f"Parameters: {kwargs}")
    
    result = globals()[tool_name](**kwargs)
    
    print(f"Result: {result}")
    print("=" * 50)
    return result

# Use for debugging
result = debug_tool_execution(
    "analyze_packages",
    package_json_path="/tmp/repo/package.json"
)
```

### Test Individual Components

```python
# Test package updates in isolation
from src.tools.package_updates_tools import PackageUpdatesTools

tools = PackageUpdatesTools(node_lts_version="22.11.0")

# Test analyze
result = tools.analyze_packages(
    package_json_path="test_package.json",
    npm_lookup=True
)
print(result)
```

### Monitor Memory Usage

```python
import tracemalloc

tracemalloc.start()

# Your code here
executor.invoke({"messages": [{"role": "user", "content": query}]})

current, peak = tracemalloc.get_traced_memory()
print(f"Current memory: {current / 10**6:.2f} MB")
print(f"Peak memory: {peak / 10**6:.2f} MB")
tracemalloc.stop()
```

### Capture Exception Tracebacks

```python
import traceback

try:
    # Your code
    executor.invoke({"messages": [{"role": "user", "content": query}]})
except Exception as e:
    print("=== Full Traceback ===")
    traceback.print_exc()
    print("\n=== Exception Details ===")
    print(f"Type: {type(e).__name__}")
    print(f"Message: {str(e)}")
```

---

## Performance Issues

### Issue: Slow Package Analysis

**Symptoms:**
```python
# Takes >30 seconds per package
Analyzing 50 packages...
```

**Solutions:**

#### 1. Disable npm_lookup for Faster Analysis

```python
# Skip registry lookups
analyze_packages(
    package_json_path="package.json",
    npm_lookup=False  # Much faster
)
```

#### 2. Use Concurrent Requests

```python
# In package_updates_utils.py
from concurrent.futures import ThreadPoolExecutor

def fetch_multiple_packuments(package_names: list, registry: str):
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {
            executor.submit(fetch_packument, name, registry): name
            for name in package_names
        }
        # ... process results
```

#### 3. Cache Registry Responses

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def fetch_packument_cached(package_name: str, registry: str):
    return fetch_packument(package_name, registry)
```

### Issue: High Memory Usage

**Solutions:**

#### 1. Process in Batches

```python
# Instead of loading all at once
packages = get_all_packages()  # 1000+ packages

# Process in chunks
batch_size = 50
for i in range(0, len(packages), batch_size):
    batch = packages[i:i+batch_size]
    process_batch(batch)
    # Memory freed after each batch
```

#### 2. Stream Large Files

```python
import json

# Instead of loading entire file
with open("large_audit.json") as f:
    data = json.load(f)  # ❌ Loads all into memory

# Stream processing
import ijson

with open("large_audit.json", "rb") as f:
    for item in ijson.items(f, "vulnerabilities.item"):
        process_vulnerability(item)  # ✅ Process one at a time
```

---

## Advanced Troubleshooting

### Debug LangChain Agent Internals

```python
from langchain.callbacks import StdOutCallbackHandler

# Add callback for detailed output
handler = StdOutCallbackHandler()

response = executor.invoke(
    {"messages": [{"role": "user", "content": query}]},
    config={"callbacks": [handler]}
)
```

### Trace Tool Execution

```python
# Monkey-patch tools for tracing
original_analyze = tools.analyze_packages

def traced_analyze(*args, **kwargs):
    import time
    print(f"[TRACE] analyze_packages called with {kwargs}")
    start = time.time()
    result = original_analyze(*args, **kwargs)
    elapsed = time.time() - start
    print(f"[TRACE] analyze_packages completed in {elapsed:.2f}s")
    return result

tools.analyze_packages = traced_analyze
```

### Profile Code Performance

```python
import cProfile
import pstats

# Profile execution
profiler = cProfile.Profile()
profiler.enable()

# Your code
executor.invoke({"messages": [{"role": "user", "content": query}]})

profiler.disable()

# Print stats
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)  # Top 20 slowest functions
```

### Network Debugging

```bash
# Monitor HTTP requests
export PYTHONWARNINGS="default"
export HTTPX_LOG_LEVEL="trace"

# Or use mitmproxy
mitmproxy -p 8080

# Configure proxy in Python
import os
os.environ['HTTP_PROXY'] = 'http://localhost:8080'
os.environ['HTTPS_PROXY'] = 'http://localhost:8080'
```

---

## Common Error Messages and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError: No module named 'src'` | Wrong working directory | Run from project root |
| `KeyError: 'GOOGLE_API_KEY'` | Missing .env file | Create .env and add API keys |
| `ValidationError: package_json_path` | Invalid parameter type | Check schema requirements |
| `npm ERR! code ENOENT` | npm not installed | Install Node.js and npm |
| `401 Bad credentials` | Invalid GitHub token | Regenerate token with repo scope |
| `429 Too Many Requests` | Rate limit exceeded | Wait or use authentication |
| `package.json not found` | Wrong path | Use absolute path to file |
| `No compatible version found` | Node version mismatch | Update node_lts_version |
| `Agent stopped` | Max iterations reached | Simplify instructions |
| `Token limit exceeded` | Input too large | Reduce context or chunk operations |

---

## Getting Help

If you're still experiencing issues:

1. **Check Logs**: Review full error messages and tracebacks
2. **Enable Debug Mode**: Set `langchain.debug = True`
3. **Isolate Issue**: Test individual components
4. **Search Issues**: Check GitHub issues for similar problems
5. **Ask for Help**: Create detailed issue with:
   - Error message
   - Full traceback
   - Minimal reproduction code
   - Environment details (`pip list`, Python version)

**Pro Tip**: Include output of this diagnostic script:

```python
import sys
import os
from dotenv import load_dotenv

load_dotenv()

print("=== Environment Diagnostics ===")
print(f"Python: {sys.version}")
print(f"Working Directory: {os.getcwd()}")
print(f"GOOGLE_API_KEY set: {os.getenv('GOOGLE_API_KEY') is not None}")
print(f"GITHUB_TOKEN set: {os.getenv('GITHUB_TOKEN') is not None}")

import pkg_resources
print("\n=== Package Versions ===")
for pkg in ['langchain', 'langchain-google-genai', 'pydantic']:
    try:
        version = pkg_resources.get_distribution(pkg).version
        print(f"{pkg}: {version}")
    except:
        print(f"{pkg}: NOT INSTALLED")
```

---

**Last Updated**: January 2026  
**Version**: 2.1.0
