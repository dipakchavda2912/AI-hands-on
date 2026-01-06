import os
import shutil
import subprocess
from typing import Tuple, Optional
from github import Github
from github.Repository import Repository


class GithubUtils:
    """Utility functions for GitHub operations."""

    @staticmethod
    def get_repo_info(github_client: Github, repository: str, branch: str = "main") -> Tuple[list, Optional[Exception]]:
        """Get repository information from GitHub API.

        Args:
            github_client: Authenticated GitHub client
            repository: Repository name in format 'owner/repo'
            branch: Branch name

        Returns:
            Tuple of (info_list, error)
        """
        try:
            repo = github_client.get_repo(repository)

            info = [
                f"Repository: {repo.full_name}",
                f"Description: {repo.description}",
                f"Stars: {repo.stargazers_count}",
                f"Language: {repo.language}",
                f"Default Branch: {repo.default_branch}",
                f"Open Issues: {repo.open_issues_count}",
                "\nRecent files in root:",
            ]

            # List files in root directory
            contents = repo.get_contents("", ref=branch)
            for content in contents[:10]:  # Limit to first 10 items
                info.append(f"  - {content.path} ({content.type})")

            return info, None
        except Exception as e:
            return [], e

    @staticmethod
    def convert_repo_to_url(repository: str) -> str:
        """Convert repository name to full GitHub URL.

        Args:
            repository: Repository name in format 'owner/repo' or full URL

        Returns:
            Full GitHub URL
        """
        if not repository.startswith("http"):
            return f"https://github.com/{repository}.git"
        return repository

    @staticmethod
    def remove_directory(path: str) -> None:
        """Remove a directory if it exists.

        Args:
            path: Directory path to remove
        """
        if os.path.exists(path):
            shutil.rmtree(path)

    @staticmethod
    def clone_repo(repository_url: str, clone_path: str, timeout: int = 60) -> Tuple[bool, str]:
        """Clone a Git repository.

        Args:
            repository_url: Full repository URL
            clone_path: Local path to clone to
            timeout: Timeout in seconds

        Returns:
            Tuple of (success, message)
        """
        try:
            result = subprocess.run(
                ["git", "clone", repository_url, clone_path],
                capture_output=True,
                text=True,
                timeout=timeout
            )

            if result.returncode == 0:
                return True, ""
            else:
                return False, result.stderr

        except subprocess.TimeoutExpired:
            return False, f"Clone operation timed out ({timeout}s limit)"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def count_files_in_directory(path: str) -> int:
        """Count all files in a directory recursively.

        Args:
            path: Directory path

        Returns:
            Total number of files
        """
        return sum([len(files) for _, _, files in os.walk(path)])

    @staticmethod
    def checkout_branch_cmd(repo_path: str, branch: str, timeout: int = 30) -> Tuple[bool, str]:
        """Checkout a branch in a Git repository.

        Args:
            repo_path: Local repository path
            branch: Branch name to checkout
            timeout: Timeout in seconds

        Returns:
            Tuple of (success, message)
        """
        try:
            result = subprocess.run(
                ["git", "checkout", branch],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=timeout
            )

            if result.returncode == 0:
                return True, ""
            else:
                return False, result.stderr

        except subprocess.TimeoutExpired:
            return False, f"Checkout operation timed out ({timeout}s limit)"
        except Exception as e:
            return False, str(e)
