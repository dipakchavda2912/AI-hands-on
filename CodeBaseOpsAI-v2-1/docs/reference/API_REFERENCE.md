# 📖 API Reference - CodeBaseOpsAI-v2-1

**Complete API documentation for all tools, schemas, and utilities.**

---

## Table of Contents

1. [Overview](#overview)
2. [Agent API](#agent-api)
3. [GitHub Tools API](#github-tools-api)
4. [Package Management Tools API](#package-management-tools-api)
5. [YAML Tools API](#yaml-tools-api)
6. [JSON Tools API](#json-tools-api)
7. [Schema Reference](#schema-reference)
8. [Utility Functions](#utility-functions)
9. [Service APIs](#service-apis)
10. [Error Responses](#error-responses)
11. [Type Definitions](#type-definitions)

---

## Overview

CodeBaseOpsAI-v2-1 provides a comprehensive set of tools for automating repository operations, package management, and configuration updates. All tools are designed to work with LangChain's agent framework.

### API Design Principles

- **Consistent Return Types**: All tools return `str` for easy parsing by LLM agents
- **Pydantic Validation**: All inputs validated using Pydantic schemas
- **Error Handling**: Errors returned as formatted strings, not exceptions
- **Idempotent Operations**: Safe to retry without side effects
- **Type Safety**: Full type hints for better IDE support

### Common Parameters

Many tools share common parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `package_json_path` | str | "package.json" | Path to package.json file |
| `npm_lookup` | bool | True | Whether to query npm registry |
| `lock_major` | bool | True | Prevent major version updates |
| `manager` | str | "npm" | Package manager (npm/yarn/pnpm) |
| `apply_updates` | bool | False | Run package manager install |

---

## Agent API

### Class: `Agent`

Main agent class that orchestrates all tools.

**Location**: `src/agent.py`

#### Constructor

```python
Agent(node_lts_version: str)
```

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `node_lts_version` | str | Yes | Node.js LTS version for compatibility checks (e.g., "22.11.0") |

**Example:**

```python
from src.agent import Agent

agent = Agent(node_lts_version="22.11.0")
```

#### Methods

##### `get_agent()`

Get the agent instance (CompiledGraph from LangChain).

**Returns**: `Any` (CompiledGraph)

**Example:**

```python
agent_instance = agent.get_agent()
```

##### `get_agent_executor()`

Get the agent executor (alias for `get_agent()` for backward compatibility).

**Returns**: `Any` (CompiledGraph)

**Example:**

```python
executor = agent.get_agent_executor()
response = executor.invoke({
    "messages": [{"role": "user", "content": "Clone repository X"}]
})
```

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| `tools` | List[StructuredTool] | All registered tools |
| `llm` | ChatGoogleGenerativeAI | Language model instance |
| `agent_prompt` | AgentPropmpt | Prompt template |
| `node_lts_version` | str | Node.js version |

---

## GitHub Tools API

### Class: `GithubTools`

Tools for GitHub repository operations.

**Location**: `src/tools/github_tools.py`

#### Constructor

```python
GithubTools(github_token: str | None = None)
```

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `github_token` | str \| None | No | `os.getenv("GITHUB_TOKEN")` | GitHub personal access token |

---

### Tool: `read_repository`

Read and analyze GitHub repository files via API.

**Schema**: `ReadRepoInput`

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `repository` | str | Yes | - | Repository in format 'owner/repo' |
| `branch` | str | No | "main" | Branch name |

**Returns**: `str`

**Success Response:**
```
Repository: owner/repo
Branch: main
Files: 123
Main Language: TypeScript
Key Files:
  - package.json
  - README.md
  - src/index.ts
```

**Error Response:**
```
Error: GitHub token not configured. Set GITHUB_TOKEN environment variable.
```
or
```
Error reading repository: 404 Repository not found
```

**Example:**

```python
from src.tools.github_tools import GithubTools

tools = GithubTools()
result = tools.read_repository(
    repository="facebook/react",
    branch="main"
)
print(result)
```

---

### Tool: `clone_repository`

Clone GitHub repository to local filesystem.

**Schema**: `CloneRepoInput`

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `repository` | str | Yes | - | Repository URL or 'owner/repo' format |
| `clone_path` | str | No | "/tmp/repo" | Local path to clone to |

**Returns**: `str`

**Success Response:**
```
Successfully cloned repository to /tmp/repo. Found 1247 files.
```

**Error Response:**
```
Error cloning repository: Authentication failed
```

**Example:**

```python
result = tools.clone_repository(
    repository="https://github.com/nodejs/node.git",
    clone_path="/tmp/node-clone"
)
```

**Notes:**
- Removes existing directory if it exists
- Works with both public and private repositories (requires token for private)
- Supports full URLs or 'owner/repo' shorthand

---

### Tool: `checkout_branch`

Checkout specific branch in cloned repository.

**Schema**: `CheckoutBranchInput`

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `repo_path` | str | Yes | - | Local path of cloned repository |
| `branch` | str | Yes | - | Branch name to checkout |

**Returns**: `str`

**Success Response:**
```
Successfully checked out branch 'develop' in /tmp/repo.
```

**Error Response:**
```
Error checking out branch: pathspec 'develop' did not match any file(s)
```

**Example:**

```python
result = tools.checkout_branch(
    repo_path="/tmp/repo",
    branch="develop"
)
```

---

### Tool: `list_files`

List all files in cloned repository.

**Schema**: `ListRepoFilesInput`

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `repo_path` | str | Yes | - | Local path of cloned repository |

**Returns**: `str`

**Success Response:**
```
Files in repository:
  .gitignore
  package.json
  README.md
  src/index.ts
  src/utils.ts
```

**Error Response:**
```
Error listing files: Not a git repository
```

**Example:**

```python
result = tools.list_files(repo_path="/tmp/repo")
```

---

## Package Management Tools API

### Class: `PackageUpdatesTools`

Tools for npm package dependency management.

**Location**: `src/tools/package_updates_tools.py`

#### Constructor

```python
PackageUpdatesTools(
    node_lts_version: str,
    npm_registry: str | None = None
)
```

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `node_lts_version` | str | Yes | - | Node.js LTS version (e.g., "22.11.0") |
| `npm_registry` | str \| None | No | `os.getenv("NPM_REGISTRY")` or "https://registry.npmjs.org" | NPM registry URL |

---

### Tool: `analyze_packages`

Analyze package dependencies and suggest updates.

**Schema**: `AnalyzePackagesInput`

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `package_json_path` | str | No | "package.json" | Path to package.json |
| `lock_major` | bool | No | True | Lock major version updates |
| `npm_lookup` | bool | No | True | Query npm registry |

**Returns**: `str`

**Success Response:**
```
Target Node.js LTS: 22.11.0
Detected Node.js version: 22.11.0
Found 25 dependencies to evaluate.

[UPDATE] express: ^4.17.1 -> ^4.19.2
[UPDATE] lodash: ^4.17.20 -> ^4.17.21
[WARN] old-package: no compatible & non-vulnerable version found

Total updates proposed: 23
```

**Error Response:**
```
Error: package.json not found at /path/to/package.json
```

**Example:**

```python
from src.tools.package_updates_tools import PackageUpdatesTools

tools = PackageUpdatesTools(node_lts_version="22.11.0")
result = tools.analyze_packages(
    package_json_path="/tmp/project/package.json",
    lock_major=True,
    npm_lookup=True
)
```

**Notes:**
- Checks npm registry for latest versions
- Filters by Node.js compatibility
- Excludes versions with known vulnerabilities
- `lock_major=True` keeps same major version (4.x.x → 4.y.z)

---

### Tool: `update_packages`

Update package dependencies in package.json.

**Schema**: `UpdatePackagesInput`

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `package_json_path` | str | No | "package.json" | Path to package.json |
| `lock_major` | bool | No | True | Lock major version updates |
| `dry_run` | bool | No | False | Preview changes without applying |
| `apply_updates` | bool | No | False | Run package manager install |
| `manager` | str | No | "npm" | Package manager (npm/yarn/pnpm) |
| `npm_lookup` | bool | No | True | Query npm registry |

**Returns**: `str`

**Success Response:**
```
Target Node.js LTS: 22.11.0
Detected Node.js: 22.11.0
[UPDATE] express: ^4.17.1 -> ^4.19.2
[UPDATE] axios: ^0.21.1 -> ^1.6.7

Successfully updated /tmp/project/package.json
Dependencies installed using npm
```

**Dry Run Response:**
```
[UPDATE] express: ^4.17.1 -> ^4.19.2

Dry-run mode: package.json not modified.
```

**Example:**

```python
# Dry run first
result = tools.update_packages(
    package_json_path="/tmp/project/package.json",
    lock_major=True,
    dry_run=True
)

# Then apply
result = tools.update_packages(
    package_json_path="/tmp/project/package.json",
    lock_major=True,
    dry_run=False,
    apply_updates=True,
    manager="npm"
)
```

**Notes:**
- Always run dry run first to preview changes
- `apply_updates=True` runs `npm install` after updating
- Modifies package.json in place

---

### Tool: `add_package`

Add new package to package.json.

**Schema**: `AddPackageInput`

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `package_name` | str | Yes | - | Package name |
| `version` | str \| None | No | None | Version (auto-detects if None) |
| `package_json_path` | str | No | "package.json" | Path to package.json |
| `dev` | bool | No | False | Add as devDependency |
| `install` | bool | No | False | Run package manager install |
| `manager` | str | No | "npm" | Package manager |
| `npm_lookup` | bool | No | True | Query npm registry |
| `node_lts_version` | str \| None | No | None | Override Node.js version |

**Returns**: `str`

**Success Response:**
```
Successfully added 'date-fns@^3.2.0' to dependencies
Package installed using npm
```

**Error Response:**
```
Error: Package 'date-fns' already exists in dependencies
```
or
```
Error: Could not find compatible version for 'old-package' compatible with Node.js 22.11.0
```

**Example:**

```python
# Add with auto-detection
result = tools.add_package(
    package_name="lodash",
    package_json_path="/tmp/project/package.json",
    install=True
)

# Add specific version as dev dependency
result = tools.add_package(
    package_name="@types/node",
    version="^20.0.0",
    package_json_path="/tmp/project/package.json",
    dev=True,
    install=True
)
```

**Notes:**
- `version=None` finds latest compatible version
- `version="latest"` also triggers auto-detection
- Returns error if package already exists

---

### Tool: `remove_package`

Remove package from package.json.

**Schema**: `RemovePackageInput`

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `package_name` | str | Yes | - | Package name |
| `package_json_path` | str | No | "package.json" | Path to package.json |
| `uninstall` | bool | No | False | Run package manager uninstall |
| `manager` | str | No | "npm" | Package manager |

**Returns**: `str`

**Success Response:**
```
Successfully removed 'moment' from dependencies
Package uninstalled using npm
```

**Error Response:**
```
Error: Package 'moment' not found in package.json
```

**Example:**

```python
result = tools.remove_package(
    package_name="moment",
    package_json_path="/tmp/project/package.json",
    uninstall=True,
    manager="npm"
)
```

**Notes:**
- Searches both dependencies and devDependencies
- `uninstall=True` runs `npm uninstall package-name`

---

### Tool: `update_specific_packages`

Update specific packages by name.

**Schema**: `UpdateSpecificPackagesInput`

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `package_names` | list[str] | Yes | - | List of package names |
| `package_json_path` | str | No | "package.json" | Path to package.json |
| `lock_major` | bool | No | True | Lock major version updates |
| `apply_updates` | bool | No | False | Run package manager install |
| `manager` | str | No | "npm" | Package manager |
| `npm_lookup` | bool | No | True | Query npm registry |

**Returns**: `str`

**Success Response:**
```
Target Node.js LTS: 22.11.0
Detected Node.js: 22.11.0
Updating 3 package(s)...

[UPDATE] express: ^4.17.1 -> ^4.19.2
[UPDATE] axios: ^0.21.1 -> ^1.6.7
[UPDATE] lodash: ^4.17.20 -> ^4.17.21

Successfully updated 3 package(s) in /tmp/project/package.json
Dependencies installed using npm
```

**Error Response:**
```
None of the specified packages found in package.json
```

**Example:**

```python
result = tools.update_specific_packages(
    package_names=["express", "axios", "lodash"],
    package_json_path="/tmp/project/package.json",
    lock_major=True,
    apply_updates=True
)
```

**Notes:**
- Only updates packages in the provided list
- Skips packages not found in package.json

---

### Tool: `get_package_info`

Get detailed information about a package.

**Schema**: `GetPackageInfoInput`

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `package_name` | str | Yes | - | Package name |
| `package_json_path` | str | No | "package.json" | Path to package.json |
| `npm_lookup` | bool | No | True | Query npm registry |

**Returns**: `str`

**Success Response:**
```
Current version in dependencies: ^4.17.1

Latest version: 4.19.2
Total versions available: 287
Node.js requirement (latest): >=0.10.0

Recent versions: 4.19.2, 4.19.1, 4.19.0, 4.18.3, 4.18.2
```

**Error Response:**
```
No information found for 'unknown-package'
```

**Example:**

```python
result = tools.get_package_info(
    package_name="express",
    package_json_path="/tmp/project/package.json",
    npm_lookup=True
)
```

**Notes:**
- Shows current version if in package.json
- Shows latest version and recent versions from npm
- Shows Node.js compatibility requirements

---

### Tool: `audit_packages`

Audit packages for security vulnerabilities.

**Schema**: `AuditPackagesInput`

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `package_json_path` | str | No | "package.json" | Path to package.json |
| `min_severity` | str \| None | No | None | Minimum severity (low/moderate/high/critical) |

**Returns**: `str`

**Success Response (No Vulnerabilities):**
```
Audit completed with exit code: 0

No vulnerabilities found!
```

**Success Response (Vulnerabilities Found):**
```
Audit completed with exit code: 1
Vulnerabilities detected. Details saved to audit.json

Vulnerability Summary:
  moderate: 2
  high: 3
  critical: 1
```

**Error Response:**
```
Error: package.json not found at /path/to/package.json
```

**Example:**

```python
# Audit all vulnerabilities
result = tools.audit_packages(
    package_json_path="/tmp/project/package.json"
)

# Only high and critical
result = tools.audit_packages(
    package_json_path="/tmp/project/package.json",
    min_severity="high"
)
```

**Notes:**
- Requires `npm` to be installed
- Requires `package-lock.json` to exist
- Saves detailed results to `audit.json` when vulnerabilities found
- Exit code 0 = no vulnerabilities, 1 = vulnerabilities found

---

## YAML Tools API

### Class: `YamlTools`

Tools for YAML file manipulation.

**Location**: `src/tools/yaml_tools.py`

#### Constructor

```python
YamlTools()
```

No parameters required.

---

### Tool: `read_yaml`

Read and display YAML file contents.

**Schema**: `ReadYamlInput`

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `yaml_file_path` | str | Yes | - | Path to YAML file |

**Returns**: `str`

**Success Response:**
```
Contents of 'serverless.yml':
service: my-service
provider:
  name: aws
  runtime: nodejs20.x
```

**Error Response:**
```
Error: File 'serverless.yml' does not exist.
```

**Example:**

```python
from src.tools.yaml_tools import YamlTools

tools = YamlTools()
result = tools.read_yaml(yaml_file_path="/tmp/project/serverless.yml")
```

---

### Tool: `update_yaml_attribute`

Update specific attribute in YAML file.

**Schema**: `UpdateYamlInput`

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `yaml_file_path` | str | Yes | - | Path to YAML file |
| `attribute_path` | str | Yes | - | Dot-separated path (e.g., "provider.runtime") |
| `new_value` | str | Yes | - | New value to set |

**Returns**: `str`

**Success Response:**
```
Successfully updated 'provider.runtime' in 'serverless.yml'. 
Old value: nodejs18.x, New value: nodejs20.x
```

**Error Response:**
```
Error: File 'serverless.yml' does not exist.
```

**Example:**

```python
# Update top-level attribute
result = tools.update_yaml_attribute(
    yaml_file_path="/tmp/project/serverless.yml",
    attribute_path="service",
    new_value="my-new-service"
)

# Update nested attribute
result = tools.update_yaml_attribute(
    yaml_file_path="/tmp/project/serverless.yml",
    attribute_path="provider.runtime",
    new_value="nodejs20.x"
)
```

**Notes:**
- Use dot notation for nested paths: `parent.child.attribute`
- Creates intermediate keys if they don't exist
- Preserves YAML formatting and comments

---

### Tool: `ensure_dict_key`

Ensure a key exists as a dictionary.

**Schema**: `EnsureDictKeyInput`

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `yaml_file_path` | str | Yes | - | Path to YAML file |
| `key_path` | str | Yes | - | Key path to ensure |

**Returns**: `str`

**Success Response:**
```
Success: Key 'custom' ensured as dictionary
```

**Error Response:**
```
Error: Key 'custom' exists but is not a dictionary
```

**Example:**

```python
result = tools.ensure_dict_key(
    yaml_file_path="/tmp/project/serverless.yml",
    key_path="custom"
)
```

**Notes:**
- Creates key if it doesn't exist
- Returns error if key exists but is not a dict
- Useful before adding attributes under a key

---

### Tool: `add_yaml_attributes`

Add multiple attributes under a parent key.

**Schema**: `AddAttributesInput`

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `yaml_file_path` | str | Yes | - | Path to YAML file |
| `parent_key` | str | Yes | - | Parent key to add under |
| `attributes_yaml` | str | Yes | - | YAML string of attributes |

**Returns**: `str`

**Success Response:**
```
Successfully added attributes under 'custom' in 'serverless.yml'
```

**Error Response:**
```
Error: Parent key 'custom' does not exist
```

**Example:**

```python
attributes_yaml = """
stage: ${opt:stage, 'dev'}
region: ${opt:region, 'us-east-1'}
tableName: my-table
"""

result = tools.add_yaml_attributes(
    yaml_file_path="/tmp/project/serverless.yml",
    parent_key="custom",
    attributes_yaml=attributes_yaml
)
```

**Notes:**
- `attributes_yaml` must be valid YAML
- Parent key must exist (use `ensure_dict_key` first)
- Merges with existing attributes

---

### Tool: `add_yaml_array_list`

Add array items to YAML file.

**Schema**: `AddArrayListInput`

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `yaml_file_path` | str | Yes | - | Path to YAML file |
| `parent_key` | str | Yes | - | Key for the array |
| `array_items_yaml` | str | Yes | - | YAML string of array items |

**Returns**: `str`

**Success Response:**
```
Successfully added array items under 'plugins' in 'serverless.yml'
```

**Error Response:**
```
Error: Invalid YAML format for array items
```

**Example:**

```python
# YAML array syntax
array_items = """
- serverless-offline
- serverless-plugin-typescript
"""

result = tools.add_yaml_array_list(
    yaml_file_path="/tmp/project/serverless.yml",
    parent_key="plugins",
    array_items_yaml=array_items
)

# JSON array syntax also works
array_items = "[serverless-offline, serverless-plugin-typescript]"

result = tools.add_yaml_array_list(
    yaml_file_path="/tmp/project/serverless.yml",
    parent_key="plugins",
    array_items_yaml=array_items
)
```

**Notes:**
- Supports both YAML and JSON array syntax
- Creates parent key if it doesn't exist
- Appends to existing array

---

## JSON Tools API

### Class: `JsonTools`

Tools for JSON manipulation.

**Location**: `src/tools/json_tools.py`

#### Constructor

```python
JsonTools()
```

No parameters required.

---

### Tool: `parse_json`

Parse JSON string to dictionary.

**Schema**: `ParseJsonInput`

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `json_string` | str | Yes | - | JSON string to parse |

**Returns**: `dict`

**Success Response:**
```python
{'name': 'my-app', 'version': '1.0.0'}
```

**Error Response:**
```python
JSONDecodeError: Expecting ',' delimiter: line 1 column 20
```

**Example:**

```python
from src.tools.json_tools import JsonTools

tools = JsonTools()
result = tools.parse_json(
    json_string='{"name": "my-app", "version": "1.0.0"}'
)
```

---

### Tool: `add_new_attribute`

Add attribute to JSON object.

**Schema**: `AddJsonAttributeInput`

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `json_data` | dict | Yes | - | Original JSON object |
| `key` | str | Yes | - | Key for new attribute |
| `value` | str | Yes | - | Value for new attribute |

**Returns**: `dict`

**Success Response:**
```python
{'name': 'my-app', 'description': 'My awesome app'}
```

**Example:**

```python
json_data = {'name': 'my-app'}

result = tools.add_new_attribute(
    json_data=json_data,
    key="description",
    value="My awesome app"
)
```

---

### Tool: `save_json_to_file`

Save JSON object to file.

**Schema**: `SaveJsonToFileInput`

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `json_data` | dict | Yes | - | JSON object to save |
| `file_path` | str | Yes | - | File path to save to |

**Returns**: `None`

**Example:**

```python
json_data = {
    'name': 'my-config',
    'settings': {'debug': True}
}

tools.save_json_to_file(
    json_data=json_data,
    file_path="/tmp/config.json"
)
```

**Notes:**
- Creates file if doesn't exist
- Overwrites existing file
- Formats with 2-space indentation

---

## Schema Reference

### GitHub Schemas

**Location**: `src/schemas/github_schemas.py`

#### `ReadRepoInput`

```python
class ReadRepoInput(BaseModel):
    repository: str = Field(description="Repository name in format 'owner/repo'")
    branch: str = Field(default="main", description="Branch name")
```

#### `CloneRepoInput`

```python
class CloneRepoInput(BaseModel):
    repository: str = Field(description="Repository URL or name in format 'owner/repo'")
    clone_path: str = Field(default="/tmp/repo", description="Local path to clone to")
```

#### `CheckoutBranchInput`

```python
class CheckoutBranchInput(BaseModel):
    repo_path: str = Field(description="Local path of the cloned repository")
    branch: str = Field(description="Branch name to checkout")
```

#### `ListRepoFilesInput`

```python
class ListRepoFilesInput(BaseModel):
    repo_path: str = Field(description="Local path of the cloned repository")
```

---

### Package Schemas

**Location**: `src/schemas/package_schemas.py`

#### `AnalyzePackagesInput`

```python
class AnalyzePackagesInput(BaseModel):
    package_json_path: str = Field(default="package.json")
    lock_major: bool = Field(default=True)
    npm_lookup: bool = Field(default=True)
```

#### `UpdatePackagesInput`

```python
class UpdatePackagesInput(BaseModel):
    package_json_path: str = Field(default="package.json")
    lock_major: bool = Field(default=True)
    dry_run: bool = Field(default=False)
    apply_updates: bool = Field(default=False)
    manager: str = Field(default="npm")
    npm_lookup: bool = Field(default=True)
```

#### `AddPackageInput`

```python
class AddPackageInput(BaseModel):
    package_name: str = Field(...)
    version: Optional[str] = Field(default=None)
    package_json_path: str = Field(default="package.json")
    dev: bool = Field(default=False)
    install: bool = Field(default=False)
    manager: str = Field(default="npm")
    npm_lookup: bool = Field(default=True)
    node_lts_version: Optional[str] = Field(default=None)
```

#### `RemovePackageInput`

```python
class RemovePackageInput(BaseModel):
    package_name: str = Field(...)
    package_json_path: str = Field(default="package.json")
    uninstall: bool = Field(default=False)
    manager: str = Field(default="npm")
```

#### `UpdateSpecificPackagesInput`

```python
class UpdateSpecificPackagesInput(BaseModel):
    package_names: list[str] = Field(...)
    package_json_path: str = Field(default="package.json")
    lock_major: bool = Field(default=True)
    apply_updates: bool = Field(default=False)
    manager: str = Field(default="npm")
    npm_lookup: bool = Field(default=True)
```

#### `GetPackageInfoInput`

```python
class GetPackageInfoInput(BaseModel):
    package_name: str = Field(...)
    package_json_path: str = Field(default="package.json")
    npm_lookup: bool = Field(default=True)
```

#### `AuditPackagesInput`

```python
class AuditPackagesInput(BaseModel):
    package_json_path: str = Field(default="package.json")
    min_severity: Optional[str] = Field(default=None)
```

---

### YAML Schemas

**Location**: `src/schemas/yaml_schemas.py`

#### `ReadYamlInput`

```python
class ReadYamlInput(BaseModel):
    yaml_file_path: str = Field(description="Path to the YAML file to read")
```

#### `UpdateYamlInput`

```python
class UpdateYamlInput(BaseModel):
    yaml_file_path: str = Field(description="Path to the YAML file to update")
    attribute_path: str = Field(description="Dot-separated path to the attribute")
    new_value: str = Field(description="New value to set for the attribute")
```

#### `EnsureDictKeyInput`

```python
class EnsureDictKeyInput(BaseModel):
    yaml_file_path: str = Field(description="Path to the YAML file")
    key_path: str = Field(description="Key path to ensure exists as a dictionary")
```

#### `AddAttributesInput`

```python
class AddAttributesInput(BaseModel):
    yaml_file_path: str = Field(description="Path to the YAML file")
    parent_key: str = Field(description="Parent key to add attributes under")
    attributes_yaml: str = Field(description="YAML formatted string of attributes to add")
```

#### `AddArrayListInput`

```python
class AddArrayListInput(BaseModel):
    yaml_file_path: str = Field(description="Path to the YAML file")
    parent_key: str = Field(description="Key to add the array list under")
    array_items_yaml: str = Field(description="YAML formatted string of array items")
```

---

### JSON Schemas

**Location**: `src/schemas/json_schemas.py`

#### `ParseJsonInput`

```python
class ParseJsonInput(BaseModel):
    json_string: str = Field(..., description="The JSON string to parse into a dictionary")
```

#### `AddJsonAttributeInput`

```python
class AddJsonAttributeInput(BaseModel):
    json_data: dict = Field(..., description="The original JSON object as a dictionary")
    key: str = Field(..., description="The key for the new attribute to add")
    value: str = Field(..., description="The value for the new attribute to add")
```

#### `SaveJsonToFileInput`

```python
class SaveJsonToFileInput(BaseModel):
    json_data: dict = Field(..., description="The JSON object as a dictionary to save")
    file_path: str = Field(..., description="The path to the file where the JSON should be saved")
```

---

## Utility Functions

### GithubUtils

**Location**: `src/utils/github_utils.py`

Key utility functions for GitHub operations:

| Function | Parameters | Returns | Description |
|----------|-----------|---------|-------------|
| `get_repo_info` | `github: Github, repository: str, branch: str` | `tuple[list, Exception]` | Get repository information |
| `clone_repo` | `repository_url: str, clone_path: str` | `tuple[bool, str]` | Clone repository |
| `checkout_branch_cmd` | `repo_path: str, branch: str` | `tuple[bool, str]` | Checkout branch |
| `list_files_in_local_repo` | `repo_path: str` | `tuple[bool, str]` | List repository files |
| `convert_repo_to_url` | `repository: str` | `str` | Convert owner/repo to URL |
| `remove_directory` | `path: str` | `None` | Remove directory |
| `count_files_in_directory` | `path: str` | `int` | Count files |

---

### PackageUpdatesUtils

**Location**: `src/utils/package_updates_utils.py`

Key utility functions for package management:

| Function | Parameters | Returns | Description |
|----------|-----------|---------|-------------|
| `fetch_packument` | `package_name: str, registry: str` | `dict` | Fetch package metadata |
| `choose_best_version` | `name: str, current_range: str, node_ver: str, lock_major: bool, packument: dict` | `str \| None` | Choose best version |
| `detect_node_version` | `pkg: dict` | `str` | Detect Node.js version |
| `load_deps` | `pkg: dict` | `dict` | Load dependencies |
| `update_pkg_ranges` | `pkg: dict, proposed: dict` | `dict` | Update package ranges |
| `run_package_manager_install` | `manager: str, cwd: str` | `None` | Run install command |
| `run_npm_audit` | `min_severity: str \| None` | `tuple[int, dict]` | Run npm audit |

---

### YamlUtils

**Location**: `src/utils/yaml_utils.py`

Key utility functions for YAML operations:

| Function | Parameters | Returns | Description |
|----------|-----------|---------|-------------|
| `parse_yaml` | `file_path: str` | `dict` | Parse YAML file |
| `write_yaml` | `file_path: str, data: dict` | `None` | Write YAML file |
| `file_exists` | `file_path: str` | `bool` | Check file exists |
| `set_nested_value` | `data: dict, path: str, value: any` | `tuple[any, any]` | Set nested value |
| `ensure_key_is_dict` | `data: dict, key_path: str` | `tuple[bool, str]` | Ensure key is dict |

---

### JsonUtils

**Location**: `src/utils/json_utils.py`

Key utility functions for JSON operations:

| Function | Parameters | Returns | Description |
|----------|-----------|---------|-------------|
| `read_json` | `file_path: Path \| str` | `dict` | Read JSON file |
| `write_json` | `file_path: Path \| str, data: dict` | `None` | Write JSON file |
| `parse_json` | `json_string: str` | `dict` | Parse JSON string |
| `add_attribute` | `json_data: dict, key: str, value: any` | `dict` | Add attribute |

---

## Service APIs

### InstructionService

**Location**: `src/services/instruction_service.py`

Generates instructions for agent execution.

#### Constructor

```python
InstructionService(
    repository: str,
    clone_path: str,
    branch: str,
    node_lts_version: str
)
```

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `repository` | str | Repository in format 'owner/repo' |
| `clone_path` | str | Path to clone repository |
| `branch` | str | Branch name |
| `node_lts_version` | str | Node.js LTS version |

#### Methods

##### `get_all_instructions()`

Get all instructions (GitHub + Serverless + Package operations).

**Returns**: `list[str]`

**Example:**

```python
from src.services.instruction_service import InstructionService

service = InstructionService(
    repository="owner/repo",
    clone_path="/tmp/clone",
    branch="main",
    node_lts_version="22.11.0"
)

instructions = service.get_all_instructions()
for instruction in instructions:
    print(instruction)
```

---

## Error Responses

All tools return errors as formatted strings rather than raising exceptions. This design allows the LLM agent to understand and respond to errors.

### Common Error Patterns

| Error Type | Format | Example |
|------------|--------|---------|
| File Not Found | `Error: <file> not found at <path>` | `Error: package.json not found at /tmp/project/package.json` |
| Missing Dependency | `Error: <tool> not installed` | `Error: npm not installed` |
| API Error | `Error <operation>: <details>` | `Error cloning repository: Authentication failed` |
| Validation Error | `Error: <validation message>` | `Error: Package 'lodash' already exists in dependencies` |
| Network Error | `[SKIP] <package>: <error>` | `[SKIP] express: registry fetch failed: timeout` |

### HTTP Status Codes (GitHub API)

| Code | Meaning | Example Error |
|------|---------|---------------|
| 401 | Unauthorized | `401 Bad credentials` |
| 403 | Forbidden | `403 API rate limit exceeded` |
| 404 | Not Found | `404 Repository not found` |
| 422 | Validation Failed | `422 Validation Failed` |

---

## Type Definitions

### Common Types

```python
# Package manager types
PackageManager = Literal["npm", "yarn", "pnpm"]

# Severity levels
Severity = Literal["low", "moderate", "high", "critical"]

# Node version format
NodeVersion = str  # e.g., "22.11.0", "18.17.0"

# Repository format
Repository = str  # e.g., "owner/repo" or "https://github.com/owner/repo.git"

# Version range
VersionRange = str  # e.g., "^1.0.0", "~2.3.4", ">=3.0.0"
```

---

## Usage Patterns

### Pattern 1: Sequential Tool Execution

```python
# Clone, then analyze, then update
executor.invoke({"messages": [{"role": "user", "content": "Clone repo X"}]})
executor.invoke({"messages": [{"role": "user", "content": "Analyze packages"}]})
executor.invoke({"messages": [{"role": "user", "content": "Update packages"}]})
```

### Pattern 2: Batch Instructions

```python
# Single instruction with multiple steps
instruction = """
1. Clone repository owner/repo to /tmp/clone
2. Checkout branch develop
3. Analyze packages in /tmp/clone/package.json
4. Update packages with lock_major=True
"""
executor.invoke({"messages": [{"role": "user", "content": instruction}]})
```

### Pattern 3: Direct Tool Usage (Without Agent)

```python
# Use tools directly without agent
from src.tools.package_updates_tools import PackageUpdatesTools

tools = PackageUpdatesTools(node_lts_version="22.11.0")
result = tools.analyze_packages(package_json_path="/tmp/project/package.json")
```

---

## Rate Limits

### npm Registry

- **Authenticated**: 5,000 requests/hour
- **Unauthenticated**: 50 requests/hour
- **Burst**: 100 requests/minute

### GitHub API

- **Authenticated**: 5,000 requests/hour
- **Unauthenticated**: 60 requests/hour
- **Search API**: 30 requests/minute

---

## Best Practices

### 1. Always Use Absolute Paths

```python
# ✅ Good
analyze_packages(package_json_path="/tmp/project/package.json")

# ❌ Bad
analyze_packages(package_json_path="package.json")  # May fail depending on cwd
```

### 2. Validate Before Operations

```python
# Always check file exists before operations
import os
if not os.path.exists(package_json_path):
    print(f"Error: File not found: {package_json_path}")
```

### 3. Use Dry Run First

```python
# Preview changes before applying
result = update_packages(dry_run=True)
print(result)  # Review changes

# Then apply
result = update_packages(dry_run=False, apply_updates=True)
```

### 4. Handle Errors Gracefully

```python
# Check for error in response
result = clone_repository(...)
if "Error" in result:
    print(f"Clone failed: {result}")
    # Handle error
else:
    print(f"Clone succeeded: {result}")
```

### 5. Use npm_lookup Wisely

```python
# For faster operations without registry checks
analyze_packages(npm_lookup=False)  # Much faster

# For accurate version information
analyze_packages(npm_lookup=True)   # Slower but accurate
```

---

## Version Compatibility

| Component | Version | Notes |
|-----------|---------|-------|
| Python | 3.11+ | Required |
| LangChain | 1.2.0 | Exact version |
| langchain-google-genai | 4.1.2 | Exact version |
| langchain-classic | 1.0.1 | Exact version |
| Pydantic | 2.0+ | Minimum version |
| Node.js | 18.0+ | For npm operations |
| npm | 8.0+ | For package management |

---

## Migration Guide

### From v2.0 to v2.1

**Breaking Changes:**

1. Agent creation changed from `create_react_agent` to `create_agent`
2. `npm_lookup` parameter added to all package tools

**Migration:**

```python
# Old (v2.0)
from langchain_classic.agents import create_react_agent
agent = create_react_agent(model, tools, prompt)

# New (v2.1)
from langchain.agents import create_agent
agent = create_agent(model, tools, system_prompt)
```

---

## Appendix

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GOOGLE_API_KEY` | Yes | - | Google Gemini API key |
| `GITHUB_TOKEN` | No | - | GitHub personal access token |
| `NPM_REGISTRY` | No | https://registry.npmjs.org | npm registry URL |

### File Paths

All file paths in CodeBaseOpsAI-v2-1:

- Must be absolute paths
- Must use forward slashes (/)
- No Windows drive letters in tool responses
- UTF-8 encoding assumed

### Supported Package Managers

| Manager | Install Command | Uninstall Command | Lock File |
|---------|----------------|-------------------|-----------|
| npm | `npm install` | `npm uninstall` | package-lock.json |
| yarn | `yarn install` | `yarn remove` | yarn.lock |
| pnpm | `pnpm install` | `pnpm remove` | pnpm-lock.yaml |

---

**Last Updated**: January 2026  
**Version**: 2.1.0  
**API Version**: 1.0
