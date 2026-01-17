"""
Node.js packages instructions
"""

from typing import List, Optional


class NodeJsPackagesInstructions:
    """Instructions for Node.js package.json operations"""

    def __init__(self, *, clone_path: Optional[str] = None, packages: Optional[List[dict[str, bool | str]]] = None, is_dev: bool = False, npm_lookup: bool = True):
        """Initialize with configuration

        Args:
            clone_path: Local path where repository is cloned
            packages: List of package dictionaries with 'name' and 'is_dev' keys
            is_dev: Default value for is_dev if not specified in package dict
        """
        self.clone_path = clone_path
        self.packages = packages or []
        self.is_dev = is_dev
        self.npm_lookup = npm_lookup

    def get_instructions(self) -> List[str]:
        """Get all Node.js package instructions

        Returns:
            List of Node.js package configuration instruction strings
        """
        instructions = []

        # Add package installation instructions
        add_instructions = self.add_packages()
        if add_instructions:
            instructions.extend(add_instructions)

        return instructions

    def add_single_package(self, package_name: str, is_dev: bool = False, npm_lookup: bool = True) -> str:
        """Get instruction to install a single dependency

        Args:
            package_name: Name of the npm package to add
            is_dev: Whether package is a dev dependency
            npm_lookup: Whether to look up the package on npm

        Returns:
            Instruction string for adding the package
        """
        dep_type = "devDependencies" if is_dev else "dependencies"
        return f"""Add '{package_name}' to {dep_type} in {self.clone_path}package.json file. Use semantic versioning format (e.g., ^1.2.3 with major.minor.patch)."""

    def add_packages(self) -> List[str]:
        """Get instructions to install multiple dependencies

        Returns:
            List of instruction strings for all packages
        """
        # Use provided packages or default packages
        # packages_to_install = self.packages if self.packages else [
        #     {"name": "serverless-plugin-datadog", "is_dev": False, "npm_lookup": True},
        #     {"name": "serverless-prune-plugin", "is_dev": False, "npm_lookup": True},
        # ]

        # Generate instruction for each package using a loop
        instructions = []
        for pkg in self.packages:
            package_name = str(pkg.get("name", ""))
            is_dev_value = pkg.get("is_dev", False)
            npm_lookup_value = pkg.get("npm_lookup", True)
            is_dev = bool(is_dev_value) if is_dev_value is not None else False
            npm_lookup = bool(
                npm_lookup_value) if npm_lookup_value is not None else True

            if package_name:  # Only add if package name is not empty
                instructions.append(
                    self.add_single_package(package_name, is_dev, npm_lookup))

        return instructions

    def update_single_package(self, package_name: str, version: Optional[str] = None) -> str:
        """Get instruction to update a single package

        Args:
            package_name: Name of the npm package to update
            version: Specific version to update to (optional, uses latest if not provided)

        Returns:
            Instruction string for updating the package
        """
        if version:
            return f"""Update '{package_name}' to version '{version}' in {self.clone_path}package.json file. Use semantic versioning format (major.minor.patch)."""
        return f"""Update '{package_name}' to the latest compatible and secure version in {self.clone_path}package.json file. Use semantic versioning format (e.g., ^1.2.3 with major.minor.patch)."""

    def update_packages_list(self, package_names: List[str]) -> List[str]:
        """Get instructions to update multiple specific packages

        Args:
            package_names: List of package names to update

        Returns:
            List of instruction strings for updating packages
        """
        instructions = []
        for package_name in package_names:
            if package_name:
                instructions.append(self.update_single_package(package_name))
        return instructions

    def update_all_packages(self, lock_major: bool = True) -> str:
        """Get instruction to update all packages

        Args:
            lock_major: Whether to lock major version updates

        Returns:
            Instruction string for updating all packages
        """
        lock_msg = " while maintaining current major versions" if lock_major else ""
        return f"""Update all npm packages in {self.clone_path}package.json to their latest compatible and non-vulnerable versions{lock_msg}."""

    def remove_package(self, package_name: str) -> str:
        """Get instruction to remove a package

        Args:
            package_name: Name of the npm package to remove

        Returns:
            Instruction string for removing the package
        """
        return f"""Remove '{package_name}' from {self.clone_path}package.json file."""

    def remove_packages_list(self, package_names: List[str]) -> List[str]:
        """Get instructions to remove multiple packages

        Args:
            package_names: List of package names to remove

        Returns:
            List of instruction strings for removing packages
        """
        instructions = []
        for package_name in package_names:
            if package_name:
                instructions.append(self.remove_package(package_name))
        return instructions

    def analyze_packages(self, lock_major: bool = True) -> str:
        """Get instruction to analyze packages for updates

        Args:
            lock_major: Whether to lock major version updates in analysis

        Returns:
            Instruction string for analyzing packages
        """
        return f"""Analyze all npm packages in {self.clone_path}package.json and report which packages can be safely updated to newer versions."""

    def audit_packages(self, min_severity: Optional[str] = None) -> str:
        """Get instruction to audit packages for vulnerabilities

        Args:
            min_severity: Minimum severity level to report (low, moderate, high, critical)

        Returns:
            Instruction string for auditing packages
        """
        severity_msg = f" with minimum severity level '{min_severity}'" if min_severity else ""
        return f"""Run security audit on all npm packages in {self.clone_path}package.json{severity_msg} and report any vulnerabilities found."""

    def get_package_info(self, package_name: str) -> str:
        """Get instruction to retrieve package information

        Args:
            package_name: Name of the npm package

        Returns:
            Instruction string for getting package information
        """
        return f"""Get detailed information about the npm package '{package_name}', including current version in {self.clone_path}package.json and latest available version."""
