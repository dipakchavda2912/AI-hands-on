"""
GitHub tools for repository operations.

Simple tools using the @tool decorator for easy integration with LangChain agents.
"""

from langchain_core.tools import tool


class GithubTools:
    """Collection of GitHub operation tools."""

    def __init__(self):
        """Initialize GitHub tools."""
        pass

    @staticmethod
    @tool
    def read_repository(repository: str, branch: str = "main") -> str:
        """
        Read a GitHub repository and analyze its files.

        Args:
            repository: GitHub repository in format 'owner/repo'
            branch: Branch name to read from (default: 'main')

        Returns:
            JSON string with repository analysis
        """
        # Mock implementation for demonstration
        return f"""{{
            "repository": "{repository}",
            "branch": "{branch}",
            "files": [
                {{"file": "README.md", "content": "# Example Repository", "sha": "abc123"}},
                {{"file": "package.json", "content": "{{\\"name\\": \\"example\\"}}", "sha": "def456"}}
            ],
            "status": "success",
            "message": "Repository analyzed successfully"
        }}"""

    @staticmethod
    @tool
    def clone_repository(repository: str, clone_path: str = "/tmp/repo") -> str:
        """
        Clone a GitHub repository to local filesystem.

        Args:
            repository: GitHub repository in format 'owner/repo'
            clone_path: Local path to clone repository

        Returns:
            Status message with clone details
        """
        # Mock implementation for demonstration
        return f"""{{
            "repository": "{repository}",
            "clone_path": "{clone_path}",
            "status": "success",
            "message": "Repository cloned successfully to {clone_path}"
        }}"""

    def get_tools(self):
        """Get list of all available tools."""
        return [
            self.read_repository,
            self.clone_repository
        ]
