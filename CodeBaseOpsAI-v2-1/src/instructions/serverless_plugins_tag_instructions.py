"""
Serverless provider section instructions
"""

from typing import List, Optional


class ServerlessPluginsTagInstructions:
    """Instructions for serverless.yml plugins section attributes"""

    def __init__(self, *, clone_path: Optional[str] = None, serverless_plugins: Optional[list] = None, package_name: Optional[str] = None, is_dev: bool = False):
        """Initialize with configuration"""
        self.clone_path = clone_path
        self.serverless_plugins = serverless_plugins
        self.package_name = package_name
        self.is_dev = is_dev

    def get_instructions(self) -> List[str]:
        """Get all serverless plugins section instructions
        Args:
            self.clone_path: Local path where repository is cloned

        Returns:
            List of serverless plugins configuration instruction strings
        """
        return [
            self.get_plugins_instructions(),
        ]

    def get_plugins_instructions(self) -> str:
        """Get instruction to add stack tags in plugins section"""
        # Extract plugin names from the list of dictionaries
        plugin_names = [pkg["name"] for pkg in (self.serverless_plugins or [])]

        return f"""
            Add the following values for plugins attributes
            of the {self.clone_path}serverless.yml file.
            plugins:
            Attribute should be added as a list by following serverless syntax and include the following plugins:
            {', '.join(plugin_names)}
            """
