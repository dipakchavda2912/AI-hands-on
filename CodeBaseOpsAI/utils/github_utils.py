# utils/github_utils.py
import base64
import logging
import os
from pathlib import Path
from typing import List, Tuple, Optional, Set

from github import Github

from config import CONSTANTS
from .file_utils import FileUtils

logger = logging.getLogger(__name__)


class GithubUtils:
    """
    Helper to fetch files from a GitHub repository using PyGithub.

    Public API:
      - read_repo(repository: str, branch_name: Optional[str] = None) -> None
      - ingest() -> tuple[tuple[str, str, str], ...]
      - repo, branch, tree, github, files (read-only properties)
    """

    def __init__(self, token: Optional[str] = None) -> None:
        logger.info("Init Github Utils")

        token = token or os.getenv("GITHUB_TOKEN")
        if not token:
            raise ValueError("GITHUB_TOKEN environment variable not set")
        self._fileUtils = FileUtils()
        self._github: Github = Github(token)
        self._repo = None
        self._branch = None
        self._tree = None
        self._files: List[Tuple[str, str, str]] = []  # (path, content, sha)
        self._chunks: List[str] = []

    # ----- Read-only properties (public surface) -----
    @property
    def github(self) -> Github:
        """PyGithub client instance (read-only)."""
        return self._github

    @property
    def repo(self):
        """Loaded repository object (read-only)."""
        return self._repo

    @property
    def branch(self):
        """Loaded branch object (read-only)."""
        return self._branch

    @property
    def tree(self):
        """Loaded git tree (read-only)."""
        return self._tree

    @property
    def files(self) -> Tuple[Tuple[str, str, str], ...]:
        """
        Immutable view of collected files.
        Each entry is (path, utf8_content, blob_sha).
        """
        return tuple(self._files)

    @property
    def chunks(self):
        """Public read-only access to all collected chunks."""
        return self._chunks

    # === MAIN PIPELINE STEPS (ordered by scope and index) ===
    def read_repo(self, repository: str, branch_name: Optional[str] = None) -> None:
        # Step 1: Load a repository and its branch, and build the git tree.
        """
        Load a repository and its branch, and build the git tree.

        :param repository: "owner/repo" (e.g., "dipakchavda2912/ai-walk")
        :param branch_name: branch name; defaults to CONSTANTS["GITHUB"]["BRANCH"]
        """
        branch_name = branch_name or CONSTANTS["GITHUB"]["BRANCH"]

        logger.info("Loading repo %s @ %s", repository, branch_name)
        self._repo = self.github.get_repo(repository)
        self._branch = self._repo.get_branch(branch_name)
        self._tree = self._repo.get_git_tree(
            self._branch.commit.sha, recursive=True
        ).tree

    def ingest(self) -> Tuple[Tuple[str, str, str], ...]:
        # Step 2: Walk the tree and collect files matching allowed extensions.
        """
        Walk the tree and collect files matching allowed extensions.
        :return: Tuple of (path, content, sha)
        """
        if not self._repo or not self._tree:
            raise RuntimeError("Repository not loaded. Call read_repo() first.")

        for item in self._tree:
            self.filter_and_collect(item)

        return self.files

    def filter_and_collect(self, item) -> None:
        # Step 2.1: Filter and collect a single file/blob if allowed.
        """
        Collect a blob if its extension is allowed.
        Non-blob items (trees, commits) are ignored.
        """
        if item.type != "blob":
            return

        ext = Path(item.path).suffix  # e.g., ".py"
        allowed = self._allowed_extensions()

        if "*" in allowed or ext in allowed:
            blob = self._repo.get_git_blob(item.sha)
            data = base64.b64decode(blob.content).decode("utf-8", errors="ignore")
            self._add_file(item.path, data, item.sha)
            self._chunks.extend(self._fileUtils.make_document_chunks(data))

    @staticmethod
    def _allowed_extensions() -> Set[str]:
        # Step 2.2: Get allowed file extensions for filtering.
        """
        _Return the allowed extensions set.
        Defaults to {"*"} meaning allow all, and normalizes entries to start with '.'.
        """
        exts = CONSTANTS["GITHUB"].get("ALLOWED_EXTENSIONS", {"*"})
        normalized = set()
        for e in exts:
            if e == "*":
                normalized.add("*")
            else:
                normalized.add(e if e.startswith(".") else f".{e}")
        return normalized

    def _add_file(self, path: str, content: str, sha: str) -> None:
        # Step 2.3: Add a collected file to the internal list.
        """Internal helper to append a collected file."""
        self._files.append((path, content, sha))
