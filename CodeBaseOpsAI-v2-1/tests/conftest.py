"""
Test configuration and fixtures for CodeBaseOpsAI tests.
"""
import pytest
import tempfile
import os
from pathlib import Path


@pytest.fixture
def temp_yaml_file():
    """Create a temporary YAML file for testing."""
    content = """service: my-service
provider:
  name: aws
  runtime: python3.9
functions:
  hello:
    handler: handler.hello
    timeout: 30
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        f.write(content)
        temp_path = f.name

    yield temp_path

    # Cleanup
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture
def temp_yaml_with_custom_string():
    """Create a temporary YAML file with custom as a string."""
    content = """service: my-service
provider:
  name: aws
custom: '{}'
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        f.write(content)
        temp_path = f.name

    yield temp_path

    # Cleanup
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture
def temp_directory():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def sample_repo_url():
    """Provide a small public repository URL for testing."""
    return "octocat/Hello-World"
