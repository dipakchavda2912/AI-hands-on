# 📚 Examples Guide - CodeBaseOpsAI-v2-1

**Comprehensive examples and real-world workflows for CodeBaseOpsAI-v2-1.**

---

## Table of Contents

1. [Basic Examples](#basic-examples)
2. [Package Management Examples](#package-management-examples)
3. [GitHub Operations Examples](#github-operations-examples)
4. [YAML Operations Examples](#yaml-operations-examples)
5. [JSON Operations Examples](#json-operations-examples)
6. [Complete Workflow Examples](#complete-workflow-examples)
7. [Custom Instruction Examples](#custom-instruction-examples)
8. [Error Handling Examples](#error-handling-examples)
9. [Multi-Tool Workflow Examples](#multi-tool-workflow-examples)
10. [Advanced Use Cases](#advanced-use-cases)

---

## Basic Examples

### Simple Agent Execution

```python
from src.agent import Agent
from dotenv import load_dotenv

load_dotenv()

# Initialize agent
agent = Agent(node_lts_version="22.11.0")
executor = agent.get_agent_executor()

# Execute a simple query
query = "Clone the repository dipakchavda2912/base-serverless to /tmp/test-clone"
response = executor.invoke({
    "messages": [{"role": "user", "content": query}]
})

print(response)
```

### Check Available Tools

```python
from src.agent import Agent

agent = Agent(node_lts_version="22.11.0")
tools = agent.tools

print(f"Available tools: {len(tools)}")
for tool in tools:
    print(f"\n📦 {tool.name}")
    print(f"   Description: {tool.description}")
```

**Output:**
```
Available tools: 18

📦 read_repository
   Description: Read a GitHub repository and analyze its files

📦 clone_repository
   Description: Clone a GitHub repository to local filesystem

📦 analyze_packages
   Description: Analyze npm package dependencies and suggest updates
...
```

---

## Package Management Examples

### Example 1: Analyze Package Dependencies

**Scenario**: Check current packages and get update recommendations

```python
from src.tools.package_updates_tools import PackageUpdatesTools

# Initialize package tools
tools = PackageUpdatesTools(node_lts_version="22.11.0")

# Analyze packages
result = tools.analyze_packages(
    package_json_path="/tmp/my-project/package.json",
    lock_major=True,      # Keep same major version
    npm_lookup=True       # Check npm registry
)

print(result)
```

**Output:**
```
Target Node.js LTS: 22.11.0
Detected Node.js version: 22.11.0
Found 25 dependencies to evaluate.

[UPDATE] express: ^4.17.1 -> ^4.19.2
[UPDATE] lodash: ^4.17.20 -> ^4.17.21
[WARN] old-package: no compatible & non-vulnerable version found
[UPDATE] axios: ^0.21.1 -> ^1.6.7

Total updates proposed: 23
```

### Example 2: Update All Packages

**Scenario**: Update all packages to latest compatible versions

```python
from src.tools.package_updates_tools import PackageUpdatesTools

tools = PackageUpdatesTools(node_lts_version="22.11.0")

# First, do a dry run to see what would change
result = tools.update_packages(
    package_json_path="/tmp/my-project/package.json",
    lock_major=True,
    dry_run=True,
    apply_updates=False
)

print("=== Dry Run Results ===")
print(result)

# Then apply the updates
result = tools.update_packages(
    package_json_path="/tmp/my-project/package.json",
    lock_major=True,
    dry_run=False,
    apply_updates=True,    # Run npm install
    manager="npm"
)

print("\n=== Applied Updates ===")
print(result)
```

### Example 3: Add a New Package

**Scenario**: Add a new dependency with automatic version resolution

```python
from src.tools.package_updates_tools import PackageUpdatesTools

tools = PackageUpdatesTools(node_lts_version="22.11.0")

# Add production dependency
result = tools.add_package(
    package_name="date-fns",
    version=None,          # Auto-detect latest compatible
    package_json_path="/tmp/my-project/package.json",
    dev=False,            # Production dependency
    install=True,         # Run npm install
    manager="npm",
    npm_lookup=True
)

print(result)
# Output: Successfully added 'date-fns@^3.2.0' to dependencies
#         Package installed using npm
```

**Add Dev Dependency:**

```python
# Add development dependency
result = tools.add_package(
    package_name="@types/node",
    version="^20.0.0",    # Specific version
    package_json_path="/tmp/my-project/package.json",
    dev=True,             # Dev dependency
    install=True,
    manager="npm"
)

print(result)
# Output: Successfully added '@types/node@^20.0.0' to devDependencies
```

### Example 4: Update Specific Packages

**Scenario**: Update only certain packages by name

```python
from src.tools.package_updates_tools import PackageUpdatesTools

tools = PackageUpdatesTools(node_lts_version="22.11.0")

# Update specific packages
packages_to_update = [
    "express",
    "axios",
    "lodash"
]

result = tools.update_specific_packages(
    package_names=packages_to_update,
    package_json_path="/tmp/my-project/package.json",
    lock_major=True,
    apply_updates=True,
    manager="npm"
)

print(result)
```

**Output:**
```
Target Node.js LTS: 22.11.0
Detected Node.js: 22.11.0
Updating 3 package(s)...

[UPDATE] express: ^4.17.1 -> ^4.19.2
[UPDATE] axios: ^0.21.1 -> ^1.6.7
[UPDATE] lodash: ^4.17.20 -> ^4.17.21

Successfully updated 3 package(s) in /tmp/my-project/package.json
Dependencies installed using npm
```

### Example 5: Remove a Package

**Scenario**: Remove unused dependency

```python
from src.tools.package_updates_tools import PackageUpdatesTools

tools = PackageUpdatesTools(node_lts_version="22.11.0")

# Remove package
result = tools.remove_package(
    package_name="moment",
    package_json_path="/tmp/my-project/package.json",
    uninstall=True,       # Also run npm uninstall
    manager="npm"
)

print(result)
# Output: Successfully removed 'moment' from dependencies
#         Package uninstalled using npm
```

### Example 6: Audit for Vulnerabilities

**Scenario**: Check for security vulnerabilities

```python
from src.tools.package_updates_tools import PackageUpdatesTools

tools = PackageUpdatesTools(node_lts_version="22.11.0")

# Audit all vulnerabilities
result = tools.audit_packages(
    package_json_path="/tmp/my-project/package.json",
    min_severity=None     # Show all severities
)

print(result)
```

**Output:**
```
Audit completed with exit code: 1
Vulnerabilities detected. Details saved to audit.json

Vulnerability Summary:
  moderate: 2
  high: 3
  critical: 1
```

**Filter by Severity:**

```python
# Only show high and critical
result = tools.audit_packages(
    package_json_path="/tmp/my-project/package.json",
    min_severity="high"
)

print(result)
```

### Example 7: Get Package Information

**Scenario**: Get detailed info about a specific package

```python
from src.tools.package_updates_tools import PackageUpdatesTools

tools = PackageUpdatesTools(node_lts_version="22.11.0")

# Get package info
result = tools.get_package_info(
    package_name="express",
    package_json_path="/tmp/my-project/package.json",
    npm_lookup=True
)

print(result)
```

**Output:**
```
Current version in dependencies: ^4.17.1

Latest version: 4.19.2
Total versions available: 287
Node.js requirement (latest): >=0.10.0

Recent versions: 4.19.2, 4.19.1, 4.19.0, 4.18.3, 4.18.2
```

---

## GitHub Operations Examples

### Example 1: Clone Repository

**Scenario**: Clone a public repository

```python
from src.tools.github_tools import GithubTools

tools = GithubTools()

# Clone repository
result = tools.clone_repository(
    repository="facebook/react",
    clone_path="/tmp/react-clone"
)

print(result)
# Output: Successfully cloned repository to /tmp/react-clone. Found 1247 files.
```

**Clone with Full URL:**

```python
# Using full GitHub URL
result = tools.clone_repository(
    repository="https://github.com/nodejs/node.git",
    clone_path="/tmp/node-clone"
)

print(result)
```

### Example 2: Checkout Branch

**Scenario**: Switch to a specific branch after cloning

```python
from src.tools.github_tools import GithubTools

tools = GithubTools()

# Clone repository
tools.clone_repository(
    repository="dipakchavda2912/base-serverless",
    clone_path="/tmp/serverless-clone"
)

# Checkout branch
result = tools.checkout_branch(
    repo_path="/tmp/serverless-clone",
    branch="develop"
)

print(result)
# Output: Successfully checked out branch 'develop' in /tmp/serverless-clone.
```

### Example 3: List Repository Files

**Scenario**: Get list of all files in repository

```python
from src.tools.github_tools import GithubTools

tools = GithubTools()

# Clone first
tools.clone_repository(
    repository="express/express",
    clone_path="/tmp/express-clone"
)

# List files
result = tools.list_files(repo_path="/tmp/express-clone")

print(result)
```

**Output:**
```
Files in repository:
  .gitignore
  .npmrc
  package.json
  README.md
  lib/application.js
  lib/express.js
  lib/request.js
  ...
```

### Example 4: Read Repository (Without Cloning)

**Scenario**: Analyze repository structure using GitHub API

```python
from src.tools.github_tools import GithubTools
import os

# Requires GITHUB_TOKEN
tools = GithubTools(github_token=os.getenv("GITHUB_TOKEN"))

# Read repository info
result = tools.read_repository(
    repository="vercel/next.js",
    branch="canary"
)

print(result)
```

**Output:**
```
Repository: vercel/next.js
Branch: canary
Files: 2,543
Main Language: TypeScript
Key Files:
  - package.json
  - README.md
  - tsconfig.json
  ...
```

---

## YAML Operations Examples

### Example 1: Read YAML File

**Scenario**: Read and display YAML contents

```python
from src.tools.yaml_tools import YamlTools

tools = YamlTools()

# Read YAML file
result = tools.read_yaml(
    yaml_file_path="/tmp/serverless-clone/serverless.yml"
)

print(result)
```

### Example 2: Update YAML Attribute

**Scenario**: Change a specific value in YAML

```python
from src.tools.yaml_tools import YamlTools

tools = YamlTools()

# Update service name
result = tools.update_yaml_attribute(
    yaml_file_path="/tmp/serverless-clone/serverless.yml",
    attribute_path="service",
    new_value="my-updated-service"
)

print(result)
# Output: Successfully updated 'service' in 'serverless.yml'. 
#         Old value: base-serverless, New value: my-updated-service
```

**Update Nested Attribute:**

```python
# Update nested value
result = tools.update_yaml_attribute(
    yaml_file_path="/tmp/serverless-clone/serverless.yml",
    attribute_path="provider.runtime",
    new_value="nodejs20.x"
)

print(result)
# Output: Successfully updated 'provider.runtime' in 'serverless.yml'.
#         Old value: nodejs18.x, New value: nodejs20.x
```

### Example 3: Ensure Dictionary Key Exists

**Scenario**: Create a parent key if it doesn't exist

```python
from src.tools.yaml_tools import YamlTools

tools = YamlTools()

# Ensure 'custom' key exists as dictionary
result = tools.ensure_dict_key(
    yaml_file_path="/tmp/serverless-clone/serverless.yml",
    key_path="custom"
)

print(result)
# Output: Success: Key 'custom' ensured as dictionary
```

### Example 4: Add Multiple Attributes

**Scenario**: Add multiple key-value pairs under a parent key

```python
from src.tools.yaml_tools import YamlTools

tools = YamlTools()

# First ensure parent key exists
tools.ensure_dict_key(
    yaml_file_path="/tmp/serverless-clone/serverless.yml",
    key_path="custom"
)

# Add multiple attributes
attributes_yaml = """
stage: ${opt:stage, 'dev'}
region: ${opt:region, 'us-east-1'}
tableName: ${self:custom.stage}-my-table
"""

result = tools.add_yaml_attributes(
    yaml_file_path="/tmp/serverless-clone/serverless.yml",
    parent_key="custom",
    attributes_yaml=attributes_yaml
)

print(result)
# Output: Successfully added attributes under 'custom'
```

### Example 5: Add Array Items

**Scenario**: Add plugins to a YAML array

```python
from src.tools.yaml_tools import YamlTools

tools = YamlTools()

# Add plugins
array_items_yaml = """
- serverless-offline
- serverless-plugin-typescript
- serverless-dynamodb-local
"""

result = tools.add_yaml_array_list(
    yaml_file_path="/tmp/serverless-clone/serverless.yml",
    parent_key="plugins",
    array_items_yaml=array_items_yaml
)

print(result)
# Output: Successfully added array items under 'plugins'
```

---

## JSON Operations Examples

### Example 1: Parse JSON String

**Scenario**: Convert JSON string to dictionary

```python
from src.tools.json_tools import JsonTools

tools = JsonTools()

json_string = '{"name": "my-app", "version": "1.0.0", "dependencies": {}}'

result = tools.parse_json(json_string=json_string)

print(result)
# Output: {'name': 'my-app', 'version': '1.0.0', 'dependencies': {}}
```

### Example 2: Add Attribute to JSON

**Scenario**: Add new key-value pair to JSON object

```python
from src.tools.json_tools import JsonTools

tools = JsonTools()

# Parse existing JSON
json_data = tools.parse_json('{"name": "my-app"}')

# Add new attribute
result = tools.add_new_attribute(
    json_data=json_data,
    key="description",
    value="My awesome application"
)

print(result)
# Output: {'name': 'my-app', 'description': 'My awesome application'}
```

### Example 3: Save JSON to File

**Scenario**: Write JSON data to file

```python
from src.tools.json_tools import JsonTools

tools = JsonTools()

json_data = {
    "name": "my-config",
    "settings": {
        "debug": True,
        "timeout": 3000
    }
}

tools.save_json_to_file(
    json_data=json_data,
    file_path="/tmp/config.json"
)

print("Configuration saved to /tmp/config.json")
```

---

## Complete Workflow Examples

### Workflow 1: Clone and Analyze Project

**Scenario**: Clone a repository, checkout a branch, and analyze packages

```python
from src.agent import Agent
from dotenv import load_dotenv

load_dotenv()

# Initialize agent
agent = Agent(node_lts_version="22.11.0")
executor = agent.get_agent_executor()

# Define complete workflow
instructions = [
    "Clone repository dipakchavda2912/base-serverless to /tmp/base-serverless",
    "Checkout branch develop in /tmp/base-serverless",
    "Analyze packages in /tmp/base-serverless/package.json with lock_major=True"
]

# Execute each instruction
for instruction in instructions:
    print(f"\n{'='*60}")
    print(f"Executing: {instruction}")
    print('='*60)
    
    response = executor.invoke({
        "messages": [{"role": "user", "content": instruction}]
    })
    
    print(response)
```

### Workflow 2: Update Project Dependencies

**Scenario**: Complete dependency update workflow

```python
from src.agent import Agent
from dotenv import load_dotenv
import json

load_dotenv()

agent = Agent(node_lts_version="22.11.0")
executor = agent.get_agent_executor()

# Step 1: Clone repository
clone_instruction = """
Clone repository dipakchavda2912/base-serverless to /tmp/update-project and 
checkout branch develop
"""

response = executor.invoke({
    "messages": [{"role": "user", "content": clone_instruction}]
})

# Step 2: Analyze current state
analyze_instruction = """
Analyze packages in /tmp/update-project/package.json with lock_major=True 
and npm_lookup=True
"""

response = executor.invoke({
    "messages": [{"role": "user", "content": analyze_instruction}]
})

print("\n=== Analysis Results ===")
print(response)

# Step 3: Update packages (dry run first)
update_instruction = """
Update packages in /tmp/update-project/package.json with lock_major=True, 
dry_run=True, and npm_lookup=True
"""

response = executor.invoke({
    "messages": [{"role": "user", "content": update_instruction}]
})

print("\n=== Dry Run Results ===")
print(response)

# Step 4: Apply updates
apply_instruction = """
Update packages in /tmp/update-project/package.json with lock_major=True, 
dry_run=False, apply_updates=True, manager=npm
"""

response = executor.invoke({
    "messages": [{"role": "user", "content": apply_instruction}]
})

print("\n=== Updates Applied ===")
print(response)

# Step 5: Audit for vulnerabilities
audit_instruction = """
Audit packages in /tmp/update-project/package.json with min_severity=high
"""

response = executor.invoke({
    "messages": [{"role": "user", "content": audit_instruction}]
})

print("\n=== Audit Results ===")
print(response)
```

### Workflow 3: Serverless Configuration Update

**Scenario**: Update serverless.yml configuration

```python
from src.agent import Agent
from dotenv import load_dotenv

load_dotenv()

agent = Agent(node_lts_version="22.11.0")
executor = agent.get_agent_executor()

# Complete serverless update workflow
workflow = """
1. Clone repository dipakchavda2912/base-serverless to /tmp/serverless-config
2. Checkout branch develop
3. Update attribute 'provider.runtime' to 'nodejs20.x' in /tmp/serverless-config/serverless.yml
4. Ensure key 'custom' exists as dictionary in /tmp/serverless-config/serverless.yml
5. Add attributes under 'custom' in /tmp/serverless-config/serverless.yml:
   stage: ${opt:stage, 'dev'}
   region: ${opt:region, 'us-east-1'}
"""

response = executor.invoke({
    "messages": [{"role": "user", "content": workflow}]
})

print(response)
```

### Workflow 4: Multi-Repository Analysis

**Scenario**: Analyze multiple repositories

```python
from src.agent import Agent
from dotenv import load_dotenv
import os

load_dotenv()

agent = Agent(node_lts_version="22.11.0")
executor = agent.get_agent_executor()

# List of repositories to analyze
repositories = [
    ("user1/repo1", "main"),
    ("user2/repo2", "develop"),
    ("user3/repo3", "master")
]

results = {}

for repo, branch in repositories:
    repo_name = repo.split('/')[-1]
    clone_path = f"/tmp/analysis/{repo_name}"
    
    # Clone and analyze
    instruction = f"""
    Clone repository {repo} to {clone_path}, 
    checkout branch {branch}, 
    and analyze packages in {clone_path}/package.json
    """
    
    print(f"\n{'='*60}")
    print(f"Processing: {repo} ({branch})")
    print('='*60)
    
    response = executor.invoke({
        "messages": [{"role": "user", "content": instruction}]
    })
    
    results[repo] = response
    print(response)

# Summary
print("\n" + "="*60)
print("SUMMARY")
print("="*60)

for repo, result in results.items():
    print(f"\n{repo}:")
    print(f"  Status: {'✅ Success' if 'Success' in str(result) else '❌ Failed'}")
```

---

## Custom Instruction Examples

### Example 1: Using InstructionService

**Scenario**: Generate instructions programmatically

```python
from src.services.instruction_service import InstructionService

# Configure instruction service
service = InstructionService(
    repository="dipakchavda2912/base-serverless",
    clone_path="/tmp/my-clone",
    branch="develop",
    node_lts_version="22.11.0"
)

# Get all instructions
instructions = service.get_all_instructions()

print(f"Generated {len(instructions)} instructions:")
for i, instruction in enumerate(instructions, 1):
    print(f"\n{i}. {instruction[:100]}...")
```

### Example 2: GitHub-Only Instructions

**Scenario**: Only GitHub operations

```python
from src.instructions.github_instructions import GithubInstructions

# Create GitHub instructions
github_instructions = GithubInstructions(
    repository="facebook/react",
    clone_path="/tmp/react-analysis",
    branch="main"
)

instructions = github_instructions.get_instructions()

for instruction in instructions:
    print(f"- {instruction}")
```

### Example 3: Package Management Instructions

**Scenario**: Generate package update instructions

```python
from src.instructions.nodejs_packages_instructions import NodejsPackagesInstructions

# Create package instructions
package_instructions = NodejsPackagesInstructions(
    clone_path="/tmp/my-project",
    node_lts_version="22.11.0"
)

instructions = package_instructions.get_instructions()

for instruction in instructions:
    print(f"📦 {instruction}")
```

**Output:**
```
📦 Analyze packages in /tmp/my-project/package.json with lock_major=True
📦 Update packages in /tmp/my-project/package.json with lock_major=True
📦 Audit packages in /tmp/my-project/package.json
```

### Example 4: Custom Serverless Instructions

**Scenario**: Generate serverless.yml update instructions

```python
from src.instructions.serverless_custom_tag_instructions import ServerlessCustomTagInstructions

# Create serverless instructions
serverless_instructions = ServerlessCustomTagInstructions(
    clone_path="/tmp/serverless-project"
)

instructions = serverless_instructions.get_instructions()

for instruction in instructions:
    print(f"⚙️  {instruction}")
```

---

## Error Handling Examples

### Example 1: Try-Catch Pattern

**Scenario**: Handle errors gracefully

```python
from src.tools.package_updates_tools import PackageUpdatesTools

tools = PackageUpdatesTools(node_lts_version="22.11.0")

try:
    result = tools.analyze_packages(
        package_json_path="/tmp/nonexistent/package.json"
    )
    print(result)
except FileNotFoundError as e:
    print(f"❌ File not found: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
```

### Example 2: Validation Before Execution

**Scenario**: Validate inputs before running

```python
import os
from pathlib import Path
from src.tools.package_updates_tools import PackageUpdatesTools

def safe_analyze_packages(package_json_path: str):
    # Validate file exists
    if not os.path.exists(package_json_path):
        return f"Error: File does not exist: {package_json_path}"
    
    # Validate file is readable
    if not os.access(package_json_path, os.R_OK):
        return f"Error: File is not readable: {package_json_path}"
    
    # Validate JSON format
    try:
        import json
        with open(package_json_path, 'r') as f:
            json.load(f)
    except json.JSONDecodeError as e:
        return f"Error: Invalid JSON: {e}"
    
    # Execute analysis
    tools = PackageUpdatesTools(node_lts_version="22.11.0")
    return tools.analyze_packages(package_json_path=package_json_path)

# Use safe function
result = safe_analyze_packages("/tmp/my-project/package.json")
print(result)
```

### Example 3: Retry Logic

**Scenario**: Retry on network failures

```python
import time
from src.tools.package_updates_tools import PackageUpdatesTools

def analyze_with_retry(package_json_path: str, max_retries=3):
    tools = PackageUpdatesTools(node_lts_version="22.11.0")
    
    for attempt in range(max_retries):
        try:
            result = tools.analyze_packages(
                package_json_path=package_json_path,
                npm_lookup=True
            )
            return result
        except Exception as e:
            if "timeout" in str(e).lower() and attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"⚠️  Attempt {attempt + 1} failed. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                # Last attempt or non-timeout error
                raise
    
    return "Error: All retries failed"

# Use with retry
result = analyze_with_retry("/tmp/my-project/package.json")
print(result)
```

### Example 4: Fallback Strategies

**Scenario**: Fallback to alternative approaches

```python
from src.tools.package_updates_tools import PackageUpdatesTools

def analyze_with_fallback(package_json_path: str):
    tools = PackageUpdatesTools(node_lts_version="22.11.0")
    
    # Try with npm_lookup first
    try:
        result = tools.analyze_packages(
            package_json_path=package_json_path,
            npm_lookup=True
        )
        return result
    except Exception as e:
        print(f"⚠️  npm lookup failed: {e}")
        print("⚠️  Falling back to local analysis...")
        
        # Fallback: analyze without npm lookup
        try:
            result = tools.analyze_packages(
                package_json_path=package_json_path,
                npm_lookup=False
            )
            return f"[Local Analysis Only]\n{result}"
        except Exception as fallback_error:
            return f"Error: Both strategies failed:\n1. {e}\n2. {fallback_error}"

result = analyze_with_fallback("/tmp/my-project/package.json")
print(result)
```

---

## Multi-Tool Workflow Examples

### Workflow 1: Complete Repository Setup

**Scenario**: Clone, configure, and update project

```python
from src.agent import Agent
from dotenv import load_dotenv

load_dotenv()

class RepositorySetup:
    def __init__(self, repository: str, branch: str, target_path: str):
        self.repository = repository
        self.branch = branch
        self.target_path = target_path
        self.agent = Agent(node_lts_version="22.11.0")
        self.executor = self.agent.get_agent_executor()
    
    def setup(self):
        """Execute complete setup workflow."""
        # Step 1: Clone
        self._clone_repository()
        
        # Step 2: Analyze packages
        analysis = self._analyze_packages()
        
        # Step 3: Update configuration
        self._update_configuration()
        
        # Step 4: Update packages
        self._update_packages()
        
        # Step 5: Audit
        audit = self._audit_packages()
        
        return {
            "clone": "Success",
            "analysis": analysis,
            "configuration": "Updated",
            "audit": audit
        }
    
    def _clone_repository(self):
        instruction = f"""
        Clone repository {self.repository} to {self.target_path} 
        and checkout branch {self.branch}
        """
        response = self.executor.invoke({
            "messages": [{"role": "user", "content": instruction}]
        })
        print(f"✅ Cloned {self.repository}")
        return response
    
    def _analyze_packages(self):
        instruction = f"""
        Analyze packages in {self.target_path}/package.json
        """
        response = self.executor.invoke({
            "messages": [{"role": "user", "content": instruction}]
        })
        print("✅ Analyzed packages")
        return response
    
    def _update_configuration(self):
        instruction = f"""
        Update attribute 'provider.runtime' to 'nodejs20.x' 
        in {self.target_path}/serverless.yml
        """
        response = self.executor.invoke({
            "messages": [{"role": "user", "content": instruction}]
        })
        print("✅ Updated configuration")
        return response
    
    def _update_packages(self):
        instruction = f"""
        Update packages in {self.target_path}/package.json 
        with lock_major=True and apply_updates=True
        """
        response = self.executor.invoke({
            "messages": [{"role": "user", "content": instruction}]
        })
        print("✅ Updated packages")
        return response
    
    def _audit_packages(self):
        instruction = f"""
        Audit packages in {self.target_path}/package.json
        """
        response = self.executor.invoke({
            "messages": [{"role": "user", "content": instruction}]
        })
        print("✅ Completed audit")
        return response

# Execute workflow
setup = RepositorySetup(
    repository="dipakchavda2912/base-serverless",
    branch="develop",
    target_path="/tmp/complete-setup"
)

result = setup.setup()
print("\n" + "="*60)
print("SETUP COMPLETE")
print("="*60)
print(f"Results: {result}")
```

### Workflow 2: Batch Package Updates

**Scenario**: Update packages in multiple projects

```python
from src.tools.package_updates_tools import PackageUpdatesTools
from pathlib import Path
import json

class BatchPackageUpdater:
    def __init__(self, node_lts_version: str = "22.11.0"):
        self.tools = PackageUpdatesTools(node_lts_version=node_lts_version)
    
    def update_projects(self, project_paths: list[str]):
        """Update packages in multiple projects."""
        results = {}
        
        for project_path in project_paths:
            print(f"\n{'='*60}")
            print(f"Processing: {project_path}")
            print('='*60)
            
            package_json = str(Path(project_path) / "package.json")
            
            try:
                # Analyze
                analysis = self.tools.analyze_packages(
                    package_json_path=package_json,
                    lock_major=True
                )
                print(f"\n📊 Analysis:\n{analysis}")
                
                # Update
                update = self.tools.update_packages(
                    package_json_path=package_json,
                    lock_major=True,
                    dry_run=False,
                    apply_updates=True
                )
                print(f"\n🔄 Update:\n{update}")
                
                # Audit
                audit = self.tools.audit_packages(
                    package_json_path=package_json
                )
                print(f"\n🔍 Audit:\n{audit}")
                
                results[project_path] = {
                    "status": "success",
                    "analysis": analysis,
                    "update": update,
                    "audit": audit
                }
                
            except Exception as e:
                print(f"❌ Error: {e}")
                results[project_path] = {
                    "status": "failed",
                    "error": str(e)
                }
        
        return results

# Use batch updater
updater = BatchPackageUpdater(node_lts_version="22.11.0")

projects = [
    "/tmp/project1",
    "/tmp/project2",
    "/tmp/project3"
]

results = updater.update_projects(projects)

# Generate report
print("\n" + "="*60)
print("BATCH UPDATE SUMMARY")
print("="*60)

for project, result in results.items():
    status = "✅" if result["status"] == "success" else "❌"
    print(f"{status} {project}: {result['status']}")
```

### Workflow 3: Progressive Package Migration

**Scenario**: Migrate packages to newer versions incrementally

```python
from src.tools.package_updates_tools import PackageUpdatesTools
import json

class ProgressivePackageMigrator:
    def __init__(self, package_json_path: str, node_lts_version: str):
        self.package_json_path = package_json_path
        self.tools = PackageUpdatesTools(node_lts_version=node_lts_version)
    
    def migrate(self, packages_per_batch: int = 5):
        """Migrate packages in small batches."""
        # Get all packages
        with open(self.package_json_path, 'r') as f:
            pkg = json.load(f)
        
        all_deps = {}
        for section in ['dependencies', 'devDependencies']:
            if section in pkg:
                all_deps.update(pkg[section])
        
        package_names = list(all_deps.keys())
        total_batches = (len(package_names) + packages_per_batch - 1) // packages_per_batch
        
        print(f"📦 Migrating {len(package_names)} packages in {total_batches} batches")
        
        results = []
        
        for i in range(0, len(package_names), packages_per_batch):
            batch = package_names[i:i+packages_per_batch]
            batch_num = (i // packages_per_batch) + 1
            
            print(f"\n{'='*60}")
            print(f"Batch {batch_num}/{total_batches}: {', '.join(batch)}")
            print('='*60)
            
            # Update batch
            result = self.tools.update_specific_packages(
                package_names=batch,
                package_json_path=self.package_json_path,
                lock_major=True,
                apply_updates=True
            )
            
            print(result)
            results.append({
                "batch": batch_num,
                "packages": batch,
                "result": result
            })
            
            # Test after each batch
            print("\n🧪 Running tests...")
            # Add your test command here
            # subprocess.run(["npm", "test"], check=True)
        
        return results

# Use migrator
migrator = ProgressivePackageMigrator(
    package_json_path="/tmp/my-project/package.json",
    node_lts_version="22.11.0"
)

results = migrator.migrate(packages_per_batch=5)
```

---

## Advanced Use Cases

### Use Case 1: Monorepo Management

**Scenario**: Manage multiple package.json files in a monorepo

```python
from src.tools.package_updates_tools import PackageUpdatesTools
from pathlib import Path
import os

class MonorepoManager:
    def __init__(self, root_path: str, node_lts_version: str = "22.11.0"):
        self.root_path = Path(root_path)
        self.tools = PackageUpdatesTools(node_lts_version=node_lts_version)
    
    def find_all_package_json(self):
        """Find all package.json files in monorepo."""
        package_files = []
        for root, dirs, files in os.walk(self.root_path):
            # Skip node_modules
            if 'node_modules' in root:
                continue
            if 'package.json' in files:
                package_files.append(Path(root) / 'package.json')
        return package_files
    
    def update_all_packages(self):
        """Update packages in all workspaces."""
        package_files = self.find_all_package_json()
        
        print(f"📦 Found {len(package_files)} package.json files")
        
        results = {}
        
        for package_file in package_files:
            relative_path = package_file.relative_to(self.root_path)
            print(f"\n{'='*60}")
            print(f"Updating: {relative_path}")
            print('='*60)
            
            result = self.tools.update_packages(
                package_json_path=str(package_file),
                lock_major=True,
                dry_run=False,
                apply_updates=False  # Run install manually for monorepos
            )
            
            results[str(relative_path)] = result
            print(result)
        
        return results

# Use monorepo manager
manager = MonorepoManager(
    root_path="/tmp/my-monorepo",
    node_lts_version="22.11.0"
)

results = manager.update_all_packages()
```

### Use Case 2: Automated Dependency Report

**Scenario**: Generate comprehensive dependency report

```python
from src.tools.package_updates_tools import PackageUpdatesTools
import json
from datetime import datetime
from pathlib import Path

class DependencyReporter:
    def __init__(self, package_json_path: str, node_lts_version: str):
        self.package_json_path = package_json_path
        self.tools = PackageUpdatesTools(node_lts_version=node_lts_version)
        self.report_data = {}
    
    def generate_report(self):
        """Generate comprehensive dependency report."""
        print("🔍 Generating dependency report...")
        
        # Load package.json
        with open(self.package_json_path, 'r') as f:
            pkg = json.load(f)
        
        self.report_data['project'] = {
            'name': pkg.get('name', 'Unknown'),
            'version': pkg.get('version', 'Unknown'),
            'timestamp': datetime.now().isoformat()
        }
        
        # Analyze packages
        print("\n📊 Analyzing packages...")
        analysis = self.tools.analyze_packages(
            package_json_path=self.package_json_path,
            lock_major=True,
            npm_lookup=True
        )
        self.report_data['analysis'] = analysis
        
        # Audit vulnerabilities
        print("\n🔒 Auditing security...")
        audit = self.tools.audit_packages(
            package_json_path=self.package_json_path
        )
        self.report_data['audit'] = audit
        
        # Get package info for major dependencies
        major_packages = ['express', 'react', 'lodash', 'axios']
        package_details = {}
        
        print("\n📋 Fetching package details...")
        for pkg_name in major_packages:
            try:
                info = self.tools.get_package_info(
                    package_name=pkg_name,
                    package_json_path=self.package_json_path,
                    npm_lookup=True
                )
                package_details[pkg_name] = info
            except:
                package_details[pkg_name] = "Not found"
        
        self.report_data['package_details'] = package_details
        
        return self.report_data
    
    def save_report(self, output_path: str = "dependency_report.json"):
        """Save report to file."""
        with open(output_path, 'w') as f:
            json.dump(self.report_data, f, indent=2)
        print(f"\n✅ Report saved to {output_path}")
    
    def print_summary(self):
        """Print report summary."""
        print("\n" + "="*60)
        print("DEPENDENCY REPORT SUMMARY")
        print("="*60)
        print(f"Project: {self.report_data['project']['name']}")
        print(f"Version: {self.report_data['project']['version']}")
        print(f"Generated: {self.report_data['project']['timestamp']}")
        print("\nAnalysis:")
        print(self.report_data['analysis'])
        print("\nSecurity Audit:")
        print(self.report_data['audit'])

# Use reporter
reporter = DependencyReporter(
    package_json_path="/tmp/my-project/package.json",
    node_lts_version="22.11.0"
)

report = reporter.generate_report()
reporter.print_summary()
reporter.save_report("dependency_report.json")
```

### Use Case 3: Continuous Integration Helper

**Scenario**: CI/CD pipeline integration

```python
from src.tools.package_updates_tools import PackageUpdatesTools
import sys

class CIHelper:
    def __init__(self, package_json_path: str, node_lts_version: str):
        self.package_json_path = package_json_path
        self.tools = PackageUpdatesTools(node_lts_version=node_lts_version)
    
    def check_outdated(self):
        """Check for outdated packages."""
        analysis = self.tools.analyze_packages(
            package_json_path=self.package_json_path,
            lock_major=True,
            npm_lookup=True
        )
        
        # Parse analysis
        has_updates = "[UPDATE]" in analysis
        
        if has_updates:
            print("⚠️  Outdated packages detected!")
            print(analysis)
            return False
        else:
            print("✅ All packages are up to date")
            return True
    
    def check_vulnerabilities(self, fail_on_severity: str = "high"):
        """Check for security vulnerabilities."""
        audit = self.tools.audit_packages(
            package_json_path=self.package_json_path,
            min_severity=fail_on_severity
        )
        
        has_vulnerabilities = "Vulnerabilities detected" in audit
        
        if has_vulnerabilities:
            print(f"❌ Security vulnerabilities found (>={fail_on_severity})!")
            print(audit)
            return False
        else:
            print("✅ No security vulnerabilities")
            return True
    
    def run_ci_checks(self):
        """Run all CI checks."""
        print("🔍 Running CI checks...\n")
        
        checks = {
            "outdated": self.check_outdated(),
            "vulnerabilities": self.check_vulnerabilities()
        }
        
        all_passed = all(checks.values())
        
        print("\n" + "="*60)
        print("CI CHECK RESULTS")
        print("="*60)
        for check, passed in checks.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{check.upper()}: {status}")
        
        if not all_passed:
            print("\n❌ CI checks failed!")
            sys.exit(1)
        else:
            print("\n✅ All CI checks passed!")
            sys.exit(0)

# Use in CI pipeline
if __name__ == "__main__":
    ci = CIHelper(
        package_json_path="/tmp/my-project/package.json",
        node_lts_version="22.11.0"
    )
    ci.run_ci_checks()
```

---

**Last Updated**: January 2026  
**Version**: 2.1.0
