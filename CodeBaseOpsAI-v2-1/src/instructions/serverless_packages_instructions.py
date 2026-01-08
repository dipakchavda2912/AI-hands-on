"""
Serverless packages instructions
"""


class ServerlessPackagesInstructions:
    """Instructions for serverless.yml package configuration"""

    # @staticmethod
    # def get_add_package_configuration_instruction(clone_path: str) -> str:
    #     """Get instruction to configure package settings"""
    #     return f"""
    #         Add package configuration under the root level in the {clone_path}serverless.yml file.
    #         Configure the following settings:
    #         individually should be true for individual Lambda packaging
    #         patterns should exclude development and build artifacts
    #         Include common patterns like excluding node_modules, .git, tests, and documentation files.
    #         """

    # @staticmethod
    # def get_add_package_excludes_instruction(clone_path: str) -> str:
    #     """Get instruction to add package exclusion patterns"""
    #     return f"""
    #         Add exclusion patterns to the package section in the {clone_path}serverless.yml file.
    #         Exclude the following patterns:
    #         - node_modules/**
    #         - .git/**
    #         - tests/**
    #         - *.md
    #         - .env*
    #         Values should be in YAML array format.
    #         """
