import os
from langchain_core.tools import StructuredTool
from github import Github
from pydantic import BaseModel, Field
from ..utils import GithubUtils


class GithubTools:
    def __init__(self, github_token: str = None) -> None:
        """Initialize GitHub tools."""
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")
        self.github = Github(self.github_token) if self.github_token else None

    def read_repository(self, repository: str, branch: str = "main") -> str:
        """Read a GitHub repository and analyze its files.

        Args:
            repository: Repository name in format 'owner/repo'
            branch: Branch name (default: 'main')

        Returns:
            String containing repository information
        """
        if not self.github:
            return "Error: GitHub token not configured. Set GITHUB_TOKEN environment variable."

        info_list, error = GithubUtils.get_repo_info(
            self.github, repository, branch)

        if error:
            return f"Error reading repository: {str(error)}"

        return "\n".join(info_list)

    def clone_repository(self, repository: str, clone_path: str = "/tmp/repo") -> str:
        """Clone a GitHub repository to local filesystem.

        Args:
            repository: Repository URL or name in format 'owner/repo'
            clone_path: Local path to clone to (default: '/tmp/repo')

        Returns:
            String with clone status
        """
        # Convert owner/repo to full URL if needed
        repository_url = GithubUtils.convert_repo_to_url(repository)

        # Remove existing directory if it exists
        GithubUtils.remove_directory(clone_path)

        # Clone the repository
        success, error_msg = GithubUtils.clone_repo(repository_url, clone_path)

        if success:
            file_count = GithubUtils.count_files_in_directory(clone_path)
            return f"Successfully cloned repository to {clone_path}. Found {file_count} files."
        else:
            return f"Error cloning repository: {error_msg}"

    def checkout_branch(self, repo_path: str, branch: str) -> str:
        """Checkout a specific branch in the cloned repository.

        Args:
            repo_path: Local path of the cloned repository
            branch: Branch name to checkout

        Returns:
            String with checkout status
        """
        success, error_msg = GithubUtils.checkout_branch_cmd(repo_path, branch)

        if success:
            return f"Successfully checked out branch '{branch}' in {repo_path}."
        else:
            return f"Error checking out branch: {error_msg}"

    def get_tools(self) -> list[StructuredTool]:
        """Get list of all available tools."""

        # Define input schemas
        class ReadRepoInput(BaseModel):
            repository: str = Field(
                description="Repository name in format 'owner/repo'")
            branch: str = Field(default="main", description="Branch name")

        class CloneRepoInput(BaseModel):
            repository: str = Field(
                description="Repository URL or name in format 'owner/repo'")
            clone_path: str = Field(
                default="/tmp/repo", description="Local path to clone to")

        class CheckoutBranchInput(BaseModel):
            repo_path: str = Field(
                description="Local path of the cloned repository")
            branch: str = Field(description="Branch name to checkout")

        return [
            StructuredTool(
                name="read_repository",
                func=self.read_repository,
                description="Read a GitHub repository and analyze its files",
                args_schema=ReadRepoInput
            ),
            StructuredTool(
                name="clone_repository",
                func=self.clone_repository,
                description="Clone a GitHub repository to local filesystem",
                args_schema=CloneRepoInput
            ),
            StructuredTool(
                name="checkout_branch",
                func=self.checkout_branch,
                description="Checkout a specific branch in the cloned repository",
                args_schema=CheckoutBranchInput
            )
        ]
