"""
Node.js packages instructions
"""


class NodeJsPackagesInstructions:
    """Instructions for Node.js package.json operations"""

    @staticmethod
    def get_read_package_json_instruction(clone_path: str) -> str:
        """Get instruction to read package.json"""
        return f"Read the {clone_path}package.json file and parse its contents."

    @staticmethod
    def get_update_package_version_instruction(clone_path: str, version: str) -> str:
        """Get instruction to update package version"""
        return f"Update the version field in {clone_path}package.json to {version}."

    @staticmethod
    def get_add_npm_script_instruction(clone_path: str, script_name: str, script_command: str) -> str:
        """Get instruction to add an npm script"""
        return f"""Add a new script '{script_name}' with command '{script_command}' to the scripts section in {clone_path}package.json file."""

    @staticmethod
    def get_install_dependency_instruction(clone_path: str, package_name: str, is_dev: bool = False) -> str:
        """Get instruction to install a dependency"""
        dep_type = "devDependencies" if is_dev else "dependencies"
        return f"""Add '{package_name}' to {dep_type} in {clone_path}package.json file."""

    @staticmethod
    def get_update_package_metadata_instruction(clone_path: str, field: str, value: str) -> str:
        """Get instruction to update package.json metadata"""
        return f"""Update the '{field}' field in {clone_path}package.json to '{value}'."""
