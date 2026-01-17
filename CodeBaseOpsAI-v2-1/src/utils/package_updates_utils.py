"""
Utility functions for package updates and version management.
"""
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests
from semantic_version import Version, Spec


# ----------------------------
# Config defaults & constants
# ----------------------------
NPM_REGISTRY = "https://registry.npmjs.org"
OSV_API = "https://api.osv.dev/v1/query"
ABBREV_ACCEPT = "application/vnd.npm.install-v1+json"  # smaller metadata


class PackageUpdatesUtils:
    """Utility class for npm package updates and version management."""

    @staticmethod
    def sh(cmd: List[str], check: bool = True, capture: bool = False, cwd: Optional[str] = None) -> subprocess.CompletedProcess:
        """Execute a shell command.

        Args:
            cmd: Command and arguments as a list
            check: Whether to raise exception on non-zero exit
            capture: Whether to capture stdout
            cwd: Working directory for the command (optional)

        Returns:
            CompletedProcess instance
        """
        return subprocess.run(
            cmd,
            check=check,
            stdout=subprocess.PIPE if capture else None,
            stderr=subprocess.STDOUT,
            cwd=cwd
        )

    @staticmethod
    def detect_node_version(pkg: Dict) -> str:
        """Detect the Node.js version from .nvmrc, node -v, or package.json.

        Args:
            pkg: package.json data as dictionary

        Returns:
            Node.js version string
        """
        # Priority: .nvmrc > node -v > package.json engines.node
        if Path(".nvmrc").exists():
            raw = Path(".nvmrc").read_text(encoding="utf-8").strip()
            # .nvmrc may contain "18" or "v18.20.4"
            v = raw.lstrip("v")
            return v

        try:
            out = PackageUpdatesUtils.sh(
                ["node", "-v"], capture=True).stdout.decode().strip()
            return out.lstrip("v")
        except Exception:
            pass

        # Fallback to engines.node lower bound
        node_range = pkg.get("engines", {}).get("node")
        if node_range:
            min_v = Spec(node_range).select([
                Version("10.0.0"), Version("12.0.0"), Version("14.0.0"),
                Version("16.0.0"), Version("18.0.0"), Version("20.0.0")
            ])
            if min_v:
                return str(min_v)

        # last resort
        return "18.0.0"

    @staticmethod
    def load_deps(pkg: Dict) -> Dict[str, str]:
        """Load all dependencies from package.json.

        Args:
            pkg: package.json data as dictionary

        Returns:
            Dictionary mapping package names to version ranges
        """
        deps = {}
        for section in ("dependencies", "devDependencies"):
            if section in pkg and isinstance(pkg[section], dict):
                deps.update(pkg[section])
        return deps

    @staticmethod
    def fetch_packument(name: str, registry: str = NPM_REGISTRY) -> Dict:
        """Fetch package metadata from npm registry.

        Args:
            name: Package name
            registry: Registry URL (default: NPM_REGISTRY)

        Returns:
            Package metadata dictionary
        """
        url = f"{registry}/{name}"
        headers = {"Accept": ABBREV_ACCEPT}
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        return resp.json()

    @staticmethod
    def list_versions_from_packument(packument: Dict) -> List[str]:
        """Extract and sort versions from packument.

        Args:
            packument: Package metadata

        Returns:
            Sorted list of version strings
        """
        versions = packument.get("versions", {})
        return sorted(versions.keys(), key=lambda v: Version.coerce(v))

    @staticmethod
    def engines_node_for_version(packument: Dict, version: str) -> Optional[str]:
        """Get the Node.js engine requirement for a specific package version.

        Args:
            packument: Package metadata
            version: Package version string

        Returns:
            Node.js version range string or None
        """
        vmeta = packument.get("versions", {}).get(version, {})
        engines = vmeta.get("engines")
        if isinstance(engines, dict):
            return engines.get("node")
        return None

    @staticmethod
    def is_compatible(node_ver: str, node_range: Optional[str]) -> bool:
        """Check if a Node.js version is compatible with a range.

        Args:
            node_ver: Node.js version string
            node_range: Node.js version range or None

        Returns:
            True if compatible, False otherwise
        """
        if not node_range:
            # Missing engines.node --> treat as "probably compatible"
            return True

        try:
            node_spec = Spec(node_range)
            return Version.coerce(node_ver) in node_spec
        except Exception:
            # If range unparsable, be conservative
            return False

    @staticmethod
    def osv_has_vuln(name: str, version: str, osv_api: str = OSV_API) -> bool:
        """Check if a package version has known vulnerabilities via OSV API.

        Args:
            name: Package name
            version: Package version
            osv_api: OSV API endpoint URL

        Returns:
            True if vulnerabilities found, False otherwise
        """
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
        return bool(vulns)

    @staticmethod
    def choose_best_version(
        name: str,
        current_range: str,
        node_ver: str,
        lock_major: bool,
        packument: Dict
    ) -> Optional[str]:
        """Choose the best compatible and non-vulnerable version.

        Args:
            name: Package name
            current_range: Current version range
            node_ver: Node.js version
            lock_major: Whether to lock to current major version
            packument: Package metadata

        Returns:
            Best version string or None
        """
        versions = PackageUpdatesUtils.list_versions_from_packument(packument)

        # Evaluate highest first
        for v in reversed(versions):
            try:
                v_sem = Version.coerce(v)
            except Exception:
                continue

            # If lock_major, restrict candidate major to current_range's major when possible
            try:
                sat = [
                    Version.coerce(x) for x in versions
                    if Spec(current_range).match(Version.coerce(x))
                ]
                current_major = sat[-1].major if sat else None
                if lock_major and current_major is not None and v_sem.major != current_major:
                    continue
            except Exception:
                pass

            node_range = PackageUpdatesUtils.engines_node_for_version(
                packument, v)
            if not PackageUpdatesUtils.is_compatible(node_ver, node_range):
                continue

            # Vulnerability check via OSV
            try:
                if PackageUpdatesUtils.osv_has_vuln(name, v):
                    continue
            except Exception:
                # Network hiccup: skip rejecting, but prefer safer behavior
                continue

            # Candidate passes both gates
            return v

        return None

    @staticmethod
    def update_pkg_ranges(pkg: Dict, updates: Dict[str, str]) -> Dict:
        """Update package.json with new version ranges.

        Args:
            pkg: package.json data as dictionary
            updates: Dictionary mapping package names to new version ranges

        Returns:
            Updated package.json dictionary
        """
        for section in ("dependencies", "devDependencies"):
            if section in pkg and isinstance(pkg[section], dict):
                for name, new_range in updates.items():
                    if name in pkg[section]:
                        pkg[section][name] = new_range
        return pkg

    @staticmethod
    def run_package_manager_install(manager: str, cwd: Optional[str] = None):
        """Run package manager install command.

        Args:
            manager: Package manager name (npm, yarn, or pnpm)
            cwd: Working directory where package.json is located (optional)
        """
        if manager == "npm":
            PackageUpdatesUtils.sh(
                ["npm", "install", "--legacy-peer-deps"], check=True, cwd=cwd)
        elif manager == "yarn":
            PackageUpdatesUtils.sh(["yarn", "install"], check=True, cwd=cwd)
        elif manager == "pnpm":
            PackageUpdatesUtils.sh(["pnpm", "install"], check=True, cwd=cwd)
        else:
            raise SystemExit(f"Unsupported manager: {manager}")

    @staticmethod
    def run_npm_audit(min_severity: Optional[str] = None) -> Tuple[int, Dict]:
        """Run npm audit and return results.

        Args:
            min_severity: Minimum severity level (optional)

        Returns:
            Tuple of (exit_code, audit_data_dict)
        """
        args = ["npm", "audit", "--json"]
        if min_severity:
            args.insert(2, f"--audit-level={min_severity}")

        cp = PackageUpdatesUtils.sh(args, check=False, capture=True)
        try:
            data = json.loads(cp.stdout.decode())
        except Exception:
            data = {}

        return cp.returncode, data

    @staticmethod
    def parse_args(argv: List[str]) -> Dict:
        """Parse command-line arguments.

        Args:
            argv: Command-line arguments list

        Returns:
            Dictionary of parsed arguments
        """
        args = {
            "apply": "--apply" in argv,
            "dry": "--dry-run" in argv or "--dry" in argv,
            "manager": "npm",  # DEFAULT_MANAGER
            "lock_major": True,  # DEFAULT_KEEP_MAJOR
            "audit": "--audit" in argv,
            "min_severity": None
        }

        for i, a in enumerate(argv):
            if a == "--manager" and i + 1 < len(argv):
                args["manager"] = argv[i + 1]
            if a == "--no-lock-major":
                args["lock_major"] = False
            if a == "--min-severity" and i + 1 < len(argv):
                args["min_severity"] = argv[i + 1]

        return args


# Make sure json is imported for run_npm_audit
