# Package Management Guide

Complete guide to npm package management features in CodeBaseOpsAI-v2-1, including NPM registry integration, semantic versioning, Node.js compatibility checking, vulnerability scanning, and advanced usage patterns.

---

## Table of Contents

1. [Overview](#overview)
2. [NPM Registry Integration](#npm-registry-integration)
3. [Semantic Versioning Explained](#semantic-versioning-explained)
4. [Node.js Compatibility Checking](#nodejs-compatibility-checking)
5. [Vulnerability Scanning with OSV API](#vulnerability-scanning-with-osv-api)
6. [npm_lookup Bypass Mechanism](#npm_lookup-bypass-mechanism)
7. [Multi-Package Manager Support](#multi-package-manager-support)
8. [Version Selection Algorithm](#version-selection-algorithm)
9. [Package Management Tools](#package-management-tools)
10. [Real-World Examples](#real-world-examples)
11. [Best Practices](#best-practices)
12. [Troubleshooting](#troubleshooting)

---

## Overview

CodeBaseOpsAI-v2-1 provides intelligent npm package management that goes beyond simple version updates. The system:

- **Analyzes** package dependencies for available updates
- **Validates** Node.js compatibility for each version
- **Scans** for security vulnerabilities using OSV API
- **Selects** optimal versions based on multiple criteria
- **Supports** npm, yarn, and pnpm package managers
- **Handles** both public and private packages

### Key Features

| Feature | Description | Benefit |
|---------|-------------|---------|
| **Intelligent Version Selection** | Automatically chooses best version | Saves manual research time |
| **Node.js Compatibility** | Checks engines.node for each version | Prevents runtime errors |
| **Security Scanning** | OSV API integration | Avoids vulnerable packages |
| **Major Version Locking** | Optional major version constraints | Prevents breaking changes |
| **Private Package Support** | npm_lookup bypass | Works with private registries |
| **Multi-Manager** | npm, yarn, pnpm support | Flexible workflow integration |

### Architecture Overview

```
┌──────────────────────────────────────────────────────────┐
│                  PackageUpdatesTools                     │
│                                                          │
│  ┌────────────┐  ┌────────────┐  ┌─────────────┐       │
│  │  analyze   │  │   update   │  │    audit    │       │
│  │  packages  │  │  packages  │  │   packages  │       │
│  └────────────┘  └────────────┘  └─────────────┘       │
│                                                          │
│  ┌────────────┐  ┌────────────┐  ┌─────────────┐       │
│  │    add     │  │   remove   │  │   get info  │       │
│  │  package   │  │  package   │  │             │       │
│  └────────────┘  └────────────┘  └─────────────┘       │
└──────────────────────────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
┌────────────────┐ ┌──────────┐ ┌──────────────┐
│ NPM Registry   │ │ OSV API  │ │ Node.js      │
│ (Packuments)   │ │ (Vulns)  │ │ Detection    │
└────────────────┘ └──────────┘ └──────────────┘
```

---

## NPM Registry Integration

### What is the NPM Registry?

The NPM registry (registry.npmjs.org) is the central repository for all public npm packages. It provides:

- **Package metadata** (versions, dependencies, engines)
- **Version history** (all published versions)
- **Distribution information** (download URLs)
- **Maintainer details** (authors, contributors)

### Packument Structure

A "packument" (package document) contains all metadata for a package:

```json
{
  "name": "express",
  "description": "Fast, unopinionated, minimalist web framework",
  "dist-tags": {
    "latest": "4.18.2",
    "next": "5.0.0-beta.1"
  },
  "versions": {
    "4.18.2": {
      "name": "express",
      "version": "4.18.2",
      "description": "Fast, unopinionated, minimalist web framework",
      "main": "index.js",
      "engines": {
        "node": ">= 0.10.0"
      },
      "dependencies": {
        "accepts": "~1.3.8",
        "array-flatten": "1.1.1",
        "body-parser": "1.20.1",
        "content-disposition": "0.5.4",
        ...
      },
      "devDependencies": {...},
      "scripts": {...},
      "dist": {
        "tarball": "https://registry.npmjs.org/express/-/express-4.18.2.tgz",
        "shasum": "3fabe4e3f4e0f8e7e3f4e3f4e3f4e3f4e3f4e3f4"
      }
    },
    "4.18.1": {...},
    "4.18.0": {...},
    ...
  }
}
```

### Abbreviated Format

CodeBaseOpsAI uses the abbreviated packument format for efficiency:

```python
ABBREV_ACCEPT = "application/vnd.npm.install-v1+json"

def fetch_packument(name: str, registry: str = NPM_REGISTRY) -> Dict:
    url = f"{registry}/{name}"
    headers = {"Accept": ABBREV_ACCEPT}
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()
```

**Benefits of abbreviated format**:
- ~70% smaller response size
- Faster downloads
- Less memory usage
- Still contains all necessary information

**Example size comparison**:

| Package | Full Format | Abbreviated | Savings |
|---------|------------|-------------|---------|
| express | 450 KB | 135 KB | 70% |
| lodash | 380 KB | 110 KB | 71% |
| react | 520 KB | 150 KB | 71% |

### Fetching Package Information

```python
# Fetch packument
packument = PackageUpdatesUtils.fetch_packument("express")

# Extract versions
versions = PackageUpdatesUtils.list_versions_from_packument(packument)
# Returns: ['4.0.0', '4.1.0', ..., '4.18.2', '5.0.0-beta.1']

# Get engines.node for specific version
node_range = PackageUpdatesUtils.engines_node_for_version(packument, "4.18.2")
# Returns: ">= 0.10.0"
```

### Registry Configuration

Default registry: `https://registry.npmjs.org`

**Custom registry support**:

```python
# Initialize with custom registry
tools = PackageUpdatesTools(
    node_lts_version="22.11.0",
    npm_registry="https://registry.company.com"
)
```

**Environment variable**:

```bash
export NPM_REGISTRY="https://registry.company.com"
```

### Error Handling

```python
try:
    packument = PackageUpdatesUtils.fetch_packument("express")
except requests.HTTPError as e:
    if e.response.status_code == 404:
        print("Package not found")
    elif e.response.status_code == 503:
        print("Registry unavailable")
    else:
        print(f"HTTP error: {e}")
except requests.Timeout:
    print("Request timed out after 30 seconds")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## Semantic Versioning Explained

### What is Semantic Versioning?

Semantic Versioning (SemVer) is a versioning scheme using three numbers: `MAJOR.MINOR.PATCH`

**Format**: `X.Y.Z` where:
- **X (Major)**: Incompatible API changes
- **Y (Minor)**: Backwards-compatible new features
- **Z (Patch)**: Backwards-compatible bug fixes

**Examples**:
- `1.0.0` → Initial release
- `1.1.0` → Added new feature
- `1.1.1` → Fixed bug
- `2.0.0` → Breaking change

### Version Ranges

NPM uses version ranges to specify acceptable versions:

#### Caret (`^`) - Compatible Changes

**Pattern**: `^X.Y.Z`

**Meaning**: Allow changes that don't modify the leftmost non-zero digit.

**Examples**:

| Range | Matches | Explanation |
|-------|---------|-------------|
| `^1.2.3` | `>=1.2.3 <2.0.0` | Allow minor and patch updates |
| `^0.2.3` | `>=0.2.3 <0.3.0` | Allow patch updates only (0.x is special) |
| `^0.0.3` | `>=0.0.3 <0.0.4` | Exact match (0.0.x is special) |

**Use case**: Most common, allows new features without breaking changes.

#### Tilde (`~`) - Patch Changes

**Pattern**: `~X.Y.Z`

**Meaning**: Allow patch-level changes only.

**Examples**:

| Range | Matches | Explanation |
|-------|---------|-------------|
| `~1.2.3` | `>=1.2.3 <1.3.0` | Allow patch updates only |
| `~1.2` | `>=1.2.0 <1.3.0` | Allow patch updates only |
| `~1` | `>=1.0.0 <2.0.0` | Allow minor and patch updates |

**Use case**: When you want to be more conservative about updates.

#### Exact Version

**Pattern**: `X.Y.Z` (no prefix)

**Meaning**: Exact version only.

**Example**: `1.2.3` matches only `1.2.3`

**Use case**: Maximum stability, no updates.

#### Other Ranges

| Range | Matches | Example |
|-------|---------|---------|
| `*` | Any version | Latest always |
| `1.x` | `>=1.0.0 <2.0.0` | Any 1.x version |
| `>=1.2.3` | `1.2.3` and above | Minimum version |
| `1.2.3 - 2.3.4` | Between versions | Specific range |
| `<1.2.3 \|\| >2.3.4` | Outside range | Exclusion range |

### Using semantic-version Library

CodeBaseOpsAI uses the `semantic-version` Python library:

```python
from semantic_version import Version, Spec

# Parse versions
v1 = Version("1.2.3")      # v1.major=1, v1.minor=2, v1.patch=3
v2 = Version.coerce("1.2")  # Handles partial versions

# Create specs (ranges)
spec = Spec("^1.2.3")  # >=1.2.3 <2.0.0

# Check if version matches spec
v1 in spec  # True
Version("2.0.0") in spec  # False

# Select from list
versions = [Version("1.1.0"), Version("1.2.5"), Version("1.3.0")]
best = spec.select(versions)  # Returns Version("1.3.0")
```

### Version Sorting

```python
def list_versions_from_packument(packument: Dict) -> List[str]:
    versions = packument.get("versions", {})
    # Sort using semantic versioning
    return sorted(versions.keys(), key=lambda v: Version.coerce(v))
```

**Result**: `['0.1.0', '0.2.0', '1.0.0', '1.0.1', '1.1.0', '2.0.0']`

Without semantic sorting: `['0.1.0', '0.2.0', '1.0.0', '1.0.1', '1.1.0', '2.0.0']` (correct)
With string sorting: `['0.1.0', '0.2.0', '1.0.0', '1.0.1', '1.1.0', '2.0.0']` (incorrect: '10.0.0' comes before '2.0.0')

### Pre-release Versions

Pre-release versions have additional identifiers:

- `1.0.0-alpha` - Alpha release
- `1.0.0-beta.1` - Beta release
- `1.0.0-rc.1` - Release candidate
- `1.0.0-next.20210101` - Next/canary release

**Precedence**: `1.0.0-alpha < 1.0.0-beta < 1.0.0-rc < 1.0.0`

**Handling in CodeBaseOpsAI**:

```python
v = Version.coerce("5.0.0-beta.1")
# v.major = 5, v.minor = 0, v.patch = 0, v.prerelease = ('beta', '1')

if v.prerelease:
    # This is a pre-release version
    # May want to skip in production environments
```

---

## Node.js Compatibility Checking

### Why Node.js Compatibility Matters

npm packages often specify required Node.js versions via the `engines.node` field:

```json
{
  "name": "my-package",
  "engines": {
    "node": ">=14.0.0"
  }
}
```

**Installing incompatible versions causes**:
- Runtime errors
- Missing APIs/features
- Build failures
- Security issues

### Node.js Version Detection

CodeBaseOpsAI detects Node.js version from multiple sources with priority order:

#### 1. .nvmrc File (Highest Priority)

```bash
# .nvmrc
22.11.0
```

or

```bash
# .nvmrc
v22.11.0
```

**Detection code**:

```python
if Path(".nvmrc").exists():
    raw = Path(".nvmrc").read_text(encoding="utf-8").strip()
    node_version = raw.lstrip("v")  # Remove 'v' prefix if present
    return node_version
```

#### 2. node -v Command

```bash
$ node -v
v22.11.0
```

**Detection code**:

```python
try:
    out = subprocess.run(
        ["node", "-v"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    ).stdout.decode().strip()
    return out.lstrip("v")
except:
    pass  # Fall through to next method
```

#### 3. package.json engines.node

```json
{
  "engines": {
    "node": ">=18.0.0"
  }
}
```

**Detection code**:

```python
node_range = pkg.get("engines", {}).get("node")
if node_range:
    # Select minimum version that satisfies range
    spec = Spec(node_range)
    min_version = spec.select([
        Version("10.0.0"), Version("12.0.0"), Version("14.0.0"),
        Version("16.0.0"), Version("18.0.0"), Version("20.0.0"),
        Version("22.0.0")
    ])
    if min_version:
        return str(min_version)
```

#### 4. Hardcoded Default (18.0.0)

If all else fails, use a safe default:

```python
return "18.0.0"
```

### Compatibility Checking Algorithm

```python
def is_compatible(node_ver: str, node_range: Optional[str]) -> bool:
    """Check if Node.js version satisfies package requirement."""
    
    # Missing engines.node → assume compatible
    if not node_range:
        return True
    
    try:
        node_spec = Spec(node_range)
        return Version.coerce(node_ver) in node_spec
    except Exception:
        # Unparseable range → be conservative
        return False
```

**Examples**:

| Node Version | engines.node | Compatible? |
|--------------|--------------|-------------|
| 22.11.0 | `>= 0.10.0` | ✅ Yes |
| 22.11.0 | `>= 14.0.0` | ✅ Yes |
| 22.11.0 | `>= 14.0.0 < 20.0.0` | ❌ No (too new) |
| 22.11.0 | `^18.0.0` | ❌ No (major mismatch) |
| 22.11.0 | (missing) | ✅ Yes (assumed) |
| 22.11.0 | `invalid range` | ❌ No (conservative) |

### Integration in Version Selection

```python
def choose_best_version(name, current_range, node_ver, lock_major, packument):
    versions = list_versions_from_packument(packument)
    
    for v in reversed(versions):  # Newest first
        # ... other checks ...
        
        # Check Node.js compatibility
        node_range = engines_node_for_version(packument, v)
        if not is_compatible(node_ver, node_range):
            continue  # Skip incompatible version
        
        # ... vulnerability check ...
        
        return v  # Compatible version found
```

### LTS Version Configuration

Set the target Node.js LTS version:

```python
# In main.py
node_lts_version = '22.11.0'  # Node.js 22 LTS

# Initialize agent
agent = Agent(node_lts_version=node_lts_version)
```

**Why LTS versions?**
- Long-term support (3 years)
- Stable and tested
- Security updates
- Widely used in production

**Current LTS versions** (as of 2026):
- **22.x (Current LTS)** - Iron (2024-2027)
- **20.x (Maintenance)** - Hydrogen (2022-2025)
- **18.x (Maintenance)** - Hydrogen (2021-2025)

---

## Vulnerability Scanning with OSV API

### What is OSV?

Open Source Vulnerabilities (OSV) is a distributed vulnerability database:
- **Coverage**: npm, PyPI, Go, Maven, RubyGems, etc.
- **Source**: Multiple databases (GitHub Advisory, NVD, etc.)
- **Format**: Standardized JSON schema
- **Access**: Free public API

**Website**: https://osv.dev/

### API Integration

**Endpoint**: `https://api.osv.dev/v1/query`

**Request**:

```python
payload = {
    "package": {
        "name": "lodash",
        "ecosystem": "npm"
    },
    "version": "4.17.19"
}

response = requests.post(
    "https://api.osv.dev/v1/query",
    json=payload,
    timeout=30
)
```

**Response (vulnerability found)**:

```json
{
  "vulns": [
    {
      "id": "GHSA-p6mc-m468-83gw",
      "summary": "Prototype Pollution in lodash",
      "details": "Versions of lodash prior to 4.17.20 are vulnerable to Prototype Pollution...",
      "aliases": ["CVE-2020-8203"],
      "modified": "2023-09-12T17:20:23Z",
      "published": "2020-07-15T19:15:00Z",
      "database_specific": {
        "severity": "HIGH",
        "cwe_ids": ["CWE-1321"]
      },
      "affected": [
        {
          "package": {
            "name": "lodash",
            "ecosystem": "npm"
          },
          "ranges": [
            {
              "type": "SEMVER",
              "events": [
                {"introduced": "0"},
                {"fixed": "4.17.20"}
              ]
            }
          ],
          "versions": ["4.17.19", "4.17.18", ...]
        }
      ]
    }
  ]
}
```

**Response (no vulnerabilities)**:

```json
{
  "vulns": []
}
```

### Implementation in CodeBaseOpsAI

```python
OSV_API = "https://api.osv.dev/v1/query"

def osv_has_vuln(name: str, version: str, osv_api: str = OSV_API) -> bool:
    """Check if a package version has known vulnerabilities."""
    payload = {
        "package": {
            "name": name,
            "ecosystem": "npm"
        },
        "version": version
    }
    
    r = requests.post(osv_api, json=payload, timeout=30)
    r.raise_for_status()
    data = r.json()
    
    vulns = data.get("vulns", [])
    return bool(vulns)  # True if any vulnerabilities found
```

### Integration in Version Selection

```python
def choose_best_version(...):
    for v in reversed(versions):  # Newest first
        # ... compatibility checks ...
        
        # Vulnerability check
        try:
            if osv_has_vuln(name, v):
                continue  # Skip vulnerable version
        except Exception:
            # Network error → be conservative, skip version
            continue
        
        return v  # Safe version found
```

### Error Handling

```python
try:
    has_vuln = osv_has_vuln("express", "4.17.1")
except requests.HTTPError as e:
    # API error (500, 503, etc.)
    print(f"OSV API error: {e}")
    # Conservative: assume vulnerable, skip version
except requests.Timeout:
    # Timeout after 30 seconds
    print("OSV API timeout")
    # Conservative: skip version
except Exception as e:
    # Other errors
    print(f"Unexpected error: {e}")
    # Conservative: skip version
```

### Audit Command

Get detailed vulnerability report:

```python
code, audit_data = PackageUpdatesUtils.run_npm_audit(min_severity="moderate")

if code == 0:
    print("No vulnerabilities found!")
else:
    print(f"Vulnerabilities detected (exit code {code})")
    
    # Save detailed report
    with open("audit.json", "w") as f:
        json.dump(audit_data, f, indent=2)
    
    # Print summary
    metadata = audit_data.get("metadata", {})
    vulnerabilities = metadata.get("vulnerabilities", {})
    for severity, count in vulnerabilities.items():
        if count > 0:
            print(f"  {severity}: {count}")
```

**Example output**:

```
Vulnerabilities detected (exit code 1)
  moderate: 2
  high: 1
  critical: 0
```

### Severity Levels

| Severity | Impact | Action |
|----------|--------|--------|
| **Low** | Minimal impact | Consider updating |
| **Moderate** | Some impact | Should update soon |
| **High** | Significant impact | Update urgently |
| **Critical** | Severe impact | Update immediately |

---

## npm_lookup Bypass Mechanism

### The Problem: Private Packages

Private packages aren't available in the public NPM registry:

```
❌ https://registry.npmjs.org/@company/private-package
   → 404 Not Found
```

**Causes**:
- Company-internal packages
- Scoped packages (@company/*)
- Private npm registry

### The Solution: npm_lookup Parameter

```python
npm_lookup: bool = True  # Default: use NPM registry

# For private packages:
npm_lookup: bool = False  # Skip registry lookup
```

### How It Works

```python
def add_package(self, package_name, version=None, npm_lookup=True, ...):
    if not npm_lookup:
        # Skip NPM registry lookup
        version = version or "latest"
        # Use specified version directly
    else:
        # Normal flow: fetch from NPM registry
        packument = PackageUpdatesUtils.fetch_packument(package_name)
        best = PackageUpdatesUtils.choose_best_version(...)
        version = f"^{best}"
    
    # Add to package.json
    pkg[section][package_name] = version
```

### Usage Examples

#### Example 1: Private Package with Version

```python
packages = [
    {
        "name": "@company/auth-lib",
        "version": "^2.1.0",
        "is_dev": False,
        "npm_lookup": False  # Skip NPM registry
    }
]
```

**Result**: Adds `"@company/auth-lib": "^2.1.0"` directly

#### Example 2: Private Package with "latest"

```python
packages = [
    {
        "name": "@company/utils",
        "is_dev": True,
        "npm_lookup": False  # Will use "latest"
    }
]
```

**Result**: Adds `"@company/utils": "latest"`

#### Example 3: Mixed Public and Private

```python
packages = [
    # Public package - use NPM registry
    {
        "name": "express",
        "is_dev": False,
        "npm_lookup": True  # Fetch from NPM, check compatibility
    },
    # Private package - skip NPM
    {
        "name": "@company/shared-lib",
        "version": "^3.1.2",
        "is_dev": False,
        "npm_lookup": False  # Use specified version
    }
]
```

### InstructionService Configuration

```python
class InstructionService:
    def __init__(self, ...):
        self.node_packages = [
            # Public packages with npm_lookup
            {"name": "express", "is_dev": False, "npm_lookup": True},
            {"name": "lodash", "is_dev": False, "npm_lookup": True},
            
            # Private packages without npm_lookup
            {"name": "@company/shared-lib", "version": "^3.1.2", 
             "is_dev": False, "npm_lookup": False},
            {"name": "@company/auth", "version": "^2.0.0", 
             "is_dev": False, "npm_lookup": False}
        ]
```

### Tool-Level Usage

```python
# When using tools directly
result = package_tools.add_package(
    package_name="@company/private-package",
    version="^1.2.3",
    npm_lookup=False,  # Skip NPM registry lookup
    install=False
)
```

### Important Considerations

**When npm_lookup=False**:
- ✅ No NPM registry access
- ✅ No Node.js compatibility check
- ✅ No vulnerability scan
- ⚠️ **You must specify version manually**
- ⚠️ **You're responsible for compatibility**
- ⚠️ **You're responsible for security**

**Best practices**:
1. Always specify exact version for private packages
2. Manually verify Node.js compatibility
3. Use internal security scanning tools
4. Document why npm_lookup is disabled

---

## Multi-Package Manager Support

### Supported Package Managers

| Manager | Command | Lock File | Notes |
|---------|---------|-----------|-------|
| **npm** | `npm install` | `package-lock.json` | Default, most common |
| **yarn** | `yarn install` | `yarn.lock` | Faster, offline mode |
| **pnpm** | `pnpm install` | `pnpm-lock.yaml` | Disk efficient, strict |

### Installation Implementation

```python
def run_package_manager_install(manager: str, cwd: Optional[str] = None):
    """Run package manager install command."""
    if manager == "npm":
        sh(["npm", "install", "--legacy-peer-deps"], check=True, cwd=cwd)
    elif manager == "yarn":
        sh(["yarn", "install"], check=True, cwd=cwd)
    elif manager == "pnpm":
        sh(["pnpm", "install"], check=True, cwd=cwd)
    else:
        raise SystemExit(f"Unsupported manager: {manager}")
```

### npm Specifics

**Command**: `npm install --legacy-peer-deps`

**Why `--legacy-peer-deps`?**
- Handles peer dependency conflicts gracefully
- More permissive installation
- Common in monorepo setups
- Prevents installation failures from peer dependency mismatches

**Example scenario**:

```
Package A requires react@^17.0.0
Package B requires react@^18.0.0
→ Without --legacy-peer-deps: Installation fails
→ With --legacy-peer-deps: Installation succeeds (uses newest)
```

### yarn Specifics

**Command**: `yarn install`

**Features**:
- Faster than npm (parallel downloads)
- Offline mode support
- Deterministic installs
- Workspaces support

**Advantages**:
- Better monorepo support
- Faster CI/CD pipelines
- Reproducible builds

### pnpm Specifics

**Command**: `pnpm install`

**Features**:
- Content-addressable storage
- Symlink-based node_modules
- Strict dependency resolution
- Monorepo support

**Advantages**:
- Saves disk space (shared packages)
- Faster installations
- Stricter (catches dependency errors)

**Disk usage comparison**:

```
Project with 100 dependencies:
npm:  200 MB
yarn: 180 MB
pnpm:  50 MB (symlinks to shared store)
```

### Specifying Package Manager

#### In Tool Calls

```python
# Using add_package tool
result = tools.add_package(
    package_name="express",
    manager="pnpm",  # Use pnpm
    install=True     # Run pnpm install after adding
)
```

#### In Schemas

```python
class AddPackageInput(BaseModel):
    manager: str = Field(
        default="npm",
        description="Package manager to use (npm, yarn, or pnpm)"
    )
```

#### In Instructions

```python
class NodeJsPackagesInstructions:
    def __init__(self, package_manager="npm", ...):
        self.package_manager = package_manager
```

### Detection from Lock Files

Automatically detect package manager:

```python
def detect_package_manager(project_path: Path) -> str:
    """Detect package manager from lock files."""
    if (project_path / "pnpm-lock.yaml").exists():
        return "pnpm"
    elif (project_path / "yarn.lock").exists():
        return "yarn"
    elif (project_path / "package-lock.json").exists():
        return "npm"
    else:
        return "npm"  # Default
```

### Uninstall Commands

```python
def run_package_manager_uninstall(manager: str, package_name: str):
    """Run package manager uninstall command."""
    if manager == "npm":
        sh(["npm", "uninstall", package_name], check=True)
    elif manager == "yarn":
        sh(["yarn", "remove", package_name], check=True)
    elif manager == "pnpm":
        sh(["pnpm", "remove", package_name], check=True)
```

---

## Version Selection Algorithm

### Overview

The version selection algorithm is the core of intelligent package management. It combines:
1. **Semantic versioning** constraints
2. **Node.js compatibility** requirements
3. **Security vulnerability** scanning
4. **Major version locking** (optional)

### Algorithm Flow

```python
def choose_best_version(
    name: str,              # Package name
    current_range: str,     # Current version range (e.g., "^4.17.0")
    node_ver: str,          # Target Node.js version (e.g., "22.11.0")
    lock_major: bool,       # Lock to current major version?
    packument: Dict         # Package metadata from NPM
) -> Optional[str]:
    
    # Step 1: Get all available versions
    versions = list_versions_from_packument(packument)
    # ['4.0.0', '4.1.0', ..., '4.18.2', '5.0.0']
    
    # Step 2: Determine current major version
    try:
        satisfied = [
            Version.coerce(v) for v in versions
            if Spec(current_range).match(Version.coerce(v))
        ]
        current_major = satisfied[-1].major if satisfied else None
    except:
        current_major = None
    
    # Step 3: Evaluate versions (newest first for efficiency)
    for v in reversed(versions):
        
        # Step 3a: Parse version
        try:
            v_sem = Version.coerce(v)
        except:
            continue  # Skip unparseable versions
        
        # Step 3b: Check major version lock
        if lock_major and current_major and v_sem.major != current_major:
            continue  # Skip different major version
        
        # Step 3c: Check Node.js compatibility
        node_range = engines_node_for_version(packument, v)
        if not is_compatible(node_ver, node_range):
            continue  # Skip incompatible version
        
        # Step 3d: Check for vulnerabilities
        try:
            if osv_has_vuln(name, v):
                continue  # Skip vulnerable version
        except:
            continue  # Skip on error (conservative)
        
        # Step 4: Found suitable version!
        return v
    
    # Step 5: No suitable version found
    return None
```

### Detailed Walkthrough: Selecting express Version

**Given**:
- Package: `express`
- Current: `^4.17.0`
- Node.js: `22.11.0`
- lock_major: `True`

**Step 1: Fetch versions**

```
Available: [4.16.0, 4.16.1, 4.17.0, 4.17.1, 4.17.2, 4.17.3, 
            4.18.0, 4.18.1, 4.18.2, 5.0.0-beta.1]
```

**Step 2: Determine current major**

```python
# Versions that satisfy ^4.17.0
satisfied = [4.17.0, 4.17.1, 4.17.2, 4.17.3, 4.18.0, 4.18.1, 4.18.2]
current_major = 4
```

**Step 3: Evaluate (newest first)**

**Candidate: 5.0.0-beta.1**
```
✓ Parse: major=5, minor=0, patch=0, prerelease=('beta', '1')
✗ Major lock: 5 != 4 (current major)
→ SKIP
```

**Candidate: 4.18.2**
```
✓ Parse: major=4, minor=18, patch=2
✓ Major lock: 4 == 4
✓ Fetch engines.node: ">= 0.10.0"
✓ Compatibility: 22.11.0 satisfies >= 0.10.0
✓ OSV check: No vulnerabilities
→ SELECT!
```

**Result**: `4.18.2`

### Edge Cases

#### Case 1: No Compatible Version

**Scenario**: All versions require Node.js < 20

```python
# Package: old-package
# Available: [1.0.0 (requires Node 12-14), 1.1.0 (requires Node 14-16)]
# Target Node: 22.11.0

for v in [1.1.0, 1.0.0]:
    node_range = ">=14.0.0 <16.0.0"
    if not is_compatible("22.11.0", node_range):
        continue  # Skip

return None  # No compatible version
```

**Result**: Error message to user about incompatibility

#### Case 2: All Versions Have Vulnerabilities

```python
# Package: vulnerable-package
# Available: [1.0.0, 1.1.0, 1.2.0]
# All have known vulnerabilities

for v in [1.2.0, 1.1.0, 1.0.0]:
    if osv_has_vuln(name, v):
        continue  # Skip all

return None  # No safe version
```

**Result**: User warned about no safe version available

#### Case 3: Missing engines.node

```python
# Package: no-engines-package
# Available: [2.0.0 (no engines.node specified)]

node_range = engines_node_for_version(packument, "2.0.0")
# Returns: None

if not is_compatible("22.11.0", None):
    # Missing engines.node → assume compatible
    return True  # Compatible

# Version selected: 2.0.0
```

**Result**: Assumes compatibility (most packages work across Node versions)

#### Case 4: lock_major with Breaking Change Available

```python
# Package: breaking-package
# Current: ^2.5.0
# Available: [2.5.0, 2.6.0, 3.0.0]
# lock_major: True

current_major = 2

for v in [3.0.0, 2.6.0, 2.5.0]:
    if v.major != 2:
        continue  # Skip 3.0.0
    
    # 2.6.0 passes all checks
    return "2.6.0"
```

**Result**: Stays on major version 2, uses 2.6.0

### Performance Optimizations

1. **Reversed iteration**: Starts with newest version
   - Most likely to be best version
   - Early exit on first match

2. **Short-circuit evaluation**: Skip remaining checks on first failure
   ```python
   if major_mismatch:
       continue  # Don't check compatibility or vulnerabilities
   ```

3. **Abbreviated packuments**: 70% smaller responses

4. **Conservative error handling**: Skip version on any error
   - Prevents false positives
   - Ensures safety

### Configuration Options

```python
# Strict: Only patch updates
choose_best_version(name, "~4.17.0", node_ver, lock_major=True, packument)

# Moderate: Minor updates allowed
choose_best_version(name, "^4.17.0", node_ver, lock_major=True, packument)

# Aggressive: Major updates allowed
choose_best_version(name, "^4.17.0", node_ver, lock_major=False, packument)

# Most aggressive: Any version
choose_best_version(name, "*", node_ver, lock_major=False, packument)
```

---

## Package Management Tools

### 1. analyze_packages

**Purpose**: Analyze dependencies and suggest updates without making changes.

**Signature**:

```python
def analyze_packages(
    package_json_path: str = "package.json",
    lock_major: bool = True,
    npm_lookup: bool = True
) -> str
```

**Parameters**:
- `package_json_path`: Path to package.json file
- `lock_major`: Whether to lock major version updates
- `npm_lookup`: Whether to lookup package versions from NPM registry

**Returns**: String with analysis report

**Example**:

```python
result = tools.analyze_packages(
    package_json_path="/path/to/package.json",
    lock_major=True,
    npm_lookup=True
)
```

**Output**:

```
Target Node.js LTS: 22.11.0
Detected Node.js version: 22.11.0
Found 15 dependencies to evaluate.

[UPDATE] express: ^4.17.1 -> ^4.18.2
[UPDATE] lodash: ^4.17.19 -> ^4.17.21
[WARN] old-package: no compatible & non-vulnerable version found
[UPDATE] axios: ^0.21.1 -> ^1.6.5
...

Total updates proposed: 12
```

### 2. update_packages

**Purpose**: Update all package dependencies to latest compatible versions.

**Signature**:

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

**Parameters**:
- `dry_run`: If True, don't modify package.json
- `apply_updates`: If True, run package manager install after updating

**Example (dry run)**:

```python
result = tools.update_packages(
    package_json_path="/path/to/package.json",
    lock_major=True,
    dry_run=True  # Don't modify file
)
```

**Example (apply updates)**:

```python
result = tools.update_packages(
    package_json_path="/path/to/package.json",
    lock_major=True,
    dry_run=False,
    apply_updates=True,  # Run npm install
    manager="npm"
)
```

**Output**:

```
Target Node.js LTS: 22.11.0
Detected Node.js: 22.11.0

[UPDATE] express: ^4.17.1 -> ^4.18.2
[UPDATE] lodash: ^4.17.19 -> ^4.17.21

Successfully updated /path/to/package.json
Dependencies installed using npm
```

### 3. audit_packages

**Purpose**: Audit dependencies for security vulnerabilities.

**Signature**:

```python
def audit_packages(
    package_json_path: str = "package.json",
    min_severity: str | None = None
) -> str
```

**Parameters**:
- `min_severity`: Minimum severity level (`"low"`, `"moderate"`, `"high"`, `"critical"`)

**Example**:

```python
result = tools.audit_packages(
    package_json_path="/path/to/package.json",
    min_severity="moderate"  # Only report moderate and above
)
```

**Output (vulnerabilities found)**:

```
Audit completed with exit code: 1

Vulnerabilities detected. Details saved to audit.json

Vulnerability Summary:
  moderate: 2
  high: 1
```

**Output (no vulnerabilities)**:

```
Audit completed with exit code: 0

No vulnerabilities found!
```

### 4. add_package

**Purpose**: Add a new package to package.json.

**Signature**:

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

**Parameters**:
- `package_name`: Name of package to add
- `version`: Version to install (if None, finds latest compatible)
- `dev`: Add as dev dependency
- `install`: Run package manager install after adding

**Example (auto-select version)**:

```python
result = tools.add_package(
    package_name="axios",
    dev=False,
    install=True,
    npm_lookup=True  # Auto-select best version
)
```

**Output**:

```
Successfully added 'axios@^1.6.5' to dependencies
Package installed using npm
```

**Example (specific version)**:

```python
result = tools.add_package(
    package_name="typescript",
    version="^5.0.0",
    dev=True,
    install=False
)
```

**Output**:

```
Successfully added 'typescript@^5.0.0' to devDependencies
```

**Example (private package)**:

```python
result = tools.add_package(
    package_name="@company/shared-lib",
    version="^3.1.2",
    dev=False,
    npm_lookup=False  # Skip NPM registry
)
```

### 5. remove_package

**Purpose**: Remove a package from package.json.

**Signature**:

```python
def remove_package(
    package_name: str,
    package_json_path: str = "package.json",
    uninstall: bool = False,
    manager: str = "npm"
) -> str
```

**Example**:

```python
result = tools.remove_package(
    package_name="unused-package",
    uninstall=True  # Also run npm uninstall
)
```

**Output**:

```
Successfully removed 'unused-package' from dependencies
Package uninstalled using npm
```

### 6. update_specific_packages

**Purpose**: Update specific packages by name.

**Signature**:

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

**Example**:

```python
result = tools.update_specific_packages(
    package_names=["express", "lodash", "axios"],
    lock_major=True,
    apply_updates=True
)
```

**Output**:

```
Target Node.js LTS: 22.11.0
Detected Node.js: 22.11.0
Updating 3 package(s)...

[UPDATE] express: ^4.17.1 -> ^4.18.2
[UPDATE] lodash: ^4.17.19 -> ^4.17.21
[UPDATE] axios: ^0.21.1 -> ^1.6.5

Successfully updated 3 package(s) in package.json
Dependencies installed using npm
```

### 7. get_package_info

**Purpose**: Get detailed information about a package.

**Signature**:

```python
def get_package_info(
    package_name: str,
    package_json_path: str = "package.json",
    npm_lookup: bool = True
) -> str
```

**Example**:

```python
result = tools.get_package_info(
    package_name="express",
    npm_lookup=True
)
```

**Output**:

```
Current version in dependencies: ^4.17.1

Latest version: 4.18.2
Total versions available: 278
Node.js requirement (latest): >= 0.10.0

Recent versions: 4.18.2, 4.18.1, 4.18.0, 4.17.3, 4.17.2
```

---

## Real-World Examples

### Example 1: Complete Package Update Workflow

**Scenario**: Update all packages in a project to latest compatible versions

```python
# Step 1: Analyze current state
analysis = tools.analyze_packages(
    package_json_path="/project/package.json",
    lock_major=True
)
print(analysis)
# Output: Found 20 dependencies, 12 updates proposed

# Step 2: Dry run to preview changes
preview = tools.update_packages(
    package_json_path="/project/package.json",
    lock_major=True,
    dry_run=True
)
print(preview)
# Output: Shows all proposed updates without modifying file

# Step 3: Apply updates
result = tools.update_packages(
    package_json_path="/project/package.json",
    lock_major=True,
    dry_run=False,
    apply_updates=True,
    manager="npm"
)
print(result)
# Output: Updated 12 packages, ran npm install

# Step 4: Audit for vulnerabilities
audit = tools.audit_packages(
    package_json_path="/project/package.json",
    min_severity="moderate"
)
print(audit)
# Output: No vulnerabilities found!
```

### Example 2: Setting Up a New Project

**Scenario**: Add dependencies to a new project

```python
# Add production dependencies
tools.add_package("express", install=False)
tools.add_package("body-parser", install=False)
tools.add_package("cors", install=False)
tools.add_package("dotenv", install=False)

# Add development dependencies
tools.add_package("typescript", dev=True, install=False)
tools.add_package("@types/node", dev=True, install=False)
tools.add_package("@types/express", dev=True, install=False)
tools.add_package("jest", dev=True, install=False)

# Install all at once
tools.update_packages(
    dry_run=False,
    apply_updates=True,
    manager="npm"
)
```

### Example 3: Upgrading with Major Version Unlocked

**Scenario**: Allow major version upgrades for specific packages

```python
# Update specific packages with major version changes allowed
result = tools.update_specific_packages(
    package_names=["webpack", "webpack-cli", "babel-loader"],
    lock_major=False,  # Allow major version bumps
    apply_updates=True
)
print(result)
# Output: webpack: ^4.46.0 -> ^5.89.0
```

### Example 4: Mixed Public and Private Packages

**Scenario**: Project with both public and private dependencies

```python
# Configuration in InstructionService
packages = [
    # Public packages
    {"name": "express", "is_dev": False, "npm_lookup": True},
    {"name": "lodash", "is_dev": False, "npm_lookup": True},
    
    # Private packages
    {"name": "@company/auth-lib", "version": "^2.1.0", 
     "is_dev": False, "npm_lookup": False},
    {"name": "@company/database-lib", "version": "^1.3.0", 
     "is_dev": False, "npm_lookup": False}
]

# Generate and execute instructions
instructions = NodeJsPackagesInstructions(
    clone_path="/project/",
    packages=packages,
    node_lts_version="22.11.0"
)

for instruction in instructions.get_instructions():
    agent.execute(instruction)
```

### Example 5: Monorepo Package Management

**Scenario**: Update packages in a monorepo with multiple package.json files

```python
packages_to_update = [
    "/monorepo/packages/api/package.json",
    "/monorepo/packages/web/package.json",
    "/monorepo/packages/mobile/package.json"
]

for pkg_path in packages_to_update:
    print(f"\nUpdating {pkg_path}...")
    
    # Analyze
    analysis = tools.analyze_packages(pkg_path)
    print(analysis)
    
    # Update
    result = tools.update_packages(
        package_json_path=pkg_path,
        lock_major=True,
        apply_updates=False,  # Don't install yet
        manager="pnpm"  # Using pnpm for monorepo
    )
    print(result)

# Install all at root level (for monorepos)
subprocess.run(["pnpm", "install"], check=True, cwd="/monorepo")
```

### Example 6: Security-Focused Update

**Scenario**: Only update packages with known vulnerabilities

```python
# Step 1: Audit to find vulnerable packages
audit_result = tools.audit_packages(min_severity="moderate")
print(audit_result)

# Step 2: Parse vulnerable packages from audit.json
with open("audit.json") as f:
    audit_data = json.load(f)

vulnerable_packages = set()
for advisory in audit_data.get("advisories", {}).values():
    vulnerable_packages.add(advisory["module_name"])

# Step 3: Update only vulnerable packages
if vulnerable_packages:
    result = tools.update_specific_packages(
        package_names=list(vulnerable_packages),
        lock_major=True,  # Conservative updates
        apply_updates=True
    )
    print(result)

# Step 4: Re-audit to verify
final_audit = tools.audit_packages()
print(final_audit)
```

---

## Best Practices

### 1. Version Range Selection

**Recommendation**: Use caret (`^`) for most dependencies

```json
{
  "dependencies": {
    "express": "^4.18.2",      // ✅ Good: allows compatible updates
    "lodash": "~4.17.21",      // ⚠️  Too strict: only patch updates
    "axios": "1.6.5",          // ❌ Bad: no updates allowed
    "react": "*"               // ❌ Dangerous: unpredictable updates
  }
}
```

**When to use different ranges**:
- `^X.Y.Z`: Default for most packages
- `~X.Y.Z`: When API is unstable, want only bug fixes
- `X.Y.Z`: For critical packages where stability is paramount
- `*` or `latest`: Never in production

### 2. Lock Major Versions by Default

```python
# ✅ Good: Prevents breaking changes
tools.update_packages(lock_major=True)

# ⚠️  Use with caution: Can introduce breaking changes
tools.update_packages(lock_major=False)
```

**When to unlock major versions**:
- Development environment
- Dedicated migration branch
- After reviewing CHANGELOG
- With comprehensive test coverage

### 3. Always Dry Run First

```python
# Step 1: Preview changes
preview = tools.update_packages(dry_run=True)
review(preview)

# Step 2: Apply if satisfied
if looks_good:
    tools.update_packages(dry_run=False, apply_updates=True)
```

### 4. Regular Vulnerability Audits

```python
# Run daily/weekly in CI/CD
audit_result = tools.audit_packages(min_severity="moderate")

if "vulnerabilities detected" in audit_result.lower():
    send_alert()
    create_ticket()
```

### 5. Separate Dev and Prod Dependencies

```json
{
  "dependencies": {
    // Only runtime dependencies
    "express": "^4.18.2",
    "axios": "^1.6.5"
  },
  "devDependencies": {
    // Only development tools
    "typescript": "^5.0.0",
    "jest": "^29.0.0"
  }
}
```

### 6. Document Private Packages

```python
packages = [
    {
        "name": "@company/auth-lib",
        "version": "^2.1.0",
        "is_dev": False,
        "npm_lookup": False  # Private package: @company internal auth library
    }
]
```

### 7. Pin Node.js Version

```bash
# .nvmrc
22.11.0
```

```json
// package.json
{
  "engines": {
    "node": ">=22.0.0 <23.0.0",
    "npm": ">=10.0.0"
  }
}
```

### 8. Use Package Manager Locks

```bash
# Commit lock files
git add package-lock.json  # for npm
git add yarn.lock          # for yarn
git add pnpm-lock.yaml     # for pnpm
```

**Why?** Ensures consistent installations across environments.

### 9. Test After Updates

```bash
# After updating packages
npm install
npm test
npm run build
npm run lint
```

### 10. Gradual Updates in Production

**Strategy**:
1. Update in development branch
2. Run full test suite
3. Deploy to staging
4. Monitor for issues
5. Gradual rollout to production

---

## Troubleshooting

### Issue 1: "Package not found" Error

**Symptom**:
```
Error: Package 'my-package' not found
```

**Causes**:
1. Typo in package name
2. Package doesn't exist
3. Private package without npm_lookup=False
4. Custom registry not configured

**Solutions**:

```python
# Check package name spelling
tools.get_package_info("expres")  # ❌
tools.get_package_info("express")  # ✅

# For private packages
tools.add_package(
    "@company/package",
    npm_lookup=False,  # ✅ Skip public registry
    version="^1.0.0"
)

# Configure custom registry
tools = PackageUpdatesTools(
    node_lts_version="22.11.0",
    npm_registry="https://registry.company.com"  # ✅
)
```

### Issue 2: "No compatible version found"

**Symptom**:
```
[WARN] old-package: no compatible & non-vulnerable version found
```

**Causes**:
1. Package doesn't support current Node.js version
2. All versions have vulnerabilities
3. Major version lock too restrictive

**Solutions**:

```python
# Check package info
info = tools.get_package_info("old-package")
print(info)
# Check Node.js requirements for each version

# Try without major version lock
tools.update_specific_packages(
    package_names=["old-package"],
    lock_major=False  # ✅ Allow major version change
)

# Or use older Node.js version if possible
agent = Agent(node_lts_version="18.0.0")  # ✅
```

### Issue 3: "All versions vulnerable"

**Symptom**:
```
Error: Could not find non-vulnerable version
```

**Solutions**:

1. **Check for recent updates**:
   ```python
   info = tools.get_package_info("vulnerable-package")
   # See if newer versions exist
   ```

2. **Consider alternatives**:
   ```python
   # Find alternative packages
   # Example: use 'axios' instead of 'request'
   tools.remove_package("request")
   tools.add_package("axios")
   ```

3. **Temporary workaround** (with caution):
   ```python
   # Add with npm_lookup=False temporarily
   # While waiting for security fix
   tools.add_package(
       "vulnerable-package",
       version="^1.2.3",
       npm_lookup=False  # ⚠️ Bypass security check
   )
   # TODO: Monitor for security updates
   ```

### Issue 4: "npm install fails" After Update

**Symptom**:
```
npm ERR! peer dependency conflict
```

**Solutions**:

```bash
# Use --legacy-peer-deps (already in tools)
npm install --legacy-peer-deps  # ✅

# Or update peerDependencies manually
# Check package warnings for required versions
```

```python
# Or use yarn/pnpm (better peer dependency handling)
tools.update_packages(
    manager="yarn",  # ✅ or "pnpm"
    apply_updates=True
)
```

### Issue 5: OSV API Timeout

**Symptom**:
```
OSV API timeout
```

**Causes**:
1. Network issues
2. OSV API temporarily down
3. Firewall blocking requests

**Solutions**:

```python
# Retry with longer timeout
import requests

# Modify timeout in PackageUpdatesUtils
def osv_has_vuln(name, version):
    # ... existing code ...
    r = requests.post(osv_api, json=payload, timeout=60)  # ✅ Increase timeout
```

```python
# Or skip vulnerability checks temporarily
tools.analyze_packages(npm_lookup=False)  # ⚠️ Skips all checks
```

### Issue 6: Private Package Version Mismatch

**Symptom**:
```
Error: Version mismatch for @company/package
```

**Solution**:

```python
# Always specify exact version for private packages
tools.add_package(
    "@company/package",
    version="^2.1.0",  # ✅ Explicit version
    npm_lookup=False
)

# Keep package list updated
# In InstructionService
self.node_packages = [
    {
        "name": "@company/package",
        "version": "^2.1.0",  # ✅ Update this when bumping version
        "npm_lookup": False
    }
]
```

### Issue 7: engines.node Mismatch

**Symptom**:
```
Error: The engine "node" is incompatible with this module
```

**Solutions**:

```bash
# Check current Node.js version
node -v
# v22.11.0

# Check required version in package.json
cat package.json | grep engines
# "engines": { "node": ">=18.0.0" }
```

```python
# Update .nvmrc
# echo "22.11.0" > .nvmrc

# Or install compatible Node.js version
# nvm install 22.11.0
# nvm use 22.11.0
```

### Issue 8: Package Lock Conflicts

**Symptom**:
```
CONFLICT in package-lock.json
```

**Solutions**:

```bash
# Delete lock file and regenerate
rm package-lock.json
npm install

# Or accept their version
git checkout --theirs package-lock.json
npm install

# Or accept your version
git checkout --ours package-lock.json
npm install
```

---

## Conclusion

CodeBaseOpsAI-v2-1's package management system provides:

✅ **Intelligent version selection** combining compatibility and security
✅ **Comprehensive vulnerability scanning** via OSV API
✅ **Flexible configuration** for public and private packages
✅ **Multi-package manager support** (npm, yarn, pnpm)
✅ **Safe defaults** with conservative error handling

**Key Takeaways**:

1. Always use `lock_major=True` for production
2. Run `dry_run=True` before applying changes
3. Regular vulnerability audits are essential
4. Private packages require `npm_lookup=False`
5. Test thoroughly after updates

---

**Next Steps**:
- See [UNDERSTANDING.md](UNDERSTANDING.md) for architecture deep dive
- Review [CONFIGURATION.md](CONFIGURATION.md) for setup details
- Check [QUICKSTART.md](QUICKSTART.md) to get started

---

*Last Updated: January 17, 2026*
*Version: 2.1*
