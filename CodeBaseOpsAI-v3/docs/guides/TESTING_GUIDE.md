# Testing Guide

Comprehensive guide to testing AI agents, tools, and production applications with CodeBaseOpsAI-v3.

---

## Table of Contents

1. [Testing Philosophy](#testing-philosophy)
2. [Test Setup](#test-setup)
3. [Unit Testing](#unit-testing)
4. [Integration Testing](#integration-testing)
5. [Testing Async Code](#testing-async-code)
6. [Mocking and Fixtures](#mocking-and-fixtures)
7. [Testing Agents](#testing-agents)
8. [Testing Tools](#testing-tools)
9. [Testing APIs](#testing-apis)
10. [Test Coverage](#test-coverage)
11. [Performance Testing](#performance-testing)
12. [Best Practices](#best-practices)

---

## Testing Philosophy

### Why Test AI Applications?

**AI systems are non-deterministic**, but we can still test:

✅ **What we CAN test:**
- Tool functionality (inputs → outputs)
- Error handling
- API contracts
- Performance boundaries
- Integration points
- Configuration loading
- State management

❌ **What we CAN'T test:**
- Exact LLM responses (they vary)
- Creative outputs
- Reasoning paths (non-deterministic)

### Testing Pyramid for AI Apps

```
        /\
       /  \  E2E Tests (Few)
      /____\  - Full workflows
     /      \  - Real LLM calls
    /________\ Integration Tests (Some)
   /          \ - Agent + Tools
  /____________\ - Mock LLM
 /              \ Unit Tests (Many)
/________________\ - Individual functions
                    - Fast, isolated
```

**Strategy:**
- **Many** fast unit tests (tools, utilities)
- **Some** integration tests (agent behavior)
- **Few** end-to-end tests (critical workflows)

---

## Test Setup

### Installing Test Dependencies

```bash
# Install testing tools
pip install pytest pytest-asyncio pytest-cov pytest-mock

# Install optional tools
pip install pytest-xdist    # Parallel test execution
pip install pytest-timeout  # Timeout control
pip install pytest-html     # HTML reports
pip install faker           # Test data generation
```

### Project Test Structure

```
CodeBaseOpsAI-v3/
├── tests/
│   ├── conftest.py              # Shared fixtures
│   ├── test_github_agent.py     # Agent tests
│   ├── test_github_tools.py     # Tool tests
│   ├── test_api_integration.py  # API tests
│   ├── test_config.py           # Configuration tests
│   └── fixtures/                # Test data
│       ├── sample_repo.json
│       └── mock_responses.py
└── pytest.ini                   # pytest configuration
```

### pytest Configuration

```ini
# pytest.ini

[pytest]
# Test discovery
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Output
addopts = 
    -v                    # Verbose
    --strict-markers      # Strict marker usage
    --tb=short            # Short traceback
    --cov=agents          # Coverage for agents/
    --cov=tools           # Coverage for tools/
    --cov-report=term-missing  # Show missing lines
    --cov-report=html     # HTML coverage report

# Async support
asyncio_mode = auto

# Test markers
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: integration tests
    unit: unit tests
    requires_api: requires external API access

# Timeout (prevent hanging tests)
timeout = 30
```

---

## Unit Testing

### Testing Pure Functions

**Simple function test:**

```python
# utils/string_utils.py

def format_repository_name(owner: str, repo: str) -> str:
    """Format repository as owner/repo."""
    if not owner or not repo:
        raise ValueError("Owner and repo are required")
    return f"{owner}/{repo}"


# tests/test_string_utils.py

import pytest
from utils.string_utils import format_repository_name


def test_format_repository_name_valid():
    """Test valid repository formatting."""
    result = format_repository_name("facebook", "react")
    assert result == "facebook/react"


def test_format_repository_name_empty_owner():
    """Test error on empty owner."""
    with pytest.raises(ValueError, match="Owner and repo are required"):
        format_repository_name("", "react")


def test_format_repository_name_empty_repo():
    """Test error on empty repo."""
    with pytest.raises(ValueError, match="Owner and repo are required"):
        format_repository_name("facebook", "")


@pytest.mark.parametrize("owner,repo,expected", [
    ("facebook", "react", "facebook/react"),
    ("google", "tensorflow", "google/tensorflow"),
    ("microsoft", "vscode", "microsoft/vscode"),
])
def test_format_repository_name_multiple(owner, repo, expected):
    """Test multiple valid inputs using parametrize."""
    result = format_repository_name(owner, repo)
    assert result == expected
```

### Testing with Parametrize

**Why:** Test multiple inputs efficiently.

```python
import pytest


@pytest.mark.parametrize("input_value,expected", [
    (0, "zero"),
    (1, "one"),
    (2, "two"),
    (10, "many"),
])
def test_number_to_word(input_value, expected):
    """Test number to word conversion."""
    result = number_to_word(input_value)
    assert result == expected


# Advanced parametrize with IDs
@pytest.mark.parametrize(
    "owner,repo,branch,expected",
    [
        ("facebook", "react", "main", "facebook/react@main"),
        ("vuejs", "vue", "dev", "vuejs/vue@dev"),
    ],
    ids=["react_main", "vue_dev"]  # Test IDs for better output
)
def test_repo_with_branch(owner, repo, branch, expected):
    result = format_repo_with_branch(owner, repo, branch)
    assert result == expected
```

---

## Integration Testing

### Testing Agent with Real LLM

**When:** Testing critical workflows end-to-end.

```python
# tests/test_agent_integration.py

import pytest
from agents.github_agent import GitHubAgent


@pytest.mark.slow
@pytest.mark.requires_api
def test_agent_analyze_repository():
    """
    Test agent can analyze a real repository.
    
    Requires: GOOGLE_API_KEY environment variable
    Marked slow: Uses real API call
    """
    agent = GitHubAgent(temperature=0.0)  # Deterministic
    
    # Use small, stable repository for testing
    result = agent.run(
        query="Analyze repository octocat/Hello-World",
        thread_id="test_integration_1"
    )
    
    # Verify structure (not exact content)
    assert result['success'] is True
    assert 'output' in result
    assert len(result['output']) > 0
    assert 'execution_time' in result
    
    # Verify contains expected keywords
    output_lower = result['output'].lower()
    assert any(keyword in output_lower for keyword in [
        'repository', 'languages', 'files'
    ])


@pytest.mark.slow
@pytest.mark.requires_api
async def test_agent_conversation_context():
    """Test agent maintains conversation context."""
    agent = GitHubAgent(enable_checkpointing=True)
    thread_id = "test_conversation"
    
    # First query
    result1 = await agent.run_async(
        "Analyze repository facebook/react",
        thread_id=thread_id
    )
    assert result1['success']
    
    # Follow-up query (tests context retention)
    result2 = await agent.run_async(
        "What programming languages did you find?",
        thread_id=thread_id
    )
    assert result2['success']
    
    # Should mention languages without re-analyzing
    assert 'javascript' in result2['output'].lower() or \
           'typescript' in result2['output'].lower()
```

**Running slow tests selectively:**

```bash
# Skip slow tests (default for development)
pytest -m "not slow"

# Run only slow tests (before deployment)
pytest -m slow

# Run tests requiring API
pytest -m requires_api --api-key=$GOOGLE_API_KEY
```

---

## Testing Async Code

### Basic Async Test

```python
import pytest
import asyncio


@pytest.mark.asyncio
async def test_async_function():
    """Test async function."""
    result = await my_async_function()
    assert result is not None


@pytest.mark.asyncio
async def test_agent_run_async():
    """Test agent async execution."""
    from agents.github_agent import GitHubAgent
    
    agent = GitHubAgent()
    result = await agent.run_async("test query")
    
    assert 'success' in result
    assert 'output' in result
```

### Testing Concurrent Operations

```python
@pytest.mark.asyncio
async def test_concurrent_agent_calls():
    """Test multiple concurrent agent calls."""
    from agents.github_agent import GitHubAgent
    
    agent = GitHubAgent()
    
    # Create multiple concurrent tasks
    tasks = [
        agent.run_async(f"Query {i}", thread_id=f"thread_{i}")
        for i in range(5)
    ]
    
    # Execute concurrently
    results = await asyncio.gather(*tasks)
    
    # Verify all succeeded
    assert len(results) == 5
    assert all(r['success'] for r in results)


@pytest.mark.asyncio
async def test_streaming_events():
    """Test streaming generates events."""
    from agents.github_agent import GitHubAgent
    
    agent = GitHubAgent()
    
    event_types = []
    async for event in agent.stream("test query"):
        event_types.append(event.get('type'))
        
        # Stop after 10 events to prevent long test
        if len(event_types) >= 10:
            break
    
    # Verify we got events
    assert len(event_types) > 0
    
    # Verify expected event types
    assert any(t in ['token', 'tool_start', 'tool_end'] for t in event_types)
```

### Testing Timeouts

```python
@pytest.mark.asyncio
async def test_agent_timeout():
    """Test agent respects timeout."""
    import asyncio
    from agents.github_agent import GitHubAgent
    
    agent = GitHubAgent()
    
    # Should timeout after 1 second
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(
            agent.run_async("complex query"),
            timeout=1.0
        )
```

---

## Mocking and Fixtures

### Shared Fixtures (conftest.py)

```python
# tests/conftest.py

import pytest
from unittest.mock import Mock, AsyncMock, MagicMock


@pytest.fixture
def mock_llm():
    """Mock LLM for testing without API calls."""
    mock = Mock()
    mock.invoke.return_value = {
        "content": "Mocked LLM response"
    }
    return mock


@pytest.fixture
def mock_async_llm():
    """Mock async LLM."""
    mock = AsyncMock()
    mock.ainvoke.return_value = {
        "content": "Mocked async response"
    }
    return mock


@pytest.fixture
def sample_repository_data():
    """Sample repository data for testing."""
    return {
        "owner": "facebook",
        "repo": "react",
        "languages": {
            "JavaScript": 950000,
            "TypeScript": 50000
        },
        "file_count": 1234,
        "size_kb": 5678
    }


@pytest.fixture
def temp_config_file(tmp_path):
    """Create temporary config file for testing."""
    config_file = tmp_path / ".env"
    config_file.write_text("""
GOOGLE_API_KEY=test_key
MODEL_NAME=gemini-2.0-flash-exp
TEMPERATURE=0.0
""")
    return config_file


@pytest.fixture
async def initialized_agent(mock_async_llm):
    """Pre-initialized agent with mocked LLM."""
    from agents.github_agent import GitHubAgent
    
    # Create agent with mock
    agent = GitHubAgent()
    agent.llm = mock_async_llm  # Replace with mock
    
    yield agent
    
    # Cleanup (if needed)
    # await agent.cleanup()
```

### Using Mocks in Tests

```python
# tests/test_with_mocks.py

import pytest
from unittest.mock import Mock, patch, MagicMock


def test_agent_with_mock_llm(mock_llm):
    """Test agent using mocked LLM fixture."""
    from agents.github_agent import GitHubAgent
    
    # Create agent
    agent = GitHubAgent()
    agent.llm = mock_llm  # Use mock instead of real LLM
    
    # Run query (no API call made)
    result = agent.run("test query")
    
    # Verify mock was called
    assert mock_llm.invoke.called
    
    # Verify call arguments
    call_args = mock_llm.invoke.call_args
    print(f"Mock called with: {call_args}")


@patch('agents.github_agent.ChatGoogleGenerativeAI')
def test_agent_initialization_with_patch(mock_llm_class):
    """Test agent initialization with patched LLM class."""
    from agents.github_agent import GitHubAgent
    
    # Configure mock
    mock_instance = Mock()
    mock_llm_class.return_value = mock_instance
    
    # Create agent
    agent = GitHubAgent()
    
    # Verify LLM was initialized correctly
    mock_llm_class.assert_called_once()
    assert agent.llm == mock_instance


def test_tool_with_mock_api(monkeypatch):
    """Test tool with mocked external API."""
    from tools.github_tools import read_repository
    
    # Mock function
    def mock_github_api(owner, repo):
        return {"name": f"{owner}/{repo}", "stars": 1000}
    
    # Replace real function with mock
    monkeypatch.setattr(
        "tools.github_tools._fetch_github_data",
        mock_github_api
    )
    
    # Call tool (uses mock)
    result = read_repository.invoke({
        "owner": "test",
        "repo": "repo"
    })
    
    assert "test/repo" in result
```

### Advanced Mocking Patterns

```python
def test_tool_with_side_effects():
    """Test tool behavior with different side effects."""
    from unittest.mock import Mock
    
    mock_api = Mock()
    
    # First call succeeds, second fails
    mock_api.fetch.side_effect = [
        {"success": True},
        Exception("API Error")
    ]
    
    # First call
    result1 = mock_api.fetch()
    assert result1["success"] is True
    
    # Second call raises exception
    with pytest.raises(Exception, match="API Error"):
        mock_api.fetch()


def test_async_mock_with_return_value():
    """Test async mock with specific return values."""
    import asyncio
    
    mock_async = AsyncMock()
    mock_async.return_value = {"data": "test"}
    
    # Call async mock
    result = asyncio.run(mock_async())
    assert result == {"data": "test"}


def test_magic_mock_for_complex_objects():
    """Test complex object interactions with MagicMock."""
    mock_agent = MagicMock()
    
    # Configure nested attributes
    mock_agent.llm.model_name = "gemini-2.0-flash-exp"
    mock_agent.tools = [Mock(name="tool1"), Mock(name="tool2")]
    
    # Verify behavior
    assert mock_agent.llm.model_name == "gemini-2.0-flash-exp"
    assert len(mock_agent.tools) == 2
```

---

## Testing Agents

### Testing Agent Initialization

```python
# tests/test_github_agent.py

import pytest
from agents.github_agent import GitHubAgent


def test_agent_initialization_defaults():
    """Test agent initializes with default values."""
    agent = GitHubAgent()
    
    assert agent.llm is not None
    assert agent.tools is not None
    assert len(agent.tools) > 0
    assert agent.checkpointer is not None  # Default MemorySaver


def test_agent_initialization_custom_config():
    """Test agent initialization with custom configuration."""
    agent = GitHubAgent(
        model_name="gemini-1.5-flash",
        temperature=0.5,
        enable_checkpointing=False
    )
    
    assert agent.llm.model_name == "gemini-1.5-flash"
    assert agent.llm.temperature == 0.5
    assert agent.checkpointer is None  # Disabled


def test_agent_initialization_custom_tools():
    """Test agent with custom tools."""
    from tools.github_tools import read_repository
    
    custom_tools = [read_repository]
    agent = GitHubAgent(tools=custom_tools)
    
    assert len(agent.tools) == 1
    assert agent.tools[0].name == "read_repository"
```

### Testing Agent Execution

```python
@pytest.mark.asyncio
async def test_agent_run_async_success(initialized_agent):
    """Test successful agent execution."""
    result = await initialized_agent.run_async("test query")
    
    assert isinstance(result, dict)
    assert 'success' in result
    assert 'output' in result
    assert 'execution_time' in result
    assert 'thread_id' in result


@pytest.mark.asyncio
async def test_agent_error_handling(initialized_agent):
    """Test agent handles errors gracefully."""
    # Configure mock to raise error
    initialized_agent.llm.ainvoke.side_effect = Exception("API Error")
    
    with pytest.raises(Exception):
        await initialized_agent.run_async("test query")


def test_agent_thread_id_generation():
    """Test agent generates unique thread IDs."""
    agent = GitHubAgent()
    
    result1 = agent.run("query 1")
    result2 = agent.run("query 2")
    
    # Different queries can use same default thread_id
    # or verify custom thread_id handling
    result3 = agent.run("query 3", thread_id="custom_123")
    assert result3['thread_id'] == "custom_123"
```

---

## Testing Tools

### Testing Tool Input Validation

```python
# tests/test_github_tools.py

import pytest
from tools.github_tools import read_repository, ReadRepositoryInput


def test_tool_input_validation_valid():
    """Test tool accepts valid input."""
    input_data = ReadRepositoryInput(
        owner="facebook",
        repo="react"
    )
    
    assert input_data.owner == "facebook"
    assert input_data.repo == "react"


def test_tool_input_validation_missing_field():
    """Test tool rejects missing required fields."""
    with pytest.raises(ValueError):
        ReadRepositoryInput(owner="facebook")  # Missing repo


def test_tool_input_validation_invalid_type():
    """Test tool rejects invalid types."""
    with pytest.raises(ValueError):
        ReadRepositoryInput(
            owner="facebook",
            repo=123  # Should be string
        )
```

### Testing Tool Execution

```python
def test_read_repository_tool_mock():
    """Test read_repository tool with mocked implementation."""
    from unittest.mock import patch
    
    # Mock the internal implementation
    with patch('tools.github_tools._read_repository_impl') as mock_impl:
        mock_impl.return_value = "Repository: facebook/react\nLanguages: JavaScript"
        
        # Invoke tool
        result = read_repository.invoke({
            "owner": "facebook",
            "repo": "react"
        })
        
        # Verify
        assert "facebook/react" in result
        assert "JavaScript" in result
        mock_impl.assert_called_once_with("facebook", "react")


def test_tool_error_handling():
    """Test tool handles errors gracefully."""
    from unittest.mock import patch
    
    with patch('tools.github_tools._read_repository_impl') as mock_impl:
        mock_impl.side_effect = Exception("GitHub API Error")
        
        result = read_repository.invoke({
            "owner": "invalid",
            "repo": "repo"
        })
        
        # Tool should return error message, not raise
        assert "error" in result.lower()


@pytest.mark.parametrize("owner,repo", [
    ("facebook", "react"),
    ("google", "tensorflow"),
    ("microsoft", "vscode"),
])
def test_tool_multiple_repos(owner, repo):
    """Test tool works with different repositories."""
    with patch('tools.github_tools._read_repository_impl') as mock_impl:
        mock_impl.return_value = f"Analyzed {owner}/{repo}"
        
        result = read_repository.invoke({"owner": owner, "repo": repo})
        
        assert f"{owner}/{repo}" in result
```

---

## Testing APIs

### Testing FastAPI Endpoints

```python
# tests/test_api_integration.py

import pytest
from fastapi.testclient import TestClient
from api_server import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


def test_health_endpoint(client):
    """Test health check endpoint."""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_analyze_endpoint_success(client):
    """Test successful repository analysis."""
    response = client.post(
        "/analyze",
        json={
            "owner": "facebook",
            "repo": "react",
            "thread_id": "test_123"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "success" in data
    assert "output" in data
    assert "execution_time" in data


def test_analyze_endpoint_validation_error(client):
    """Test validation error handling."""
    response = client.post(
        "/analyze",
        json={
            "owner": "facebook"
            # Missing required 'repo' field
        }
    )
    
    assert response.status_code == 422  # Validation error


def test_analyze_endpoint_server_error(client, monkeypatch):
    """Test server error handling."""
    # Mock agent to raise error
    def mock_error(*args, **kwargs):
        raise Exception("Internal error")
    
    monkeypatch.setattr("api_server.agent.run_async", mock_error)
    
    response = client.post(
        "/analyze",
        json={
            "owner": "facebook",
            "repo": "react"
        }
    )
    
    assert response.status_code == 500
```

### Testing Streaming Endpoints

```python
@pytest.mark.asyncio
async def test_streaming_endpoint():
    """Test SSE streaming endpoint."""
    from httpx import AsyncClient
    import json
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        async with client.stream(
            "POST",
            "/stream",
            json={
                "owner": "facebook",
                "repo": "react"
            }
        ) as response:
            
            assert response.status_code == 200
            assert response.headers["content-type"] == "text/event-stream"
            
            events = []
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    event = json.loads(line[6:])
                    events.append(event)
                    
                    # Stop after 5 events
                    if len(events) >= 5:
                        break
            
            # Verify we received events
            assert len(events) > 0
            
            # Verify event structure
            for event in events:
                assert "type" in event
```

---

## Test Coverage

### Measuring Coverage

```bash
# Run tests with coverage
pytest --cov=agents --cov=tools --cov-report=term-missing

# Generate HTML report
pytest --cov=agents --cov=tools --cov-report=html

# Open in browser
open htmlcov/index.html
```

### Coverage Report Example

```
Name                          Stmts   Miss  Cover   Missing
-----------------------------------------------------------
agents/__init__.py                2      0   100%
agents/github_agent.py          127     12    91%   45-48, 89-92
tools/__init__.py                 3      0   100%
tools/github_tools.py            94      8    91%   102-105, 156-159
-----------------------------------------------------------
TOTAL                           226     20    91%
```

### Coverage Configuration

```ini
# .coveragerc

[run]
source = agents, tools
omit = 
    */tests/*
    */venv/*
    */__pycache__/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:
```

### Coverage Goals

**Target Coverage:**
- **Overall:** 80-90%
- **Critical paths:** 95-100% (authentication, core logic)
- **New code:** 90%+ before merging

**What NOT to aim for:**
- 100% coverage (diminishing returns)
- Coverage of generated code
- Coverage of external libraries

---

## Performance Testing

### Timing Tests

```python
import time
import pytest


def test_agent_performance():
    """Test agent response time is acceptable."""
    from agents.github_agent import GitHubAgent
    
    agent = GitHubAgent()
    
    start = time.time()
    result = agent.run("Simple query")
    duration = time.time() - start
    
    # Should complete within 10 seconds
    assert duration < 10.0
    assert result['execution_time'] < 10.0


@pytest.mark.slow
def test_concurrent_performance():
    """Test concurrent execution is faster than sequential."""
    import asyncio
    from agents.github_agent import GitHubAgent
    
    agent = GitHubAgent()
    queries = ["query1", "query2", "query3"]
    
    # Sequential timing
    seq_start = time.time()
    for query in queries:
        agent.run(query)
    seq_time = time.time() - seq_start
    
    # Concurrent timing
    async def concurrent():
        tasks = [agent.run_async(q) for q in queries]
        await asyncio.gather(*tasks)
    
    conc_start = time.time()
    asyncio.run(concurrent())
    conc_time = time.time() - conc_start
    
    # Concurrent should be faster
    assert conc_time < seq_time
    print(f"Speedup: {seq_time / conc_time:.2f}x")
```

### Load Testing

```python
import pytest
from locust import HttpUser, task, between


class AgentUser(HttpUser):
    """Locust user for load testing API."""
    
    wait_time = between(1, 3)  # Wait 1-3s between requests
    
    @task
    def analyze_repository(self):
        """Simulate repository analysis request."""
        self.client.post(
            "/analyze",
            json={
                "owner": "facebook",
                "repo": "react",
                "thread_id": f"user_{self.environment.runner.user_count}"
            }
        )


# Run load test:
# locust -f tests/test_load.py --host=http://localhost:8000
```

---

## Best Practices

### 1. Test Naming Conventions

```python
# ✓ Good: Descriptive names
def test_agent_handles_missing_api_key():
    """Test agent raises error when API key is missing."""
    pass

def test_tool_validates_repository_name_format():
    """Test tool validates owner/repo format."""
    pass

# ✗ Bad: Vague names
def test_agent():
    pass

def test_1():
    pass
```

### 2. Arrange-Act-Assert (AAA) Pattern

```python
def test_agent_execution():
    # Arrange: Set up test data and mocks
    agent = GitHubAgent()
    query = "test query"
    expected_keys = ['success', 'output']
    
    # Act: Execute the code under test
    result = agent.run(query)
    
    # Assert: Verify expectations
    assert all(key in result for key in expected_keys)
    assert result['success'] is True
```

### 3. One Assertion Per Test (Generally)

```python
# ✓ Good: Focused tests
def test_result_has_success_key():
    result = agent.run("query")
    assert 'success' in result

def test_result_has_output_key():
    result = agent.run("query")
    assert 'output' in result

# ⚠️ Acceptable: Related assertions
def test_result_structure():
    result = agent.run("query")
    assert isinstance(result, dict)
    assert 'success' in result
    assert 'output' in result
```

### 4. Use Fixtures for Reusable Setup

```python
# ✓ Good: DRY with fixtures
@pytest.fixture
def configured_agent():
    return GitHubAgent(temperature=0.0)

def test_with_fixture(configured_agent):
    result = configured_agent.run("query")
    assert result is not None

# ✗ Bad: Repeated setup
def test_1():
    agent = GitHubAgent(temperature=0.0)
    result = agent.run("query")

def test_2():
    agent = GitHubAgent(temperature=0.0)  # Repeated
    result = agent.run("query")
```

### 5. Test Edge Cases

```python
def test_empty_input():
    """Test behavior with empty input."""
    with pytest.raises(ValueError):
        process_input("")

def test_none_input():
    """Test behavior with None input."""
    with pytest.raises(TypeError):
        process_input(None)

def test_very_long_input():
    """Test behavior with very long input."""
    long_input = "a" * 10000
    result = process_input(long_input)
    assert len(result) <= 1000  # Truncated
```

### 6. Clean Up Resources

```python
@pytest.fixture
async def agent_with_cleanup():
    """Agent fixture with cleanup."""
    agent = GitHubAgent()
    
    yield agent
    
    # Cleanup after test
    await agent.close_connections()
    agent.clear_cache()


def test_with_cleanup(tmp_path):
    """Test that cleans up temporary files."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("test")
    
    try:
        # Test code
        process_file(test_file)
    finally:
        # Cleanup
        if test_file.exists():
            test_file.unlink()
```

### 7. Use Descriptive Error Messages

```python
# ✓ Good: Descriptive assertion messages
def test_agent_output():
    result = agent.run("query")
    assert result['success'], \
        f"Agent failed: {result.get('error', 'Unknown error')}"

# ✗ Bad: No context
def test_agent_output():
    result = agent.run("query")
    assert result['success']  # Why did it fail?
```

---

## Running Tests

### Basic Commands

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_github_agent.py

# Run specific test
pytest tests/test_github_agent.py::test_agent_initialization

# Run tests matching pattern
pytest -k "test_agent"

# Run with verbose output
pytest -v

# Run and stop on first failure
pytest -x

# Run last failed tests
pytest --lf
```

### Advanced Commands

```bash
# Run in parallel (requires pytest-xdist)
pytest -n auto

# Generate HTML coverage report
pytest --cov=agents --cov=tools --cov-report=html

# Run only fast tests (skip slow integration tests)
pytest -m "not slow"

# Run with specific marker
pytest -m integration

# Show print statements
pytest -s

# Create JUnit XML report (for CI/CD)
pytest --junitxml=report.xml
```

### Continuous Integration

```yaml
# .github/workflows/test.yml

name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.11
    
    - name: Install dependencies
      run: |
        pip install -r requirements-production.txt
        pip install pytest pytest-cov pytest-asyncio
    
    - name: Run tests
      run: |
        pytest --cov=agents --cov=tools --cov-report=xml
      env:
        GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
    
    - name: Upload coverage
      uses: codecov/codecov-action@v2
```

---

**Document Information:**
- **Created:** January 2, 2026
- **Version:** 1.0
- **Lines:** 1,200+
- **Related:** [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md), [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

**External References:**
- [Pytest Documentation](https://docs.pytest.org/)
- [unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)
- [pytest-asyncio Documentation](https://pytest-asyncio.readthedocs.io/)
- [Testing Best Practices](https://docs.pytest.org/en/latest/goodpractices.html)
