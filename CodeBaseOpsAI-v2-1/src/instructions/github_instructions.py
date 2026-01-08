"""
GitHub operation instructions
"""

from typing import List, Optional


class GithubInstructions:
    """Instructions for GitHub repository operations"""

    def __init__(self, *, repository: Optional[str] = None, clone_path: Optional[str] = None, branch: Optional[str] = None):
        """Initialize GitHub instructions with configuration

        Args:
            repository: GitHub repository identifier (e.g., 'owner/repo')
            clone_path: Local path where repository will be cloned
            branch: Branch name to work with
        """
        self.repository = repository
        self.clone_path = clone_path
        self.branch = branch

    def get_instructions(self) -> List[str]:
        """Get all GitHub operation instructions

        Returns:
            List of GitHub operation instruction strings
        """
        return [
            self.get_read_repository_instruction(),
            self.get_clone_repository_instruction(),
            self.get_checkout_branch_instruction(),
            self.get_list_files_instruction(),
        ]

    def get_read_repository_instruction(self) -> str:
        """Get instruction to read a repository"""
        return f"Read the repository '{self.repository}' on branch '{self.branch}'."

    def get_clone_repository_instruction(self) -> str:
        """Get instruction to clone a repository"""
        return f"Clone the repository '{self.repository}' to local filesystem at {self.clone_path}"

    def get_checkout_branch_instruction(self) -> str:
        """Get instruction to checkout a branch"""
        return f"Checkout the '{self.branch}' branch in the cloned repository at {self.clone_path}."

    def get_list_files_instruction(self) -> str:
        """Get instruction to list all files in the repository"""
        return f"List all the files in the cloned repository at {self.clone_path} on branch {self.branch}"
