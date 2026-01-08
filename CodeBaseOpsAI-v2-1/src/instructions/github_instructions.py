"""
GitHub operation instructions
"""


class GithubInstructions:
    """Instructions for GitHub repository operations"""

    @staticmethod
    def get_read_repository_instruction(repository: str, branch: str) -> str:
        """Get instruction to read a repository"""
        return f"Read the repository '{repository}' on branch '{branch}'."

    @staticmethod
    def get_clone_repository_instruction(repository: str, clone_path: str) -> str:
        """Get instruction to clone a repository"""
        return f"Clone the repository '{repository}' to local filesystem at {clone_path}"

    @staticmethod
    def get_checkout_branch_instruction(clone_path: str, branch: str) -> str:
        """Get instruction to checkout a branch"""
        return f"Checkout the '{branch}' branch in the cloned repository at {clone_path}."

    @staticmethod
    def get_list_files_instruction(clone_path: str, branch: str) -> str:
        """Get instruction to list all files in the repository"""
        return f"List all the files in the cloned repository at {clone_path} on branch {branch}"
