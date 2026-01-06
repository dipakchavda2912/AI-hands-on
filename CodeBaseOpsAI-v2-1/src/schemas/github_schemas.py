"""
Pydantic schemas for GitHub tool input validation.
"""

from pydantic import BaseModel, Field


class ReadRepoInput(BaseModel):
    """Input schema for reading a GitHub repository."""
    repository: str = Field(
        description="Repository name in format 'owner/repo'")
    branch: str = Field(
        default="main",
        description="Branch name")


class CloneRepoInput(BaseModel):
    """Input schema for cloning a GitHub repository."""
    repository: str = Field(
        description="Repository URL or name in format 'owner/repo'")
    clone_path: str = Field(
        default="/tmp/repo",
        description="Local path to clone to")


class CheckoutBranchInput(BaseModel):
    """Input schema for checking out a branch."""
    repo_path: str = Field(
        description="Local path of the cloned repository")
    branch: str = Field(
        description="Branch name to checkout")


class ListRepoFilesInput(BaseModel):
    """Input schema for listing files in a repository."""
    repo_path: str = Field(
        description="Local path of the cloned repository")
