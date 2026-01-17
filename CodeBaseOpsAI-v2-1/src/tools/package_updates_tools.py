"""
Package updates tools for npm dependency management.
Provides tools to analyze, update, and audit npm package dependencies.
"""
import json
import os
from pathlib import Path
from typing import Dict, List
from langchain_core.tools import StructuredTool
from semantic_version import Version, Spec

from ..utils import JsonUtils, PackageUpdatesUtils
from ..schemas.package_schemas import (
    AnalyzePackagesInput,
    UpdatePackagesInput,
    AuditPackagesInput,
    AddPackageInput,
    RemovePackageInput,
    UpdateSpecificPackagesInput,
    GetPackageInfoInput
)


class PackageUpdatesTools:
    """A collection of npm package update tools for the agent to use."""

    def __init__(self, node_lts_version: str, npm_registry: str | None = None) -> None:
        """Initialize package updates tools.

        Args:
            node_lts_version: Node.js LTS version for package compatibility checks
            npm_registry: NPM registry URL (default: from env or https://registry.npmjs.org)
        """
        self.npm_registry = npm_registry or os.getenv(
            "NPM_REGISTRY", "https://registry.npmjs.org")
        self.node_lts_version = node_lts_version

    def _evaluate_package_updates(
        self,
        package_path: Path,
        lock_major: bool,
        verbose: bool = True,
        npm_lookup: bool = True
    ) -> tuple[Dict[str, str], List[str], str]:
        """Internal method to evaluate package updates.

        Args:
            package_path: Path to package.json file
            lock_major: Whether to lock major version updates
            verbose: Whether to include detailed messages
            npm_lookup: Whether to lookup package versions from npm registry

        Returns:
            Tuple of (proposed_updates_dict, report_lines_list, node_version)
        """
        pkg = JsonUtils.read_json(package_path)
        # Use instance node_lts_version or detect from environment
        node_ver = self.node_lts_version if self.node_lts_version is not None else PackageUpdatesUtils.detect_node_version(
            pkg)
        deps = PackageUpdatesUtils.load_deps(pkg)

        report_lines = []
        if verbose:
            report_lines.extend([
                f"Detected Node.js version: {node_ver}",
                f"Found {len(deps)} dependencies to evaluate.",
                ""
            ])

        proposed: Dict[str, str] = {}

        # Skip npm lookup if npm_lookup is False
        if not npm_lookup:
            if verbose:
                report_lines.append(
                    "npm_lookup is disabled. Skipping npm registry version checks.")
            return proposed, report_lines, node_ver

        for name, current_range in deps.items():
            try:
                packument = PackageUpdatesUtils.fetch_packument(
                    name, self.npm_registry)
            except Exception as e:
                if verbose:
                    report_lines.append(
                        f"[SKIP] {name}: registry fetch failed: {e}")
                continue

            best = PackageUpdatesUtils.choose_best_version(
                name, current_range, node_ver, lock_major, packument
            )

            if not best:
                if verbose:
                    report_lines.append(
                        f"[WARN] {name}: no compatible & non-vulnerable version found")
                continue

            new_range = f"^{best}"
            proposed[name] = new_range
            if verbose:
                report_lines.append(
                    f"[UPDATE] {name}: {current_range} -> {new_range}")

        return proposed, report_lines, node_ver

    def analyze_packages(self, package_json_path: str = "package.json", lock_major: bool = True, npm_lookup: bool = True) -> str:
        """Analyze package dependencies and suggest updates.

        Args:
            package_json_path: Path to package.json file
            lock_major: Whether to lock major version updates
            npm_lookup: Whether to lookup package versions from npm registry

        Returns:
            String with analysis report
        """
        try:
            package_path = Path(package_json_path)
            if not package_path.exists():
                return f"Error: package.json not found at {package_json_path}"

            proposed, report_lines, _ = self._evaluate_package_updates(
                package_path, lock_major, verbose=True, npm_lookup=npm_lookup
            )

            # Prepend Node.js version info
            report_lines.insert(
                0, f"Target Node.js LTS: {self.node_lts_version}")

            if not proposed:
                report_lines.append("\nNo updates proposed.")
            else:
                report_lines.append(
                    f"\nTotal updates proposed: {len(proposed)}")

            return "\n".join(report_lines)

        except Exception as e:
            return f"Error analyzing packages: {str(e)}"

    def update_packages(
        self,
        package_json_path: str = "package.json",
        lock_major: bool = True,
        dry_run: bool = False,
        apply_updates: bool = False,
        manager: str = "npm",
        npm_lookup: bool = True
    ) -> str:
        """Update package dependencies in package.json.

        Args:
            package_json_path: Path to package.json file
            lock_major: Whether to lock major version updates
            dry_run: Whether to perform a dry run without modifying files
            apply_updates: Whether to run package manager install after updating
            manager: Package manager to use (npm, yarn, or pnpm)
            npm_lookup: Whether to lookup package versions from npm registry

        Returns:
            String with update status
        """
        try:
            package_path = Path(package_json_path)
            if not package_path.exists():
                return f"Error: package.json not found at {package_json_path}"

            proposed, report_lines, node_ver = self._evaluate_package_updates(
                package_path, lock_major, verbose=True, npm_lookup=npm_lookup
            )

            # Prepend version info
            report_lines.insert(
                0, f"Target Node.js LTS: {self.node_lts_version}")
            report_lines.insert(1, f"Detected Node.js: {node_ver}")

            if not proposed:
                return "No updates proposed."

            if dry_run:
                report_lines.append(
                    "\nDry-run mode: package.json not modified.")
                return "\n".join(report_lines)

            # Apply changes
            pkg = JsonUtils.read_json(package_path)
            updated_pkg = PackageUpdatesUtils.update_pkg_ranges(pkg, proposed)
            JsonUtils.write_json(package_path, updated_pkg)
            report_lines.append(f"\nSuccessfully updated {package_json_path}")

            if apply_updates:
                PackageUpdatesUtils.run_package_manager_install(
                    manager, cwd=str(package_path.parent))
                report_lines.append(f"Dependencies installed using {manager}")

            return "\n".join(report_lines)

        except Exception as e:
            return f"Error updating packages: {str(e)}"

    def audit_packages(
        self,
        package_json_path: str = "package.json",
        min_severity: str | None = None
    ) -> str:
        """Audit package dependencies for vulnerabilities.

        Args:
            package_json_path: Path to package.json file
            min_severity: Minimum severity level (low, moderate, high, critical)

        Returns:
            String with audit results
        """
        try:
            package_path = Path(package_json_path)
            if not package_path.exists():
                return f"Error: package.json not found at {package_json_path}"

            code, audit_data = PackageUpdatesUtils.run_npm_audit(min_severity)

            report_lines = [
                f"Audit completed with exit code: {code}",
                ""
            ]

            if code == 0:
                report_lines.append("No vulnerabilities found!")
            else:
                # Save audit results
                audit_file = Path("audit.json")
                audit_file.write_text(
                    json.dumps(audit_data, indent=2) + "\n",
                    encoding="utf-8"
                )
                report_lines.append(
                    f"Vulnerabilities detected. Details saved to {audit_file}")

                # Add summary if available
                if "metadata" in audit_data:
                    metadata = audit_data["metadata"]
                    vulnerabilities = metadata.get("vulnerabilities", {})
                    if vulnerabilities:
                        report_lines.append("\nVulnerability Summary:")
                        for severity, count in vulnerabilities.items():
                            if count > 0:
                                report_lines.append(f"  {severity}: {count}")

            return "\n".join(report_lines)

        except Exception as e:
            return f"Error auditing packages: {str(e)}"

    def add_package(
        self,
        package_name: str,
        version: str | None = None,
        package_json_path: str = "package.json",
        dev: bool = False,
        install: bool = False,
        manager: str = "npm",
        npm_lookup: bool = True,
        node_lts_version: str | None = None
    ) -> str:
        """Add a new package to package.json.

        Args:
            package_name: Name of the package to add
            version: Version to install (if None, finds latest compatible)
            package_json_path: Path to package.json file
            dev: Whether to add as dev dependency
            install: Whether to run package manager install after adding
            manager: Package manager to use (npm, yarn, or pnpm)
            npm_lookup: Whether to lookup package versions from npm registry
            node_lts_version: Node.js LTS version for compatibility checks (uses instance default if None)

        Returns:
            String with operation status
        """
        try:
            package_path = Path(package_json_path)
            if not package_path.exists():
                return f"Error: package.json not found at {package_json_path}"

            pkg = JsonUtils.read_json(package_path)
            section = "devDependencies" if dev else "dependencies"

            # Check if package already exists
            if section in pkg and package_name in pkg[section]:
                return f"Package '{package_name}' already exists in {section}"

            # Determine version to use
            if not version or version == "latest":
                if npm_lookup:
                    try:
                        # Use provided node_lts_version or instance default or detect from environment
                        target_node_version = node_lts_version or self.node_lts_version
                        if not target_node_version:
                            target_node_version = PackageUpdatesUtils.detect_node_version(
                                pkg)

                        packument = PackageUpdatesUtils.fetch_packument(
                            package_name, self.npm_registry)
                        best = PackageUpdatesUtils.choose_best_version(
                            package_name, "*", target_node_version, False, packument
                        )
                        if best:
                            version = f"^{best}"
                        else:
                            return f"Error: Could not find compatible version for '{package_name}' compatible with Node.js {target_node_version}"
                    except Exception as e:
                        return f"Error fetching package info: {str(e)}"
                else:
                    # If npm_lookup is False, use "latest" as the version
                    version = "latest"

            # Ensure section exists
            if section not in pkg:
                pkg[section] = {}

            # Add package
            pkg[section][package_name] = version
            JsonUtils.write_json(package_path, pkg)

            result = f"Successfully added '{package_name}@{version}' to {section}"

            if install:
                PackageUpdatesUtils.run_package_manager_install(
                    manager, cwd=str(package_path.parent))
                result += f"\nPackage installed using {manager}"

            return result

        except Exception as e:
            return f"Error adding package: {str(e)}"

    def remove_package(
        self,
        package_name: str,
        package_json_path: str = "package.json",
        uninstall: bool = False,
        manager: str = "npm"
    ) -> str:
        """Remove a package from package.json.

        Args:
            package_name: Name of the package to remove
            package_json_path: Path to package.json file
            uninstall: Whether to run package manager uninstall
            manager: Package manager to use (npm, yarn, or pnpm)

        Returns:
            String with operation status
        """
        try:
            package_path = Path(package_json_path)
            if not package_path.exists():
                return f"Error: package.json not found at {package_json_path}"

            pkg = JsonUtils.read_json(package_path)
            found = False
            removed_from = None

            # Check both dependencies and devDependencies
            for section in ("dependencies", "devDependencies"):
                if section in pkg and package_name in pkg[section]:
                    del pkg[section][package_name]
                    found = True
                    removed_from = section
                    break

            if not found:
                return f"Package '{package_name}' not found in package.json"

            JsonUtils.write_json(package_path, pkg)
            result = f"Successfully removed '{package_name}' from {removed_from}"

            if uninstall:
                try:
                    if manager == "npm":
                        PackageUpdatesUtils.sh(
                            ["npm", "uninstall", package_name], check=True)
                    elif manager == "yarn":
                        PackageUpdatesUtils.sh(
                            ["yarn", "remove", package_name], check=True)
                    elif manager == "pnpm":
                        PackageUpdatesUtils.sh(
                            ["pnpm", "remove", package_name], check=True)
                    result += f"\nPackage uninstalled using {manager}"
                except Exception as e:
                    result += f"\nWarning: Failed to uninstall: {str(e)}"

            return result

        except Exception as e:
            return f"Error removing package: {str(e)}"

    def update_specific_packages(
        self,
        package_names: list[str],
        package_json_path: str = "package.json",
        lock_major: bool = True,
        apply_updates: bool = False,
        manager: str = "npm",
        npm_lookup: bool = True
    ) -> str:
        """Update specific packages to their latest compatible versions.

        Args:
            package_names: List of package names to update
            package_json_path: Path to package.json file
            lock_major: Whether to lock major version updates
            apply_updates: Whether to run package manager install after updating
            manager: Package manager to use (npm, yarn, or pnpm)
            npm_lookup: Whether to lookup package versions from npm registry

        Returns:
            String with update status
        """
        try:
            package_path = Path(package_json_path)
            if not package_path.exists():
                return f"Error: package.json not found at {package_json_path}"

            pkg = JsonUtils.read_json(package_path)
            # Use instance node_lts_version or detect from environment
            node_ver = self.node_lts_version if self.node_lts_version != "18.0.0" else PackageUpdatesUtils.detect_node_version(
                pkg)
            deps = PackageUpdatesUtils.load_deps(pkg)

            # Filter to only requested packages
            requested_deps = {name: version for name,
                              version in deps.items() if name in package_names}

            if not requested_deps:
                return f"None of the specified packages found in package.json"

            proposed: Dict[str, str] = {}
            report_lines = [
                f"Target Node.js LTS: {self.node_lts_version}",
                f"Detected Node.js: {node_ver}",
                f"Updating {len(requested_deps)} package(s)...",
                ""
            ]

            # Skip npm lookup if npm_lookup is False
            if not npm_lookup:
                report_lines.append(
                    "npm_lookup is disabled. Skipping npm registry version checks.")
                return "\n".join(report_lines) + "\n\nNo updates applied."

            for name, current_range in requested_deps.items():
                try:
                    packument = PackageUpdatesUtils.fetch_packument(
                        name, self.npm_registry)
                    best = PackageUpdatesUtils.choose_best_version(
                        name, current_range, node_ver, lock_major, packument
                    )

                    if best:
                        new_range = f"^{best}"
                        proposed[name] = new_range
                        report_lines.append(
                            f"[UPDATE] {name}: {current_range} -> {new_range}")
                    else:
                        report_lines.append(
                            f"[SKIP] {name}: no compatible version found")
                except Exception as e:
                    report_lines.append(f"[ERROR] {name}: {str(e)}")

            if not proposed:
                return "\n".join(report_lines) + "\n\nNo updates applied."

            # Apply changes
            updated_pkg = PackageUpdatesUtils.update_pkg_ranges(pkg, proposed)
            JsonUtils.write_json(package_path, updated_pkg)
            report_lines.append(
                f"\nSuccessfully updated {len(proposed)} package(s) in {package_json_path}")

            if apply_updates:
                PackageUpdatesUtils.run_package_manager_install(
                    manager, cwd=str(package_path.parent))
                report_lines.append(f"Dependencies installed using {manager}")

            return "\n".join(report_lines)

        except Exception as e:
            return f"Error updating specific packages: {str(e)}"

    def get_package_info(
        self,
        package_name: str,
        package_json_path: str = "package.json",
        npm_lookup: bool = True
    ) -> str:
        """Get information about a specific package.

        Args:
            package_name: Name of the package to get information about
            package_json_path: Path to package.json file
            npm_lookup: Whether to lookup package versions from npm registry

        Returns:
            String with package information
        """
        try:
            package_path = Path(package_json_path)
            info_lines = []

            # Check if it exists in package.json
            if package_path.exists():
                pkg = JsonUtils.read_json(package_path)
                for section in ("dependencies", "devDependencies"):
                    if section in pkg and package_name in pkg[section]:
                        current_version = pkg[section][package_name]
                        info_lines.append(
                            f"Current version in {section}: {current_version}")
                        break
                else:
                    info_lines.append(
                        f"Package '{package_name}' not found in {package_json_path}")

            # Fetch registry information if npm_lookup is enabled
            if npm_lookup:
                try:
                    packument = PackageUpdatesUtils.fetch_packument(
                        package_name, self.npm_registry)
                    versions = PackageUpdatesUtils.list_versions_from_packument(
                        packument)

                    if versions:
                        latest = versions[-1]
                        info_lines.append(f"\nLatest version: {latest}")
                        info_lines.append(
                            f"Total versions available: {len(versions)}")

                        # Show Node.js compatibility for latest version
                        node_range = PackageUpdatesUtils.engines_node_for_version(
                            packument, latest)
                        if node_range:
                            info_lines.append(
                                f"Node.js requirement (latest): {node_range}")

                        # Show last few versions
                        recent = versions[-5:] if len(
                            versions) > 5 else versions
                        info_lines.append(
                            f"\nRecent versions: {', '.join(reversed(recent))}")

                except Exception as e:
                    info_lines.append(
                        f"\nError fetching registry info: {str(e)}")
            else:
                info_lines.append(
                    "\nnpm_lookup is disabled. Skipping npm registry information.")

            return "\n".join(info_lines) if info_lines else f"No information found for '{package_name}'"

        except Exception as e:
            return f"Error getting package info: {str(e)}"

    def get_tools(self) -> list[StructuredTool]:
        """Get list of all available tools."""
        return [
            StructuredTool(
                name="analyze_packages",
                func=self.analyze_packages,
                description="Analyze npm package dependencies and suggest updates for compatibility and security",
                args_schema=AnalyzePackagesInput
            ),
            StructuredTool(
                name="update_packages",
                func=self.update_packages,
                description="Update npm package dependencies in package.json with compatible and non-vulnerable versions",
                args_schema=UpdatePackagesInput
            ),
            StructuredTool(
                name="audit_packages",
                func=self.audit_packages,
                description="Audit npm package dependencies for known vulnerabilities using npm audit",
                args_schema=AuditPackagesInput
            ),
            StructuredTool(
                name="add_package",
                func=self.add_package,
                description="Add a new npm package to package.json with automatic version resolution",
                args_schema=AddPackageInput
            ),
            StructuredTool(
                name="remove_package",
                func=self.remove_package,
                description="Remove an npm package from package.json",
                args_schema=RemovePackageInput
            ),
            StructuredTool(
                name="update_specific_packages",
                func=self.update_specific_packages,
                description="Update specific npm packages by name to their latest compatible versions",
                args_schema=UpdateSpecificPackagesInput
            ),
            StructuredTool(
                name="get_package_info",
                func=self.get_package_info,
                description="Get detailed information about a specific npm package including current and available versions",
                args_schema=GetPackageInfoInput
            )
        ]
