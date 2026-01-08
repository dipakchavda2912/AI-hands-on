"""
Service for managing agent instructions
"""

from typing import List
from src.instructions.github_instructions import GithubInstructions
from src.instructions.serverless_custom_tag_instructions import ServerlessCustomTagInstructions
from src.instructions.serverless_providers_tag_instructions import ServerlessProvidersTagInstructions
from src.instructions.nodejs_packages_instructions import NodeJsPackagesInstructions
from src.instructions.serverless_plugins_tag_instructions import ServerlessPluginsTagInstructions


class InstructionService:
    """Service class for retrieving agent instructions"""

    def __init__(self, repository: str, clone_path: str, branch: str):
        """
        Initialize instruction service

        Args:
            repository: GitHub repository identifier
            clone_path: Local path where repository will be cloned
            branch: Branch name to work with
        """
        self.repository = repository
        self.clone_path = clone_path
        self.branch = branch
        self.serverless_plugins = [
            {"name": "serverless-webpack", "is_dev": False},
            {"name": "serverless-plugin-datadog", "is_dev": False},
            {"name": "serverless-prune-plugin", "is_dev": False},
        ]

    def get_all_instructions(self) -> List[str]:
        """
        Get all agent instructions in sequence

        Returns:
            List of instruction strings
        """
        instructions = []

        # # Node.js package instructions
        # nodejs = NodeJsPackagesInstructions(
        #     clone_path=self.clone_path,
        #     packages=self.serverless_plugins
        # )
        # instructions.extend(nodejs.get_instructions())

        # GitHub operations - keyword arguments, order doesn't matter
        github = GithubInstructions(
            repository=self.repository,
            clone_path=self.clone_path,
            branch=self.branch
        )
        instructions.extend(github.get_instructions())

        # Serverless custom section configuration
        serverless_custom = ServerlessCustomTagInstructions(
            clone_path=self.clone_path
        )
        instructions.extend(serverless_custom.get_instructions())

        # Serverless provider section configuration
        serverless_provider = ServerlessProvidersTagInstructions(
            clone_path=self.clone_path
        )
        instructions.extend(serverless_provider.get_instructions())

        # Serverless plugins section configuration
        serverless_plugins = ServerlessPluginsTagInstructions(
            clone_path=self.clone_path,
            serverless_plugins=self.serverless_plugins
        )
        instructions.extend(serverless_plugins.get_instructions())

        return instructions
