"""
Unit tests for GitHub Tools.

Run with: pytest tests/test_github_tools.py -v
"""

import pytest
from tools.github_tools import GithubTools, ReadRepositoryInput, CloneRepositoryInput
from pydantic import ValidationError


def test_github_tools_initialization():
    """Test GithubTools initializes correctly."""
    tools = GithubTools()
    assert tools is not None


def test_get_tools_returns_list():
    """Test get_tools returns a list of tools."""
    tools = GithubTools()
    tool_list = tools.get_tools()

    assert isinstance(tool_list, list)
    assert len(tool_list) > 0


def test_read_repository_input_validation():
    """Test ReadRepositoryInput validates correctly."""
    # Valid input
    valid_input = ReadRepositoryInput(
        repository="owner/repo",
        branch="main"
    )
    assert valid_input.repository == "owner/repo"
    assert valid_input.branch == "main"

    # URL parsing
    url_input = ReadRepositoryInput(
        repository="https://github.com/owner/repo",
        branch="develop"
    )
    assert url_input.repository == "owner/repo"


def test_clone_repository_input_validation():
    """Test CloneRepositoryInput validates correctly."""
    valid_input = CloneRepositoryInput(
        repository="owner/repo",
        clone_path="/tmp/test"
    )
    assert valid_input.repository == "owner/repo"
    assert valid_input.clone_path == "/tmp/test"


def test_tools_have_correct_names():
    """Test tools have expected names."""
    tools = GithubTools().get_tools()
    tool_names = [tool.name for tool in tools]

    assert "read_repository" in tool_names
    assert "clone_repository" in tool_names
