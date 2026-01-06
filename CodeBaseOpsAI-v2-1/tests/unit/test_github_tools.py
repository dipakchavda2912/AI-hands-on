"""
Unit tests for GitHub tools (LangChain wrappers).
"""
import pytest
from src.tools.github_tools import GithubTools


class TestGithubTools:
    """Test suite for GithubTools class."""

    def test_read_repository_without_token(self, monkeypatch):
        """Test reading repository without GitHub token."""
        monkeypatch.delenv('GITHUB_TOKEN', raising=False)

        result = GithubTools.read_repository('octocat/Hello-World')

        assert 'error' in result.lower() or 'token' in result.lower()

    def test_read_repository_invalid_format(self, monkeypatch):
        """Test reading repository with invalid format."""
        monkeypatch.setenv('GITHUB_TOKEN', 'fake_token')

        result = GithubTools.read_repository('invalid-repo-format')

        # Should handle error gracefully
        assert isinstance(result, str)

    def test_clone_repository_missing_params(self):
        """Test cloning repository with missing parameters."""
        result = GithubTools.clone_repository('', '')

        assert 'error' in result.lower() or 'required' in result.lower()

    def test_checkout_branch_missing_params(self):
        """Test checkout branch with missing parameters."""
        result = GithubTools.checkout_branch('', '')

        assert 'error' in result.lower() or 'required' in result.lower()

    def test_list_files_nonexistent_directory(self):
        """Test listing files in non-existent directory."""
        result = GithubTools.list_files('/nonexistent/directory')

        assert 'error' in result.lower() or '0' in result
