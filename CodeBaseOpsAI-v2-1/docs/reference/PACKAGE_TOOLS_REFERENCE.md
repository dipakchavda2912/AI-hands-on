# 📦 Package Tools Reference - CodeBaseOpsAI-v2-1

**Comprehensive guide to all 7 npm package management tools.**

---

## Table of Contents

1. [Overview](#overview)
2. [Tool 1: analyze_packages](#tool-1-analyze_packages)
3. [Tool 2: update_packages](#tool-2-update_packages)
4. [Tool 3: add_package](#tool-3-add_package)
5. [Tool 4: update_specific_packages](#tool-4-update_specific_packages)
6. [Tool 5: get_package_info](#tool-5-get_package_info)
7. [Tool 6: audit_packages](#tool-6-audit_packages)
8. [Tool 7: remove_package](#tool-7-remove_package)
9. [Advanced Usage Patterns](#advanced-usage-patterns)
10. [Real-World Use Cases](#real-world-use-cases)
11. [Best Practices](#best-practices)
12. [Troubleshooting](#troubleshooting)

---

## Overview

The Package Management Tools provide comprehensive npm dependency management capabilities with intelligent version resolution, Node.js compatibility checking, and vulnerability scanning.

### Core Features

- **Smart Version Resolution**: Automatically finds latest compatible versions
- **Node.js Compatibility**: Ensures packages work with target Node.js version
- **Vulnerability Filtering**: Excludes packages with known security issues
- **Major Version Locking**: Prevents breaking changes with `lock_major`
- **Dry Run Support**: Preview changes before applying
- **Multiple Package Managers**: Supports npm, yarn, and pnpm
- **Offline Mode**: Works without npm registry (`npm_lookup=False`)

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│           PackageUpdatesTools                           │
├─────────────────────────────────────────────────────────┤
│  - node_lts_version: str                                │
│  - npm_registry: str                                    │
└─────────────────┬───────────────────────────────────────┘
                  │
    ┌─────────────┼─────────────┬──────────────────┐
    ▼             ▼             ▼                  ▼
┌─────────┐  ┌─────────┐  ┌─────────┐       ┌─────────┐
│ analyze │  │ update  │  │   add   │  ...  │ remove  │
│packages │  │packages │  │ package │       │package  │
└─────────┘  └─────────┘  └─────────┘       └─────────┘
     │            │            │                   │
     └────────────┴────────────┴───────────────────┘
                  │
                  ▼
     ┌────────────────────────────┐
     │   PackageUpdatesUtils      │
     │  - fetch_packument()       │
     │  - choose_best_version()   │
     │  - update_pkg_ranges()     │
     └────────────────────────────┘
```

### Version Selection Algorithm

For each package, the tools:

1. **Fetch** package metadata from npm registry
2. **Filter** versions compatible with Node.js version
3. **Exclude** versions with known vulnerabilities
4. **Apply** major version lock if enabled
5. **Select** highest remaining version
6. **Format** as caret range (^x.y.z)

---

## Tool 1: analyze_packages

### Description

Analyze package dependencies and suggest updates without modifying files. Perfect for getting an overview of available updates.

### Function Signature

```python
def analyze_packages(
    package_json_path: str = "package.json",
    lock_major: bool = True,
    npm_lookup: bool = True
) -> str
```

### Parameters

#### `package_json_path` (str, default: "package.json")

Path to the package.json file to analyze.

**Valid Values:**
- Absolute path: `/tmp/project/package.json`
- Relative path: `package.json` (relative to current directory)

**Example:**
```python
analyze_packages(package_json_path="/tmp/my-project/package.json")
```

#### `lock_major` (bool, default: True)

Whether to prevent major version updates.

**When True:**
- `^4.17.1` → `^4.19.2` ✅ (minor/patch update)
- `^4.17.1` → `^5.0.0` ❌ (major update prevented)

**When False:**
- `^4.17.1` → `^5.0.0` ✅ (major update allowed)

**Example:**
```python
# Conservative updates (recommended)
analyze_packages(lock_major=True)

# Allow breaking changes
analyze_packages(lock_major=False)
```

#### `npm_lookup` (bool, default: True)

Whether to query npm registry for package versions.

**When True:**
- Fetches latest versions from npm
- Checks Node.js compatibility
- Filters vulnerable versions
- Slower but accurate

**When False:**
- No network requests
- No version checks
- Much faster
- Use for offline environments

**Example:**
```python
# Full analysis with npm lookup
analyze_packages(npm_lookup=True)

# Quick local analysis
analyze_packages(npm_lookup=False)
```

### Return Value

Returns a formatted string with analysis results.

**Success Format:**
```
Target Node.js LTS: 22.11.0
Detected Node.js version: 22.11.0
Found 25 dependencies to evaluate.

[UPDATE] express: ^4.17.1 -> ^4.19.2
[UPDATE] lodash: ^4.17.20 -> ^4.17.21
[UPDATE] axios: ^0.21.1 -> ^1.6.7
[WARN] old-package: no compatible & non-vulnerable version found

Total updates proposed: 23
```

**Error Format:**
```
Error: package.json not found at /path/to/package.json
```

### Basic Examples

#### Example 1: Simple Analysis

```python
from src.tools.package_updates_tools import PackageUpdatesTools

tools = PackageUpdatesTools(node_lts_version="22.11.0")

result = tools.analyze_packages(
    package_json_path="/tmp/project/package.json"
)

print(result)
```

**Output:**
```
Target Node.js LTS: 22.11.0
Found 15 dependencies to evaluate.

[UPDATE] express: ^4.17.1 -> ^4.19.2
[UPDATE] axios: ^0.21.1 -> ^1.6.7
...
Total updates proposed: 12
```

#### Example 2: Allow Major Updates

```python
result = tools.analyze_packages(
    package_json_path="/tmp/project/package.json",
    lock_major=False  # Allow major version updates
)
```

**Output:**
```
[UPDATE] express: ^4.17.1 -> ^5.0.0  # Major update allowed
[UPDATE] webpack: ^4.46.0 -> ^5.90.0
```

#### Example 3: Offline Analysis

```python
# Fast analysis without npm lookup
result = tools.analyze_packages(
    package_json_path="/tmp/project/package.json",
    npm_lookup=False  # No network calls
)
```

**Output:**
```
npm_lookup is disabled. Skipping npm registry version checks.
```

### Advanced Examples

#### Parse and Filter Results

```python
result = tools.analyze_packages(package_json_path="/tmp/project/package.json")

# Extract update count
lines = result.split('\n')
update_lines = [line for line in lines if '[UPDATE]' in line]
print(f"Found {len(update_lines)} updates")

# Extract specific packages
for line in update_lines:
    if 'express' in line:
        print(f"Express update: {line}")
```

#### Compare Different Strategies

```python
# Strategy 1: Conservative (lock major)
conservative = tools.analyze_packages(
    package_json_path="/tmp/project/package.json",
    lock_major=True
)

# Strategy 2: Aggressive (allow major)
aggressive = tools.analyze_packages(
    package_json_path="/tmp/project/package.json",
    lock_major=False
)

print("Conservative Updates:")
print(conservative)
print("\nAggressive Updates:")
print(aggressive)
```

### Use Cases

1. **Pre-Update Review**: Check what updates are available before applying
2. **Dependency Audit**: Regular review of package versions
3. **CI/CD Integration**: Automated dependency monitoring
4. **Migration Planning**: Identify packages requiring major updates
5. **Documentation**: Generate dependency status reports

### Performance

| Scenario | Package Count | Time (npm_lookup=True) | Time (npm_lookup=False) |
|----------|---------------|------------------------|-------------------------|
| Small Project | 10 packages | ~5 seconds | <1 second |
| Medium Project | 50 packages | ~15 seconds | <1 second |
| Large Project | 100+ packages | ~30 seconds | <1 second |

### Tips

- **Always analyze before updating**: See what changes before applying
- **Use lock_major=True in production**: Prevent breaking changes
- **Cache results**: Save analysis output for documentation
- **Run regularly**: Keep dependencies up to date

---

## Tool 2: update_packages

### Description

Update all package dependencies in package.json with latest compatible versions. The most powerful tool for comprehensive dependency updates.

### Function Signature

```python
def update_packages(
    package_json_path: str = "package.json",
    lock_major: bool = True,
    dry_run: bool = False,
    apply_updates: bool = False,
    manager: str = "npm",
    npm_lookup: bool = True
) -> str
```

### Parameters

#### `package_json_path` (str, default: "package.json")

Path to package.json file to update.

#### `lock_major` (bool, default: True)

Prevent major version updates to avoid breaking changes.

#### `dry_run` (bool, default: False)

Preview changes without modifying package.json.

**Recommended Workflow:**
1. Run with `dry_run=True` to preview
2. Review changes
3. Run with `dry_run=False` to apply

**Example:**
```python
# Step 1: Preview
result = tools.update_packages(dry_run=True)
print(result)  # Review changes

# Step 2: Apply
result = tools.update_packages(dry_run=False)
```

#### `apply_updates` (bool, default: False)

Run package manager install after updating package.json.

**When True:**
- Updates package.json
- Runs `npm install` (or yarn/pnpm)
- Updates lock file
- Installs new versions

**When False:**
- Only updates package.json
- Manual `npm install` required

**Example:**
```python
# Update and install
tools.update_packages(
    dry_run=False,
    apply_updates=True  # Runs npm install
)
```

#### `manager` (str, default: "npm")

Package manager to use for installation.

**Valid Values:**
- `"npm"` - Uses `npm install`
- `"yarn"` - Uses `yarn install`
- `"pnpm"` - Uses `pnpm install`

**Example:**
```python
tools.update_packages(
    apply_updates=True,
    manager="yarn"  # Use yarn instead of npm
)
```

#### `npm_lookup` (bool, default: True)

Query npm registry for version information.

### Return Value

**Success (dry_run=True):**
```
Target Node.js LTS: 22.11.0
[UPDATE] express: ^4.17.1 -> ^4.19.2
[UPDATE] axios: ^0.21.1 -> ^1.6.7

Dry-run mode: package.json not modified.
```

**Success (dry_run=False):**
```
[UPDATE] express: ^4.17.1 -> ^4.19.2
[UPDATE] axios: ^0.21.1 -> ^1.6.7

Successfully updated /tmp/project/package.json
```

**Success (with apply_updates=True):**
```
[UPDATE] express: ^4.17.1 -> ^4.19.2

Successfully updated /tmp/project/package.json
Dependencies installed using npm
```

### Basic Examples

#### Example 1: Safe Update Workflow

```python
from src.tools.package_updates_tools import PackageUpdatesTools

tools = PackageUpdatesTools(node_lts_version="22.11.0")

# Step 1: Dry run
print("=== DRY RUN ===")
result = tools.update_packages(
    package_json_path="/tmp/project/package.json",
    dry_run=True
)
print(result)

# Step 2: Review and apply
print("\n=== APPLYING UPDATES ===")
result = tools.update_packages(
    package_json_path="/tmp/project/package.json",
    dry_run=False,
    apply_updates=True
)
print(result)
```

#### Example 2: Update with Different Package Manager

```python
# Use yarn
result = tools.update_packages(
    package_json_path="/tmp/project/package.json",
    dry_run=False,
    apply_updates=True,
    manager="yarn"
)
```

#### Example 3: Update Without Installing

```python
# Just update package.json, don't install
result = tools.update_packages(
    package_json_path="/tmp/project/package.json",
    dry_run=False,
    apply_updates=False  # No npm install
)

# Later, manually run:
# npm install
```

### Advanced Examples

#### Conditional Updates Based on Analysis

```python
# Analyze first
analysis = tools.analyze_packages(package_json_path="/tmp/project/package.json")

# Count updates
update_count = analysis.count('[UPDATE]')

if update_count > 0:
    print(f"Found {update_count} updates. Applying...")
    result = tools.update_packages(
        package_json_path="/tmp/project/package.json",
        dry_run=False,
        apply_updates=True
    )
else:
    print("No updates needed")
```

#### Progressive Update Strategy

```python
# First, update with major version lock
print("Phase 1: Safe updates (lock major)")
result = tools.update_packages(
    package_json_path="/tmp/project/package.json",
    lock_major=True,
    dry_run=False,
    apply_updates=True
)

# Test application...
# If tests pass, then update with major versions

print("Phase 2: Major updates")
result = tools.update_packages(
    package_json_path="/tmp/project/package.json",
    lock_major=False,
    dry_run=False,
    apply_updates=True
)
```

#### Batch Update Multiple Projects

```python
projects = [
    "/tmp/project1/package.json",
    "/tmp/project2/package.json",
    "/tmp/project3/package.json"
]

for project in projects:
    print(f"\nUpdating {project}")
    result = tools.update_packages(
        package_json_path=project,
        dry_run=False,
        apply_updates=True
    )
    print(result)
```

### Use Cases

1. **Regular Maintenance**: Monthly dependency updates
2. **Security Patches**: Update to fix vulnerabilities
3. **CI/CD Automation**: Automated dependency management
4. **Project Migration**: Upgrade projects to newer versions
5. **Monorepo Management**: Update all packages in workspace

### Best Practices

#### ✅ Do

- **Always dry run first**
  ```python
  # Good
  result = tools.update_packages(dry_run=True)  # Preview
  result = tools.update_packages(dry_run=False)  # Apply
  ```

- **Use lock_major in production**
  ```python
  # Good for production
  tools.update_packages(lock_major=True)
  ```

- **Test after updating**
  ```python
  tools.update_packages(dry_run=False, apply_updates=True)
  # Run tests
  # npm test
  ```

- **Commit lock files**
  ```bash
  git add package.json package-lock.json
  git commit -m "Update dependencies"
  ```

#### ❌ Don't

- **Update blindly**
  ```python
  # Bad - no preview
  tools.update_packages(dry_run=False, apply_updates=True)
  ```

- **Use lock_major=False without testing**
  ```python
  # Risky - may break application
  tools.update_packages(lock_major=False, apply_updates=True)
  ```

- **Update production directly**
  ```python
  # Bad - test in dev/staging first
  tools.update_packages(package_json_path="/production/package.json")
  ```

### Error Handling

```python
result = tools.update_packages(
    package_json_path="/tmp/project/package.json",
    dry_run=False
)

if "Error" in result:
    print(f"Update failed: {result}")
    # Handle error
elif "Successfully updated" in result:
    print("Update successful!")
    # Proceed with testing
else:
    print(f"Unexpected result: {result}")
```

---

## Tool 3: add_package

### Description

Add a new package to package.json with automatic version resolution. Intelligently finds the latest compatible version.

### Function Signature

```python
def add_package(
    package_name: str,
    version: str | None = None,
    package_json_path: str = "package.json",
    dev: bool = False,
    install: bool = False,
    manager: str = "npm",
    npm_lookup: bool = True,
    node_lts_version: str | None = None
) -> str
```

### Parameters

#### `package_name` (str, **required**)

Name of the package to add.

**Formats:**
- Simple name: `lodash`
- Scoped package: `@types/node`
- Organization package: `@angular/core`

**Example:**
```python
add_package(package_name="lodash")
add_package(package_name="@types/node")
add_package(package_name="@angular/core")
```

#### `version` (str | None, default: None)

Version to install. If None, finds latest compatible.

**Valid Values:**
- `None` - Auto-detect latest compatible
- `"latest"` - Auto-detect latest compatible
- `"^1.0.0"` - Specific range
- `"~2.3.4"` - Tilde range
- `"1.2.3"` - Exact version

**Example:**
```python
# Auto-detect
add_package(package_name="lodash", version=None)

# Specific version
add_package(package_name="lodash", version="^4.17.21")

# Exact version
add_package(package_name="lodash", version="4.17.21")
```

#### `dev` (bool, default: False)

Add as development dependency.

**When True:**
- Adds to `devDependencies`
- For build tools, testing frameworks, type definitions

**When False:**
- Adds to `dependencies`
- For runtime dependencies

**Example:**
```python
# Production dependency
add_package(package_name="express", dev=False)

# Development dependency
add_package(package_name="@types/node", dev=True)
```

#### `install` (bool, default: False)

Run package manager install after adding.

**Example:**
```python
# Add and install
add_package(
    package_name="lodash",
    install=True  # Runs npm install
)
```

#### `manager` (str, default: "npm")

Package manager to use.

**Valid Values:** `"npm"`, `"yarn"`, `"pnpm"`

#### `npm_lookup` (bool, default: True)

Query npm registry for version information.

**When False:**
- Uses specified version or "latest"
- No compatibility checking
- Faster but less safe

#### `node_lts_version` (str | None, default: None)

Override Node.js version for this operation.

**Example:**
```python
add_package(
    package_name="some-package",
    node_lts_version="20.10.0"  # Override default
)
```

### Return Value

**Success:**
```
Successfully added 'lodash@^4.17.21' to dependencies
```

**Success with install:**
```
Successfully added 'lodash@^4.17.21' to dependencies
Package installed using npm
```

**Error (already exists):**
```
Error: Package 'lodash' already exists in dependencies
```

**Error (not found):**
```
Error: Could not find compatible version for 'unknown-package' compatible with Node.js 22.11.0
```

### Basic Examples

#### Example 1: Add Production Dependency

```python
from src.tools.package_updates_tools import PackageUpdatesTools

tools = PackageUpdatesTools(node_lts_version="22.11.0")

result = tools.add_package(
    package_name="express",
    package_json_path="/tmp/project/package.json"
)

print(result)
# Output: Successfully added 'express@^4.19.2' to dependencies
```

#### Example 2: Add Dev Dependency

```python
result = tools.add_package(
    package_name="@types/node",
    package_json_path="/tmp/project/package.json",
    dev=True  # Add to devDependencies
)

print(result)
# Output: Successfully added '@types/node@^22.0.0' to devDependencies
```

#### Example 3: Add and Install

```python
result = tools.add_package(
    package_name="axios",
    package_json_path="/tmp/project/package.json",
    install=True  # Also run npm install
)

print(result)
# Output: Successfully added 'axios@^1.6.7' to dependencies
#         Package installed using npm
```

#### Example 4: Add Specific Version

```python
result = tools.add_package(
    package_name="lodash",
    version="^4.17.20",  # Specific version
    package_json_path="/tmp/project/package.json"
)
```

### Advanced Examples

#### Add Multiple Packages

```python
packages = [
    ("express", False),      # (name, dev)
    ("axios", False),
    ("@types/node", True),
    ("@types/express", True)
]

for pkg_name, is_dev in packages:
    result = tools.add_package(
        package_name=pkg_name,
        package_json_path="/tmp/project/package.json",
        dev=is_dev,
        install=False  # Install all at once later
    )
    print(result)

# Install all at once
# npm install
```

#### Conditional Add (Check if exists first)

```python
import json

# Read package.json
with open("/tmp/project/package.json", 'r') as f:
    pkg = json.load(f)

# Check if package exists
package_name = "lodash"
exists = (
    ("dependencies" in pkg and package_name in pkg["dependencies"]) or
    ("devDependencies" in pkg and package_name in pkg["devDependencies"])
)

if not exists:
    result = tools.add_package(
        package_name=package_name,
        package_json_path="/tmp/project/package.json"
    )
    print(result)
else:
    print(f"Package {package_name} already exists")
```

#### Add with Version Fallback

```python
# Try latest compatible first
result = tools.add_package(
    package_name="some-package",
    package_json_path="/tmp/project/package.json"
)

if "Could not find compatible version" in result:
    # Fallback: add specific older version
    result = tools.add_package(
        package_name="some-package",
        version="^1.0.0",  # Older version
        package_json_path="/tmp/project/package.json",
        npm_lookup=False
    )
```

### Use Cases

1. **Initial Project Setup**: Add core dependencies
2. **Feature Development**: Add new library for feature
3. **Testing Setup**: Add testing frameworks
4. **Type Definitions**: Add TypeScript types
5. **Tool Installation**: Add development tools

### Common Packages by Category

#### Web Frameworks
```python
add_package("express")      # Node.js web framework
add_package("koa")          # Lightweight web framework
add_package("fastify")      # Fast web framework
```

#### HTTP Clients
```python
add_package("axios")        # Promise-based HTTP client
add_package("node-fetch")   # Fetch API for Node.js
add_package("got")          # Human-friendly HTTP client
```

#### Utilities
```python
add_package("lodash")       # Utility library
add_package("date-fns")     # Date utilities
add_package("ramda")        # Functional programming
```

#### TypeScript Types (dev)
```python
add_package("@types/node", dev=True)
add_package("@types/express", dev=True)
add_package("@types/lodash", dev=True)
```

#### Testing (dev)
```python
add_package("jest", dev=True)
add_package("mocha", dev=True)
add_package("chai", dev=True)
```

### Tips

- **Use specific versions for stability**
  ```python
  add_package(package_name="react", version="^18.2.0")
  ```

- **Install type definitions with packages**
  ```python
  add_package("express")
  add_package("@types/express", dev=True)
  ```

- **Group related packages**
  ```python
  # Add all at once, install once
  add_package("react", install=False)
  add_package("react-dom", install=False)
  # Then: npm install
  ```

---

## Tool 4: update_specific_packages

### Description

Update only specific packages by name. Perfect for targeted updates when you don't want to update everything.

### Function Signature

```python
def update_specific_packages(
    package_names: list[str],
    package_json_path: str = "package.json",
    lock_major: bool = True,
    apply_updates: bool = False,
    manager: str = "npm",
    npm_lookup: bool = True
) -> str
```

### Parameters

#### `package_names` (list[str], **required**)

List of package names to update.

**Example:**
```python
update_specific_packages(
    package_names=["express", "axios", "lodash"]
)
```

#### Other Parameters

Same as `update_packages` (see Tool 2).

### Return Value

**Success:**
```
Target Node.js LTS: 22.11.0
Detected Node.js: 22.11.0
Updating 3 package(s)...

[UPDATE] express: ^4.17.1 -> ^4.19.2
[UPDATE] axios: ^0.21.1 -> ^1.6.7
[UPDATE] lodash: ^4.17.20 -> ^4.17.21

Successfully updated 3 package(s) in /tmp/project/package.json
```

**Partial Success:**
```
Updating 3 package(s)...

[UPDATE] express: ^4.17.1 -> ^4.19.2
[SKIP] missing-package: no compatible version found
[UPDATE] lodash: ^4.17.20 -> ^4.17.21

Successfully updated 2 package(s)
```

**Error:**
```
None of the specified packages found in package.json
```

### Basic Examples

#### Example 1: Update Specific Packages

```python
from src.tools.package_updates_tools import PackageUpdatesTools

tools = PackageUpdatesTools(node_lts_version="22.11.0")

result = tools.update_specific_packages(
    package_names=["express", "axios"],
    package_json_path="/tmp/project/package.json",
    apply_updates=True
)

print(result)
```

#### Example 2: Update Security-Critical Packages

```python
# Update only packages with known vulnerabilities
vulnerable_packages = ["lodash", "minimist", "axios"]

result = tools.update_specific_packages(
    package_names=vulnerable_packages,
    package_json_path="/tmp/project/package.json",
    lock_major=False,  # Allow major updates for security
    apply_updates=True
)
```

#### Example 3: Update Framework Packages

```python
# Update all React-related packages
react_packages = [
    "react",
    "react-dom",
    "react-router",
    "react-router-dom"
]

result = tools.update_specific_packages(
    package_names=react_packages,
    package_json_path="/tmp/project/package.json"
)
```

### Advanced Examples

#### Update Based on Analysis

```python
# First, analyze all packages
analysis = tools.analyze_packages(package_json_path="/tmp/project/package.json")

# Extract packages with high-priority updates
import re
update_lines = [line for line in analysis.split('\n') if '[UPDATE]' in line]

# Parse package names
packages_to_update = []
for line in update_lines:
    match = re.search(r'\[UPDATE\] (\S+):', line)
    if match:
        packages_to_update.append(match.group(1))

# Update only those packages
if packages_to_update:
    result = tools.update_specific_packages(
        package_names=packages_to_update,
        package_json_path="/tmp/project/package.json",
        apply_updates=True
    )
```

#### Progressive Update (Batch by Type)

```python
# Update in phases

# Phase 1: Utilities
utility_packages = ["lodash", "date-fns", "ramda"]
result = tools.update_specific_packages(
    package_names=utility_packages,
    package_json_path="/tmp/project/package.json",
    apply_updates=True
)
# Test...

# Phase 2: HTTP libraries
http_packages = ["axios", "node-fetch"]
result = tools.update_specific_packages(
    package_names=http_packages,
    package_json_path="/tmp/project/package.json",
    apply_updates=True
)
# Test...

# Phase 3: Frameworks
framework_packages = ["express", "koa"]
result = tools.update_specific_packages(
    package_names=framework_packages,
    package_json_path="/tmp/project/package.json",
    apply_updates=True
)
```

### Use Cases

1. **Security Fixes**: Update only vulnerable packages
2. **Framework Migration**: Update related packages together
3. **Incremental Updates**: Update packages one at a time
4. **Dependency Conflicts**: Update specific package to resolve conflicts
5. **Testing**: Update and test packages in small batches

### Comparison with update_packages

| Feature | update_packages | update_specific_packages |
|---------|----------------|--------------------------|
| Updates all packages | ✅ | ❌ |
| Updates specific packages | ❌ | ✅ |
| Selective updates | ❌ | ✅ |
| Faster (fewer packages) | ❌ | ✅ |
| Comprehensive | ✅ | ❌ |

**When to use update_specific_packages:**
- Fixing specific vulnerabilities
- Testing updates incrementally
- Avoiding changes to working packages
- Updating related packages together

**When to use update_packages:**
- Regular maintenance
- Starting fresh project
- Comprehensive updates
- Monthly dependency updates

---

## Tool 5: get_package_info

### Description

Get detailed information about a specific package including versions, compatibility, and current usage.

### Function Signature

```python
def get_package_info(
    package_name: str,
    package_json_path: str = "package.json",
    npm_lookup: bool = True
) -> str
```

### Parameters

#### `package_name` (str, **required**)

Name of the package to get information about.

#### `package_json_path` (str, default: "package.json")

Path to package.json file.

#### `npm_lookup` (bool, default: True)

Query npm registry for package information.

### Return Value

**Success (package in package.json, npm_lookup=True):**
```
Current version in dependencies: ^4.17.1

Latest version: 4.19.2
Total versions available: 287
Node.js requirement (latest): >=0.10.0

Recent versions: 4.19.2, 4.19.1, 4.19.0, 4.18.3, 4.18.2
```

**Success (package not in package.json):**
```
Package 'some-package' not found in /tmp/project/package.json

Latest version: 2.1.0
Total versions available: 45
Node.js requirement (latest): >=14.0.0

Recent versions: 2.1.0, 2.0.5, 2.0.4, 2.0.3, 2.0.2
```

**Error:**
```
No information found for 'unknown-package'
```

### Basic Examples

#### Example 1: Check Package Info

```python
from src.tools.package_updates_tools import PackageUpdatesTools

tools = PackageUpdatesTools(node_lts_version="22.11.0")

result = tools.get_package_info(
    package_name="express",
    package_json_path="/tmp/project/package.json"
)

print(result)
```

#### Example 2: Research Before Adding

```python
# Check package before adding
info = tools.get_package_info(
    package_name="some-new-package",
    npm_lookup=True
)

print(info)

# If compatible, add it
if "Latest version" in info:
    result = tools.add_package(
        package_name="some-new-package",
        package_json_path="/tmp/project/package.json"
    )
```

#### Example 3: Compare Current vs Latest

```python
info = tools.get_package_info(
    package_name="lodash",
    package_json_path="/tmp/project/package.json"
)

# Parse current and latest
import re
current_match = re.search(r'Current version in \w+: (.+)', info)
latest_match = re.search(r'Latest version: (.+)', info)

if current_match and latest_match:
    current = current_match.group(1)
    latest = latest_match.group(1)
    print(f"Current: {current}")
    print(f"Latest: {latest}")
    
    if current != f"^{latest}":
        print("Update available!")
```

### Advanced Examples

#### Batch Package Research

```python
# Research multiple packages
packages_to_research = [
    "express",
    "axios",
    "lodash",
    "date-fns",
    "react"
]

for pkg in packages_to_research:
    print(f"\n{'='*60}")
    print(f"Package: {pkg}")
    print('='*60)
    
    info = tools.get_package_info(
        package_name=pkg,
        package_json_path="/tmp/project/package.json"
    )
    print(info)
```

#### Generate Dependency Report

```python
import json

# Load package.json
with open("/tmp/project/package.json", 'r') as f:
    pkg = json.load(f)

# Get all dependencies
all_deps = list(pkg.get("dependencies", {}).keys())

# Generate report
report = []
for dep in all_deps:
    info = tools.get_package_info(
        package_name=dep,
        package_json_path="/tmp/project/package.json"
    )
    report.append({
        "package": dep,
        "info": info
    })

# Save report
with open("dependency_report.json", 'w') as f:
    json.dump(report, f, indent=2)
```

### Use Cases

1. **Package Research**: Learn about package before adding
2. **Version Checking**: See current vs latest version
3. **Compatibility Check**: Verify Node.js compatibility
4. **Documentation**: Generate dependency documentation
5. **Audit**: Review all package versions

---

## Tool 6: audit_packages

### Description

Audit packages for security vulnerabilities using npm audit. Essential for security maintenance.

### Function Signature

```python
def audit_packages(
    package_json_path: str = "package.json",
    min_severity: str | None = None
) -> str
```

### Parameters

#### `package_json_path` (str, default: "package.json")

Path to package.json file.

#### `min_severity` (str | None, default: None)

Minimum severity level to report.

**Valid Values:**
- `None` - Report all severities
- `"low"` - Report low and above
- `"moderate"` - Report moderate and above
- `"high"` - Report high and critical only
- `"critical"` - Report critical only

**Example:**
```python
# All vulnerabilities
audit_packages(min_severity=None)

# Only high and critical
audit_packages(min_severity="high")
```

### Return Value

**Success (No Vulnerabilities):**
```
Audit completed with exit code: 0

No vulnerabilities found!
```

**Success (Vulnerabilities Found):**
```
Audit completed with exit code: 1
Vulnerabilities detected. Details saved to audit.json

Vulnerability Summary:
  moderate: 2
  high: 3
  critical: 1
```

**Error:**
```
Error: package.json not found at /path/to/package.json
```

### Basic Examples

#### Example 1: Full Audit

```python
from src.tools.package_updates_tools import PackageUpdatesTools

tools = PackageUpdatesTools(node_lts_version="22.11.0")

result = tools.audit_packages(
    package_json_path="/tmp/project/package.json"
)

print(result)
```

#### Example 2: High Severity Only

```python
result = tools.audit_packages(
    package_json_path="/tmp/project/package.json",
    min_severity="high"
)

print(result)
```

#### Example 3: Critical Only

```python
result = tools.audit_packages(
    package_json_path="/tmp/project/package.json",
    min_severity="critical"
)
```

### Advanced Examples

#### Automated Security Check

```python
# Run audit
result = tools.audit_packages(
    package_json_path="/tmp/project/package.json",
    min_severity="high"
)

# Parse results
has_vulnerabilities = "Vulnerabilities detected" in result

if has_vulnerabilities:
    print("⚠️  Security vulnerabilities found!")
    print(result)
    
    # Load audit details
    import json
    with open("audit.json", 'r') as f:
        audit_data = json.load(f)
    
    # Extract vulnerable packages
    # ... process audit_data
    
    print("\nAttempting to fix...")
    # Try to update vulnerable packages
    update_result = tools.update_packages(
        package_json_path="/tmp/project/package.json",
        lock_major=False,  # Allow major updates for security
        apply_updates=True
    )
    print(update_result)
else:
    print("✅ No security vulnerabilities")
```

#### CI/CD Security Gate

```python
import sys

def security_check(package_json_path: str, fail_on: str = "high"):
    """Run security audit and fail if vulnerabilities found."""
    tools = PackageUpdatesTools(node_lts_version="22.11.0")
    
    result = tools.audit_packages(
        package_json_path=package_json_path,
        min_severity=fail_on
    )
    
    print(result)
    
    if "Vulnerabilities detected" in result:
        print(f"\n❌ Security check failed: {fail_on}+ vulnerabilities found")
        sys.exit(1)
    else:
        print("\n✅ Security check passed")
        sys.exit(0)

# Use in CI pipeline
security_check("/tmp/project/package.json", fail_on="high")
```

#### Parse Audit Results

```python
import json

# Run audit
result = tools.audit_packages(package_json_path="/tmp/project/package.json")

if "Vulnerabilities detected" in result:
    # Load audit.json
    with open("audit.json", 'r') as f:
        audit = json.load(f)
    
    # Parse vulnerabilities
    if "vulnerabilities" in audit.get("metadata", {}):
        vulns = audit["metadata"]["vulnerabilities"]
        
        print("\nVulnerability Breakdown:")
        for severity in ["low", "moderate", "high", "critical"]:
            count = vulns.get(severity, 0)
            if count > 0:
                print(f"  {severity.upper()}: {count}")
```

### Use Cases

1. **Security Maintenance**: Regular security scans
2. **CI/CD Gates**: Prevent deployment with vulnerabilities
3. **Compliance**: Security compliance requirements
4. **Risk Assessment**: Understand security posture
5. **Remediation**: Identify packages to update

### Best Practices

- **Run regularly**: Weekly or before each deployment
- **Set severity threshold**: `min_severity="high"` for production
- **Automate fixes**: Update packages after audit
- **Track over time**: Monitor security trend
- **Document exceptions**: Known issues in backlog

### Tips

```python
# Generate security report
audit = tools.audit_packages(package_json_path="/tmp/project/package.json")
with open("security_report.txt", 'w') as f:
    f.write(audit)
```

---

## Tool 7: remove_package

### Description

Remove a package from package.json and optionally uninstall it.

### Function Signature

```python
def remove_package(
    package_name: str,
    package_json_path: str = "package.json",
    uninstall: bool = False,
    manager: str = "npm"
) -> str
```

### Parameters

#### `package_name` (str, **required**)

Name of the package to remove.

#### `package_json_path` (str, default: "package.json")

Path to package.json file.

#### `uninstall` (bool, default: False)

Run package manager uninstall command.

**When True:**
- Removes from package.json
- Runs `npm uninstall package-name`
- Removes from node_modules
- Updates lock file

**When False:**
- Only removes from package.json
- Leaves node_modules unchanged

#### `manager` (str, default: "npm")

Package manager to use.

**Valid Values:** `"npm"`, `"yarn"`, `"pnpm"`

### Return Value

**Success:**
```
Successfully removed 'moment' from dependencies
```

**Success (with uninstall):**
```
Successfully removed 'moment' from dependencies
Package uninstalled using npm
```

**Error:**
```
Error: Package 'moment' not found in package.json
```

### Basic Examples

#### Example 1: Remove Package

```python
from src.tools.package_updates_tools import PackageUpdatesTools

tools = PackageUpdatesTools(node_lts_version="22.11.0")

result = tools.remove_package(
    package_name="moment",
    package_json_path="/tmp/project/package.json"
)

print(result)
# Output: Successfully removed 'moment' from dependencies
```

#### Example 2: Remove and Uninstall

```python
result = tools.remove_package(
    package_name="moment",
    package_json_path="/tmp/project/package.json",
    uninstall=True  # Also run npm uninstall
)

print(result)
# Output: Successfully removed 'moment' from dependencies
#         Package uninstalled using npm
```

#### Example 3: Remove with Yarn

```python
result = tools.remove_package(
    package_name="old-package",
    package_json_path="/tmp/project/package.json",
    uninstall=True,
    manager="yarn"
)
```

### Advanced Examples

#### Batch Remove Packages

```python
# Remove multiple deprecated packages
deprecated_packages = [
    "moment",        # Use date-fns instead
    "request",       # Use axios instead
    "mkdirp"         # Built into Node.js now
]

for pkg in deprecated_packages:
    result = tools.remove_package(
        package_name=pkg,
        package_json_path="/tmp/project/package.json",
        uninstall=True
    )
    print(result)
```

#### Remove and Replace

```python
# Remove old package
result = tools.remove_package(
    package_name="moment",
    package_json_path="/tmp/project/package.json",
    uninstall=True
)
print(result)

# Add modern alternative
result = tools.add_package(
    package_name="date-fns",
    package_json_path="/tmp/project/package.json",
    install=True
)
print(result)
```

### Use Cases

1. **Dependency Cleanup**: Remove unused packages
2. **Migration**: Replace deprecated packages
3. **Size Optimization**: Remove bloated dependencies
4. **Security**: Remove vulnerable packages
5. **Simplification**: Reduce dependency count

---

## Advanced Usage Patterns

### Pattern 1: Complete Update Workflow

```python
from src.tools.package_updates_tools import PackageUpdatesTools

def complete_update_workflow(package_json_path: str):
    """Complete dependency update workflow."""
    tools = PackageUpdatesTools(node_lts_version="22.11.0")
    
    print("Step 1: Analyze current state")
    analysis = tools.analyze_packages(package_json_path=package_json_path)
    print(analysis)
    
    print("\nStep 2: Audit security")
    audit = tools.audit_packages(package_json_path=package_json_path)
    print(audit)
    
    print("\nStep 3: Dry run update")
    dry_run = tools.update_packages(
        package_json_path=package_json_path,
        dry_run=True
    )
    print(dry_run)
    
    # Review and confirm...
    
    print("\nStep 4: Apply updates")
    update = tools.update_packages(
        package_json_path=package_json_path,
        dry_run=False,
        apply_updates=True
    )
    print(update)
    
    print("\nStep 5: Verify security")
    final_audit = tools.audit_packages(package_json_path=package_json_path)
    print(final_audit)

complete_update_workflow("/tmp/project/package.json")
```

### Pattern 2: Smart Dependency Migration

```python
def migrate_dependencies(package_json_path: str, migrations: dict):
    """Replace old packages with modern alternatives.
    
    Args:
        package_json_path: Path to package.json
        migrations: Dict of {old_package: new_package}
    """
    tools = PackageUpdatesTools(node_lts_version="22.11.0")
    
    for old_pkg, new_pkg in migrations.items():
        print(f"\nMigrating: {old_pkg} → {new_pkg}")
        
        # Check if old package exists
        info = tools.get_package_info(
            package_name=old_pkg,
            package_json_path=package_json_path
        )
        
        if "not found" in info:
            print(f"  {old_pkg} not installed, skipping")
            continue
        
        # Remove old package
        remove_result = tools.remove_package(
            package_name=old_pkg,
            package_json_path=package_json_path,
            uninstall=True
        )
        print(f"  Removed: {remove_result}")
        
        # Add new package
        add_result = tools.add_package(
            package_name=new_pkg,
            package_json_path=package_json_path,
            install=True
        )
        print(f"  Added: {add_result}")

# Usage
migrations = {
    "moment": "date-fns",
    "request": "axios",
    "mkdirp": "fs-extra"
}

migrate_dependencies("/tmp/project/package.json", migrations)
```

### Pattern 3: Selective Update Strategy

```python
def selective_update(package_json_path: str):
    """Update packages selectively based on priority."""
    tools = PackageUpdatesTools(node_lts_version="22.11.0")
    
    # Priority 1: Security updates
    print("=== PRIORITY 1: Security Updates ===")
    audit = tools.audit_packages(
        package_json_path=package_json_path,
        min_severity="high"
    )
    
    if "Vulnerabilities detected" in audit:
        # Extract vulnerable packages from audit.json
        # Update those packages
        pass
    
    # Priority 2: Critical dependencies
    print("\n=== PRIORITY 2: Critical Dependencies ===")
    critical_packages = ["express", "react", "vue"]
    tools.update_specific_packages(
        package_names=critical_packages,
        package_json_path=package_json_path,
        apply_updates=True
    )
    
    # Priority 3: All other packages
    print("\n=== PRIORITY 3: Other Packages ===")
    tools.update_packages(
        package_json_path=package_json_path,
        lock_major=True,
        apply_updates=True
    )
```

---

## Real-World Use Cases

### Use Case 1: Monthly Maintenance

```python
#!/usr/bin/env python3
"""Monthly dependency maintenance script."""

from src.tools.package_updates_tools import PackageUpdatesTools
from datetime import datetime
import sys

def monthly_maintenance(project_path: str):
    tools = PackageUpdatesTools(node_lts_version="22.11.0")
    package_json = f"{project_path}/package.json"
    
    print(f"=== Monthly Maintenance: {datetime.now().strftime('%Y-%m')} ===\n")
    
    # 1. Security audit
    print("1. Security Audit")
    audit = tools.audit_packages(package_json_path=package_json)
    print(audit)
    
    if "critical" in audit.lower():
        print("❌ Critical vulnerabilities found! Fix immediately.")
        sys.exit(1)
    
    # 2. Analyze updates
    print("\n2. Available Updates")
    analysis = tools.analyze_packages(
        package_json_path=package_json,
        lock_major=True
    )
    print(analysis)
    
    # 3. Update packages
    print("\n3. Applying Updates")
    update = tools.update_packages(
        package_json_path=package_json,
        lock_major=True,
        dry_run=False,
        apply_updates=True
    )
    print(update)
    
    # 4. Final audit
    print("\n4. Post-Update Audit")
    final_audit = tools.audit_packages(package_json_path=package_json)
    print(final_audit)
    
    print("\n✅ Monthly maintenance complete!")

if __name__ == "__main__":
    monthly_maintenance("/path/to/project")
```

### Use Case 2: CI/CD Integration

```python
# .github/workflows/dependency-check.yml
"""
name: Dependency Check
on: [push, pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - name: Run dependency check
        run: python scripts/dependency_check.py
"""

# scripts/dependency_check.py
from src.tools.package_updates_tools import PackageUpdatesTools
import sys

def ci_dependency_check():
    tools = PackageUpdatesTools(node_lts_version="22.11.0")
    
    # Check for critical vulnerabilities
    audit = tools.audit_packages(
        package_json_path="package.json",
        min_severity="high"
    )
    
    if "Vulnerabilities detected" in audit:
        print("❌ Security vulnerabilities found!")
        print(audit)
        sys.exit(1)
    
    # Check for outdated packages
    analysis = tools.analyze_packages(package_json_path="package.json")
    
    update_count = analysis.count('[UPDATE]')
    if update_count > 10:
        print(f"⚠️  {update_count} packages need updates")
        # Create GitHub issue or comment
    
    print("✅ Dependency check passed")
    sys.exit(0)

if __name__ == "__main__":
    ci_dependency_check()
```

### Use Case 3: Monorepo Management

```python
from pathlib import Path

def update_monorepo(root_path: str):
    """Update all packages in a monorepo."""
    tools = PackageUpdatesTools(node_lts_version="22.11.0")
    
    # Find all package.json files
    root = Path(root_path)
    package_files = list(root.glob("**/package.json"))
    
    # Exclude node_modules
    package_files = [
        p for p in package_files
        if "node_modules" not in str(p)
    ]
    
    print(f"Found {len(package_files)} packages\n")
    
    results = {}
    
    for pkg_file in package_files:
        pkg_name = pkg_file.parent.name
        print(f"=== Updating: {pkg_name} ===")
        
        # Update
        result = tools.update_packages(
            package_json_path=str(pkg_file),
            lock_major=True,
            dry_run=False,
            apply_updates=False  # Install at root level
        )
        
        results[pkg_name] = result
        print(result)
        print()
    
    # Install all at root
    print("Installing dependencies at root...")
    # npm install (at root)
    
    return results

update_monorepo("/path/to/monorepo")
```

---

## Best Practices

### 1. Always Preview Changes

```python
# ✅ Good: Preview first
result = tools.update_packages(dry_run=True)
# Review...
result = tools.update_packages(dry_run=False)

# ❌ Bad: Update blindly
result = tools.update_packages(dry_run=False, apply_updates=True)
```

### 2. Test After Updates

```python
# Update packages
tools.update_packages(
    package_json_path="/tmp/project/package.json",
    dry_run=False,
    apply_updates=True
)

# Run tests
import subprocess
subprocess.run(["npm", "test"], check=True)
```

### 3. Use lock_major in Production

```python
# ✅ Production: Lock major versions
tools.update_packages(lock_major=True)

# ⚠️  Development: Can allow major updates
tools.update_packages(lock_major=False)
```

### 4. Regular Security Audits

```python
# Run weekly
tools.audit_packages(
    package_json_path="/tmp/project/package.json",
    min_severity="moderate"
)
```

### 5. Document Changes

```python
# Before update
analysis = tools.analyze_packages(package_json_path="/tmp/project/package.json")

# Save for documentation
with open("update_log.txt", 'w') as f:
    f.write(f"Update Date: {datetime.now()}\n")
    f.write(analysis)

# Apply update
update = tools.update_packages(...)
```

---

## Troubleshooting

### Common Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| `package.json not found` | Wrong path | Use absolute path |
| `npm ERR! code ENOENT` | npm not installed | Install Node.js and npm |
| `registry fetch failed: timeout` | Network issue | Increase timeout or use `npm_lookup=False` |
| `no compatible version found` | Node.js version mismatch | Update `node_lts_version` or use older version |
| `Package already exists` | Duplicate add | Use `update_specific_packages` instead |

---

**Last Updated**: January 2026  
**Version**: 2.1.0
