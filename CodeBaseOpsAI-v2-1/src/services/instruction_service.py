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

    def __init__(self, repository: str, clone_path: str, branch: str, node_lts_version: str = "18.0.0"):
        """
        Initialize instruction service

        Args:
            repository: GitHub repository identifier
            clone_path: Local path where repository will be cloned
            branch: Branch name to work with
            node_lts_version: Node.js LTS version to use for package compatibility checks
        """
        self.repository = repository
        self.clone_path = clone_path
        self.branch = branch
        self.node_lts_version = node_lts_version
        self.serverless_plugins = [
            {"name": "serverless-webpack", "is_dev": False, "npm_lookup": True},
            {"name": "serverless-plugin-datadog",
                "is_dev": False, "npm_lookup": True},
            {"name": "serverless-prune-plugin",
                "is_dev": False, "npm_lookup": True},
        ]
        self.node_packages = self.serverless_plugins + [
            {"name": "@babel/core", "is_dev": True, "npm_lookup": True},
            {"name": "@babel/preset-env", "is_dev": True, "npm_lookup": True},
            {"name": "@babel/preset-typescript",
                "is_dev": True, "npm_lookup": True},
            {"name": "@types/aws-lambda", "is_dev": True, "npm_lookup": True},
            {"name": "@types/aws-sdk", "is_dev": True, "npm_lookup": True},
            {"name": "@types/jest", "is_dev": True, "npm_lookup": True},
            {"name": "@types/node", "is_dev": True, "npm_lookup": True},
            {"name": "@types/node-fetch", "is_dev": True, "npm_lookup": True},
            {"name": "apollo-boost", "is_dev": True, "npm_lookup": True},
            {"name": "aws-lambda", "is_dev": True, "npm_lookup": True},
            {"name": "axios", "is_dev": True, "npm_lookup": True},
            {"name": "babel-jest", "is_dev": True, "npm_lookup": True},
            {"name": "graphql", "is_dev": True, "npm_lookup": True},
            {"name": "jest", "is_dev": True, "npm_lookup": True},
            {"name": "jest-html-reporters", "is_dev": True, "npm_lookup": True},
            {"name": "moment", "is_dev": True, "npm_lookup": True},
            {"name": "moment-timezone", "is_dev": True, "npm_lookup": True},
            {"name": "rimraf", "is_dev": True, "npm_lookup": True},
            {"name": "serverless", "is_dev": True, "npm_lookup": True},
            {"name": "serverless-plugin-datadog",
                "is_dev": True, "npm_lookup": True},
            {"name": "serverless-webpack", "is_dev": True, "npm_lookup": True},
            {"name": "ts-jest", "is_dev": True, "npm_lookup": True},
            {"name": "ts-node", "is_dev": True, "npm_lookup": True},
            {"name": "typescript", "is_dev": True, "npm_lookup": True},
            {"name": "webpack", "is_dev": True, "npm_lookup": True},
            {"name": "webpack-node-externals", "version": "^3.0.0",
                "is_dev": True, "npm_lookup": True},
            {"name": "@tmna-devops/naqp-shared-lib",
                "version": "^3.1.2", "is_dev": False, "npm_lookup": False},
            {"name": "aws-sdk", "version": "^2.1012.0",
                "is_dev": False, "npm_lookup": True},
            {"name": "lodash", "version": "^4.17.21",
                "is_dev": False, "npm_lookup": True},
            {"name": "moment", "version": "^2.29.1",
                "is_dev": False, "npm_lookup": True},
            {"name": "node-fetch", "version": "^2.6.1",
                "is_dev": False, "npm_lookup": True},
            {"name": "uuid", "version": "^9.0.0",
                "is_dev": False, "npm_lookup": True}
        ]

    def get_all_instructions(self) -> List[str]:
        """
        Get all agent instructions in sequence

        Returns:
            List of instruction strings
        """
        instructions = []

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

        # Node.js package instructions
        nodejs = NodeJsPackagesInstructions(
            clone_path=self.clone_path,
            packages=self.node_packages,
            node_lts_version=self.node_lts_version
        )
        instructions.extend(nodejs.get_instructions())

        return instructions
