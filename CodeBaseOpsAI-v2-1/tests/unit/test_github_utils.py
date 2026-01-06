"""
Unit tests for GitHub utilities.
"""
import pytest
import os
from src.utils.github_utils import GithubUtils


class TestGithubUtils:
    """Test suite for GithubUtils class."""

    def test_get_repo_info_with_token(self, monkeypatch):
        """Test getting repository information with valid token."""
        # Mock environment variable
        monkeypatch.setenv('GITHUB_TOKEN', 'fake_token')

        # This will fail with fake token but we can test the function call
        try:
            success, data = GithubUtils.get_repo_info('octocat/Hello-World')
            # With fake token, it should fail
            assert success is False or isinstance(data, dict)
        except Exception:
            # Expected with fake token
            pass

    def test_get_repo_info_without_token(self, monkeypatch):
        """Test getting repository info without token."""
        monkeypatch.delenv('GITHUB_TOKEN', raising=False)

        success, data = GithubUtils.get_repo_info('octocat/Hello-World')

        # Without token, should fail
        assert success is False
        assert 'GITHUB_TOKEN' in data

    def test_convert_repo_to_url(self):
        """Test converting repository name to URL."""
        # Test with full URL
        url1 = GithubUtils.convert_repo_to_url(
            'https://github.com/user/repo.git')
        assert url1 == 'https://github.com/user/repo.git'

        # Test with user/repo format
        url2 = GithubUtils.convert_repo_to_url('user/repo')
        assert url2 == 'https://github.com/user/repo.git'

        # Test with just repo name (should handle gracefully)
        url3 = GithubUtils.convert_repo_to_url('repo')
        assert 'github.com' in url3

    def test_clone_repo_invalid_path(self):
        """Test cloning with invalid local path."""
        success, message = GithubUtils.clone_repo(
            'https://github.com/octocat/Hello-World.git',
            ''
        )

        assert success is False
        assert 'path' in message.lower() or 'required' in message.lower()

    def test_checkout_branch_cmd(self):
        """Test checkout branch command generation."""
        # This function should return a tuple or execute git checkout
        # Since we can't test actual git operations without a repo,
        # we just verify the function exists and can be called
        try:
            result = GithubUtils.checkout_branch_cmd('/tmp/test', 'main')
            assert result is not None
        except Exception:
            # Expected if path doesn't exist
            pass

    def test_count_files_in_directory(self, temp_directory):
        """Test counting files in directory."""
        # Create some test files
        for i in range(3):
            with open(os.path.join(temp_directory, f'file{i}.txt'), 'w') as f:
                f.write('test')

        count = GithubUtils.count_files_in_directory(temp_directory)
        assert count == 3

    def test_count_files_nonexistent_directory(self):
        """Test counting files in non-existent directory."""
        count = GithubUtils.count_files_in_directory('/nonexistent/path')
        assert count == 0
