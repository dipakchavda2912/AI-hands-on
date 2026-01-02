# Development Guide

Complete guide to extending, customizing, and contributing to CodeBaseOpsAI-v3.

---

## Table of Contents

1. [Getting Started as a Developer](#getting-started-as-a-developer)
2. [Project Structure Deep Dive](#project-structure-deep-dive)
3. [Adding New Tools](#adding-new-tools)
4. [Creating Custom Agents](#creating-custom-agents)
5. [Modifying Existing Functionality](#modifying-existing-functionality)
6. [Code Style and Conventions](#code-style-and-conventions)
7. [Testing Your Changes](#testing-your-changes)
8. [Documentation Standards](#documentation-standards)
9. [Debugging Workflows](#debugging-workflows)
10. [Pull Request Guidelines](#pull-request-guidelines)
11. [Advanced Development Patterns](#advanced-development-patterns)

---

## Getting Started as a Developer

### Development Setup

```bash
# 1. Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/CodeBaseOpsAI-v3.git
cd CodeBaseOpsAI-v3

# 2. Create development environment
python3.11 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# 3. Install ALL dependencies (including dev tools)
pip install --upgrade pip
pip install -r requirements-production.txt
pip install -r requirements-api.txt

# Install development tools
pip install pytest pytest-asyncio pytest-cov
pip install black isort flake8 mypy
pip install pre-commit

# 4. Set up pre-commit hooks
pre-commit install

# 5. Copy environment template
cp env.example .env

# 6. Add your API key to .env
echo "GOOGLE_API_KEY=your-key-here" >> .env

# 7. Verify setup
python -m pytest tests/
```

### Development Tools

Install these recommended tools:

```bash
# Code formatting
pip install black isort

# Linting
pip install flake8 pylint

# Type checking
pip install mypy

# Testing
pip install pytest pytest-asyncio pytest-cov pytest-mock

# Documentation
pip install mkdocs mkdocs-material

# Git hooks
pip install pre-commit
```

---

## Project Structure Deep Dive

### Directory Layout

```
CodeBaseOpsAI-v3/
├── agents/              # Agent implementations
│   ├── __init__.py     # Package initialization
│   └── github_agent.py # Main GitHub agent
│
├── tools/              # LangChain tools
│   ├── __init__.py
│   └── github_tools.py # GitHub-specific tools
│
├── config.py           # Configuration management
├── main.py            # Example usage
├── api_server.py      # FastAPI REST API
│
├── tests/             # Test suite
│   ├── conftest.py    # Shared fixtures
│   ├── test_github_agent.py
│   ├── test_github_tools.py
│   └── test_api_integration.py
│
├── docs/              # Documentation
│   ├── guides/        # User guides
│   ├── reference/     # Technical reference
│   ├── deployment/    # Deployment guides
│   └── migration/     # Migration docs
│
├── requirements-production.txt  # Core dependencies
├── requirements-api.txt         # API dependencies
├── Dockerfile                   # Container image
└── docker-compose.yml          # Multi-container setup
```

### File Ownership and Responsibilities

| File | Purpose | When to Modify |
|------|---------|----------------|
| `agents/github_agent.py` | Agent execution logic | Adding agent features, streaming improvements |
| `tools/github_tools.py` | Tool implementations | Adding new tools, modifying tool behavior |
| `config.py` | Configuration management | Adding new settings, environment variables |
| `main.py` | Example usage | Adding usage examples |
| `api_server.py` | REST API endpoints | Adding new endpoints, modifying API |
| `tests/*` | Test suites | Adding tests for new features |

---

## Adding New Tools

### Step 1: Define Tool Function

Tools in LangChain are Python functions decorated with `@tool`. Here's how to create one:

```python
# tools/github_tools.py

from langchain_core.tools import tool
from pydantic import BaseModel, Field
from typing import Optional

# Step 1: Define input schema with Pydantic
class SearchCodeInput(BaseModel):
    """Input schema for searching code."""
    
    query: str = Field(
        description="Search query (e.g., 'function authenticate')"
    )
    language: Optional[str] = Field(
        default=None,
        description="Filter by programming language (e.g., 'python', 'javascript')"
    )
    owner: Optional[str] = Field(
        default=None,
        description="Filter by repository owner"
    )
    repo: Optional[str] = Field(
        default=None,
        description="Filter by repository name"
    )

# Step 2: Implement tool function
@tool(args_schema=SearchCodeInput)
def search_code(
    query: str,
    language: Optional[str] = None,
    owner: Optional[str] = None,
    repo: Optional[str] = None
) -> str:
    """
    Search for code across GitHub repositories.
    
    Use this tool when the user wants to:
    - Find code examples: "Find Python authentication code"
    - Search in specific repo: "Search for 'async' in microsoft/vscode"
    - Filter by language: "Find JavaScript React components"
    
    Args:
        query: Search query string
        language: Programming language filter
        owner: Repository owner filter
        repo: Repository name filter
    
    Returns:
        Formatted search results with code snippets.
    
    Examples:
        - search_code("authentication", language="python")
        - search_code("async await", owner="microsoft", repo="vscode")
    """
    try:
        # Implementation
        search_query = query
        
        # Add filters
        if language:
            search_query += f" language:{language}"
        if owner and repo:
            search_query += f" repo:{owner}/{repo}"
        
        # Mock implementation - replace with real GitHub API
        results = _search_github_code(search_query)
        
        # Format results
        formatted = "Search Results:\n\n"
        for i, result in enumerate(results[:5], 1):
            formatted += f"{i}. {result['path']} ({result['repo']})\n"
            formatted += f"   {result['snippet']}\n\n"
        
        return formatted
        
    except Exception as e:
        logger.error(f"Code search failed: {e}")
        return f"Error searching code: {str(e)}"

# Helper function
def _search_github_code(query: str) -> list:
    """
    Actual GitHub code search implementation.
    
    In production, this would use GitHub API:
    https://docs.github.com/en/rest/search#search-code
    """
    # Mock implementation
    return [
        {
            "path": "src/auth/login.py",
            "repo": "example/repo",
            "snippet": "def authenticate(username, password):"
        }
    ]
```

### Step 2: Register Tool in get_tools()

```python
# tools/github_tools.py

def get_tools() -> List[BaseTool]:
    """
    Get all available GitHub tools.
    
    Returns:
        List of LangChain tools ready for agent use.
    """
    return [
        read_repository,
        clone_repository,
        search_code,  # ✓ Add your new tool here
    ]
```

### Step 3: Write Tests

```python
# tests/test_github_tools.py

import pytest
from tools.github_tools import search_code, SearchCodeInput

def test_search_code_basic():
    """Test basic code search."""
    result = search_code.invoke({
        "query": "authentication"
    })
    
    assert result is not None
    assert "Search Results" in result

def test_search_code_with_language():
    """Test code search with language filter."""
    result = search_code.invoke({
        "query": "async",
        "language": "python"
    })
    
    assert "language:python" in result or "Search Results" in result

def test_search_code_with_repo():
    """Test code search in specific repository."""
    result = search_code.invoke({
        "query": "function",
        "owner": "microsoft",
        "repo": "vscode"
    })
    
    assert result is not None

def test_search_code_validation():
    """Test input validation."""
    # Test with invalid input
    with pytest.raises(Exception):
        search_code.invoke({
            "query": "",  # Empty query should fail
        })

@pytest.mark.asyncio
async def test_search_code_in_agent():
    """Test tool integration with agent."""
    from agents.github_agent import GitHubAgent
    
    agent = GitHubAgent()
    
    # Ensure tool is available
    tool_names = [t.name for t in agent.tools]
    assert "search_code" in tool_names
    
    # Test agent using the tool
    result = await agent.run_async(
        "Search for Python authentication code"
    )
    
    assert result is not None
```

### Step 4: Document Your Tool

Add to API_REFERENCE.md:

```markdown
### search_code

Search for code across GitHub repositories.

**Function Signature:**
```python
def search_code(
    query: str,
    language: Optional[str] = None,
    owner: Optional[str] = None,
    repo: Optional[str] = None
) -> str
```

**Parameters:**
- `query` (str): Search query string
- `language` (Optional[str]): Programming language filter
- `owner` (Optional[str]): Repository owner
- `repo` (Optional[str]): Repository name

**Returns:**
- str: Formatted search results with code snippets

**Usage Examples:**
```python
# Basic search
result = search_code.invoke({"query": "authentication"})

# Search with language filter
result = search_code.invoke({
    "query": "async await",
    "language": "python"
})

# Search in specific repository
result = search_code.invoke({
    "query": "component",
    "owner": "facebook",
    "repo": "react"
})
```
```

### Tool Development Best Practices

1. **Clear Descriptions:**
   - Describe WHEN to use the tool (user intent)
   - Provide concrete examples
   - Mention what the tool returns

2. **Input Validation:**
   - Use Pydantic schemas
   - Validate all inputs
   - Provide helpful error messages

3. **Error Handling:**
   - Wrap in try/except
   - Log errors with context
   - Return user-friendly error messages

4. **Return Format:**
   - Return strings (LangChain requirement)
   - Format output clearly
   - Include metadata when useful

5. **Testing:**
   - Unit tests for tool function
   - Integration tests with agent
   - Test error cases

**External Reference:** [LangChain Tools Documentation](https://python.langchain.com/docs/modules/tools/)

---

## Creating Custom Agents

### Basic Agent Structure

```python
# agents/custom_agent.py

import logging
from typing import Dict, Any, List, AsyncIterator
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import BaseTool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from config import get_settings

logger = logging.getLogger(__name__)

class CustomAgent:
    """
    Custom agent for specific domain.
    
    This template shows how to create a new agent with:
    - Custom tools
    - Custom prompts
    - State management
    - Streaming support
    """
    
    def __init__(
        self,
        tools: List[BaseTool] = None,
        model_name: str = None,
        temperature: float = None,
        enable_checkpointing: bool = True
    ):
        """
        Initialize custom agent.
        
        Args:
            tools: List of LangChain tools (if None, uses default)
            model_name: Google Gemini model name
            temperature: LLM temperature (0.0 = deterministic, 1.0 = creative)
            enable_checkpointing: Whether to save conversation state
        """
        self.settings = get_settings()
        
        # Use provided values or defaults from config
        self.model_name = model_name or self.settings.model_name
        self.temperature = temperature or self.settings.temperature
        
        # Initialize LLM
        self.llm = ChatGoogleGenerativeAI(
            model=self.model_name,
            temperature=self.temperature,
            google_api_key=self.settings.google_api_key
        )
        
        # Set tools
        self.tools = tools or self._get_default_tools()
        
        # Set up checkpointing
        self.checkpointer = MemorySaver() if enable_checkpointing else None
        
        # Create agent
        self.agent = self._create_agent()
        
        logger.info(f"Initialized {self.__class__.__name__} with {len(self.tools)} tools")
    
    def _get_default_tools(self) -> List[BaseTool]:
        """Get default tools for this agent."""
        # Import your custom tools
        from tools.custom_tools import get_custom_tools
        return get_custom_tools()
    
    def _create_agent(self):
        """Create LangGraph ReAct agent."""
        system_prompt = self._get_system_prompt()
        
        return create_react_agent(
            self.llm,
            self.tools,
            state_modifier=system_prompt,
            checkpointer=self.checkpointer
        )
    
    def _get_system_prompt(self) -> str:
        """
        Get system prompt for agent.
        
        This defines the agent's behavior, personality, and guidelines.
        """
        return """You are a helpful AI assistant specialized in [DOMAIN].
        
Your responsibilities:
- [Responsibility 1]
- [Responsibility 2]
- [Responsibility 3]

When answering questions:
1. Always use available tools to get accurate information
2. Explain your reasoning step by step
3. Provide specific examples when helpful
4. If you're unsure, say so

Available tools:
{tool_descriptions}

Guidelines:
- Be concise but thorough
- Cite sources when using tool data
- Ask clarifying questions if needed
"""
    
    def run(self, query: str, thread_id: str = "default") -> Dict[str, Any]:
        """
        Run agent synchronously.
        
        Args:
            query: User query
            thread_id: Conversation thread ID for state persistence
        
        Returns:
            Agent response with messages and metadata
        """
        config = {"configurable": {"thread_id": thread_id}}
        
        try:
            result = self.agent.invoke(
                {"messages": [("user", query)]},
                config
            )
            
            logger.info(f"Agent completed query: {query[:50]}...")
            return result
            
        except Exception as e:
            logger.error(f"Agent execution failed: {e}")
            raise
    
    async def run_async(self, query: str, thread_id: str = "default") -> Dict[str, Any]:
        """
        Run agent asynchronously.
        
        Args:
            query: User query
            thread_id: Conversation thread ID
        
        Returns:
            Agent response
        """
        config = {"configurable": {"thread_id": thread_id}}
        
        try:
            result = await self.agent.ainvoke(
                {"messages": [("user", query)]},
                config
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Async agent execution failed: {e}")
            raise
    
    async def stream(
        self,
        query: str,
        thread_id: str = "default"
    ) -> AsyncIterator[Dict[str, Any]]:
        """
        Stream agent execution.
        
        Args:
            query: User query
            thread_id: Conversation thread ID
        
        Yields:
            Stream events (tool calls, thoughts, final answer)
        """
        config = {"configurable": {"thread_id": thread_id}}
        
        try:
            stream = self.agent.astream_events(
                {"messages": [("user", query)]},
                config,
                version="v2"
            )
            
            async for event in stream:
                # Format and yield events
                formatted = self._format_stream_event(event)
                if formatted:
                    yield formatted
                    
        except Exception as e:
            logger.error(f"Streaming failed: {e}")
            yield {"type": "error", "error": str(e)}
    
    def _format_stream_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Format stream event for consumption."""
        event_type = event.get("event")
        
        if event_type == "on_chat_model_stream":
            # LLM token streaming
            content = event.get("data", {}).get("chunk", {}).get("content", "")
            if content:
                return {"type": "token", "content": content}
        
        elif event_type == "on_tool_start":
            # Tool execution started
            tool_name = event.get("name", "unknown")
            return {"type": "tool_start", "tool": tool_name}
        
        elif event_type == "on_tool_end":
            # Tool execution completed
            tool_name = event.get("name", "unknown")
            output = event.get("data", {}).get("output", "")
            return {"type": "tool_end", "tool": tool_name, "output": output}
        
        return None
```

### Using Your Custom Agent

```python
# main.py

from agents.custom_agent import CustomAgent

def main():
    # Initialize agent
    agent = CustomAgent()
    
    # Synchronous execution
    result = agent.run("Your query here")
    print(result)
    
    # Async execution
    import asyncio
    result = asyncio.run(agent.run_async("Your query"))
    
    # Streaming
    async def stream_example():
        async for event in agent.stream("Your query"):
            print(event)
    
    asyncio.run(stream_example())

if __name__ == "__main__":
    main()
```

---

## Modifying Existing Functionality

### Extending GitHubAgent

```python
# agents/github_agent.py

class GitHubAgent:
    """Existing agent class."""
    
    def run(self, query: str, thread_id: str = "default") -> Dict[str, Any]:
        """Existing method."""
        # ... existing code ...
    
    # ✓ Add new method
    def run_with_retry(
        self,
        query: str,
        max_retries: int = 3,
        thread_id: str = "default"
    ) -> Dict[str, Any]:
        """
        Run agent with automatic retry on failure.
        
        Args:
            query: User query
            max_retries: Maximum number of retry attempts
            thread_id: Conversation thread ID
        
        Returns:
            Agent response
        
        Raises:
            RuntimeError: If all retries fail
        """
        for attempt in range(max_retries):
            try:
                return self.run(query, thread_id)
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise RuntimeError(f"All {max_retries} attempts failed") from e
                time.sleep(2 ** attempt)  # Exponential backoff
    
    # ✓ Add batch processing
    async def run_batch(
        self,
        queries: List[str],
        thread_id: str = "default"
    ) -> List[Dict[str, Any]]:
        """
        Process multiple queries concurrently.
        
        Args:
            queries: List of user queries
            thread_id: Conversation thread ID
        
        Returns:
            List of agent responses in same order as queries
        """
        tasks = [
            self.run_async(query, f"{thread_id}_{i}")
            for i, query in enumerate(queries)
        ]
        
        return await asyncio.gather(*tasks)
```

### Customizing Tool Behavior

```python
# tools/github_tools.py

# ✓ Add caching to expensive operations
from functools import lru_cache
import hashlib

class ToolCache:
    """Simple in-memory cache for tool results."""
    
    def __init__(self, max_size: int = 100):
        self.cache = {}
        self.max_size = max_size
    
    def get(self, key: str):
        """Get cached value."""
        return self.cache.get(key)
    
    def set(self, key: str, value: Any):
        """Set cached value."""
        if len(self.cache) >= self.max_size:
            # Remove oldest entry
            self.cache.pop(next(iter(self.cache)))
        self.cache[key] = value

# Global cache instance
_tool_cache = ToolCache()

@tool(args_schema=ReadRepositoryInput)
def read_repository(owner: str, repo: str) -> str:
    """Read repository with caching."""
    
    # Check cache
    cache_key = f"{owner}/{repo}"
    cached = _tool_cache.get(cache_key)
    if cached:
        logger.info(f"Cache hit for {cache_key}")
        return cached
    
    # Execute original logic
    try:
        result = _read_repository_impl(owner, repo)
        
        # Cache result
        _tool_cache.set(cache_key, result)
        
        return result
    except Exception as e:
        logger.error(f"Repository read failed: {e}")
        return f"Error: {str(e)}"
```

---

## Code Style and Conventions

### Python Style Guide

We follow [PEP 8](https://peps.python.org/pep-0008/) with some additions:

```python
# ✓ Good examples

# 1. Imports: Standard library → Third party → Local
import os
import sys
from typing import Dict, List, Optional

from langchain_core.tools import tool
from pydantic import BaseModel

from config import get_settings

# 2. Class naming: PascalCase
class GitHubAgent:
    pass

# 3. Function naming: snake_case
def get_tools() -> List[BaseTool]:
    pass

# 4. Constants: UPPER_SNAKE_CASE
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30

# 5. Type hints everywhere
def process_data(
    items: List[str],
    config: Optional[Dict[str, Any]] = None
) -> Dict[str, int]:
    """Process items with optional config."""
    pass

# 6. Docstrings: Google style
def complex_function(param1: str, param2: int) -> bool:
    """
    Short one-line description.
    
    Longer description explaining the function's purpose,
    behavior, and any important notes.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When validation fails
        RuntimeError: When execution fails
    
    Examples:
        >>> complex_function("test", 42)
        True
    """
    pass

# 7. Line length: 100 characters (not 79)
# Use black formatter with --line-length 100

# 8. String formatting: f-strings preferred
name = "John"
age = 30
message = f"{name} is {age} years old"  # ✓
message = "%s is %d years old" % (name, age)  # ✗

# 9. Boolean comparisons: Direct comparison
if items:  # ✓
    pass
if len(items) > 0:  # ✗
    pass

if value is None:  # ✓
    pass
if value == None:  # ✗
    pass
```

### Async/Await Conventions

```python
# ✓ Good async patterns

# 1. Always use async/await for I/O operations
async def fetch_data():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com")
        return response.json()

# 2. Name async functions with async_ prefix (optional but recommended)
async def async_process_items(items: List[str]) -> List[Dict]:
    """Process items asynchronously."""
    pass

# 3. Use asyncio.gather() for concurrent operations
async def fetch_multiple():
    results = await asyncio.gather(
        fetch_data_1(),
        fetch_data_2(),
        fetch_data_3()
    )
    return results

# 4. Handle exceptions in async code
async def safe_fetch():
    try:
        return await fetch_data()
    except httpx.HTTPError as e:
        logger.error(f"HTTP error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise

# 5. Use async context managers
async def use_resource():
    async with AsyncResource() as resource:
        await resource.do_something()
```

### Error Handling

```python
# ✓ Good error handling

def process_item(item: str) -> Dict[str, Any]:
    """Process single item with comprehensive error handling."""
    
    # 1. Validate inputs early
    if not item:
        raise ValueError("Item cannot be empty")
    
    try:
        # 2. Main logic
        result = expensive_operation(item)
        
        # 3. Validate outputs
        if not result:
            raise RuntimeError("Operation produced no result")
        
        return result
        
    except ValueError as e:
        # 4. Handle specific exceptions
        logger.error(f"Validation error: {e}")
        raise  # Re-raise if caller should handle
        
    except Exception as e:
        # 5. Catch unexpected errors
        logger.error(f"Unexpected error processing {item}: {e}", exc_info=True)
        return {"error": str(e), "item": item}
    
    finally:
        # 6. Cleanup (if needed)
        cleanup_resources()
```

### Logging Best Practices

```python
import logging

logger = logging.getLogger(__name__)

# ✓ Good logging

# 1. Appropriate log levels
logger.debug("Detailed diagnostic info")
logger.info("General informational messages")
logger.warning("Warning messages for recoverable issues")
logger.error("Error messages for failures")
logger.critical("Critical errors requiring immediate attention")

# 2. Include context in log messages
logger.info(f"Processing repository {owner}/{repo}")
logger.error(f"Failed to fetch {url}: {error}", exc_info=True)

# 3. Use structured logging
logger.info(
    "Request completed",
    extra={
        "duration_ms": 123,
        "status_code": 200,
        "endpoint": "/api/agent"
    }
)

# 4. Avoid logging sensitive data
logger.info(f"API key: {api_key}")  # ✗ NEVER DO THIS
logger.info(f"API key configured: {bool(api_key)}")  # ✓
```

---

## Testing Your Changes

### Test Structure

```
tests/
├── conftest.py              # Shared fixtures
├── test_github_agent.py     # Agent tests
├── test_github_tools.py     # Tool tests
├── test_api_integration.py  # API tests
└── test_my_feature.py       # Your new tests
```

### Writing Unit Tests

```python
# tests/test_my_feature.py

import pytest
from unittest.mock import Mock, patch, AsyncMock
from my_module import my_function

class TestMyFeature:
    """Test suite for my new feature."""
    
    def test_basic_functionality(self):
        """Test basic functionality works."""
        result = my_function("input")
        assert result == "expected"
    
    def test_with_different_inputs(self):
        """Test with various inputs."""
        test_cases = [
            ("input1", "output1"),
            ("input2", "output2"),
            ("input3", "output3"),
        ]
        
        for input_val, expected in test_cases:
            result = my_function(input_val)
            assert result == expected
    
    def test_error_handling(self):
        """Test error handling."""
        with pytest.raises(ValueError):
            my_function("")  # Empty input should raise error
    
    @pytest.mark.asyncio
    async def test_async_function(self):
        """Test async functions."""
        result = await my_async_function("input")
        assert result is not None
    
    def test_with_mock(self):
        """Test with mocked dependencies."""
        mock_dependency = Mock()
        mock_dependency.do_something.return_value = "mocked"
        
        result = my_function_with_dependency(mock_dependency)
        
        assert result == "mocked"
        mock_dependency.do_something.assert_called_once()
    
    @patch('my_module.external_api')
    def test_with_patch(self, mock_api):
        """Test with patched external dependencies."""
        mock_api.fetch_data.return_value = {"data": "test"}
        
        result = my_function()
        
        assert result["data"] == "test"
        mock_api.fetch_data.assert_called()
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_my_feature.py

# Run specific test
pytest tests/test_my_feature.py::TestMyFeature::test_basic_functionality

# Run with coverage
pytest --cov=agents --cov=tools --cov-report=html

# Run with verbose output
pytest -v

# Run tests matching pattern
pytest -k "test_async"

# Stop on first failure
pytest -x

# Run tests in parallel (requires pytest-xdist)
pytest -n auto
```

### Test Coverage Goals

- **Minimum:** 80% coverage for new code
- **Target:** 90% coverage overall
- **Critical paths:** 100% coverage (authentication, API, core logic)

```bash
# Generate coverage report
pytest --cov=agents --cov=tools --cov-report=term-missing

# View in browser
pytest --cov=agents --cov=tools --cov-report=html
open htmlcov/index.html
```

---

## Documentation Standards

### Code Documentation

```python
def function_template(
    param1: str,
    param2: Optional[int] = None,
    param3: List[str] = None
) -> Dict[str, Any]:
    """
    Short one-line summary of what the function does.
    
    Longer description providing more context about the function's
    purpose, behavior, and any important considerations. This can
    span multiple lines.
    
    Args:
        param1: Description of param1, including what values are valid
        param2: Description of param2. Defaults to None which means...
        param3: Description of param3. If not provided, uses empty list.
    
    Returns:
        Description of return value, including structure and any
        important fields if returning a dictionary or object.
    
    Raises:
        ValueError: When param1 is empty or invalid
        RuntimeError: When execution fails for XYZ reason
        APIError: When external API call fails
    
    Examples:
        Basic usage:
        >>> function_template("test")
        {'result': 'success'}
        
        With optional parameters:
        >>> function_template("test", param2=42, param3=["a", "b"])
        {'result': 'success', 'count': 42}
    
    Notes:
        - Any special considerations or gotchas
        - Performance characteristics
        - Thread safety information
    
    See Also:
        - related_function(): Related functionality
        - AnotherClass: Related class
    """
    pass
```

### Markdown Documentation

```markdown
# Page Title

Brief introduction to the topic.

---

## Section 1

Content with examples:

```python
# Code example with explanation
def example():
    pass
```

**Key Points:**
- Point 1
- Point 2
- Point 3

---

## Section 2

### Subsection

More detailed content.

**Related Resources:**
- [TESTING_GUIDE.md](TESTING_GUIDE.md) - Testing best practices
- [CONFIGURATION_GUIDE.md](CONFIGURATION_GUIDE.md) - Configuration reference
```

---

## Debugging Workflows

### Local Development Debugging

```python
# 1. Use logging extensively
import logging
logging.basicConfig(level=logging.DEBUG)

# 2. Use debugger
import pdb; pdb.set_trace()  # Classic
breakpoint()  # Python 3.7+

# 3. Print debugging (temporary only)
print(f"DEBUG: variable = {variable}")

# 4. Use assertions for assumptions
assert isinstance(result, dict), f"Expected dict, got {type(result)}"
```

### Remote Debugging (VS Code)

```json
// .vscode/launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": false
        },
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "api_server:app",
                "--reload",
                "--port",
                "8000"
            ],
            "jinja": true
        }
    ]
}
```

---

## Pull Request Guidelines

### Before Submitting

```bash
# 1. Ensure all tests pass
pytest

# 2. Check code style
black --check .
isort --check .
flake8 .

# 3. Type checking
mypy agents/ tools/

# 4. Test coverage
pytest --cov=agents --cov=tools

# 5. Update documentation
# - Add docstrings to new functions
# - Update relevant .md files
# - Add examples if needed
```

### PR Template

```markdown
## Description

Brief description of the changes.

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Changes Made

- Change 1
- Change 2
- Change 3

## Testing

- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Documentation

- [ ] Code documented
- [ ] README updated (if needed)
- [ ] API reference updated (if needed)

## Checklist

- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Coverage maintained/improved
- [ ] No breaking changes (or documented)
```

---

## Advanced Development Patterns

### Dependency Injection

```python
# Instead of hard-coding dependencies
class Agent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(...)  # Hard-coded
        self.tools = get_tools()  # Hard-coded

# ✓ Use dependency injection
class Agent:
    def __init__(
        self,
        llm: Optional[ChatGoogleGenerativeAI] = None,
        tools: Optional[List[BaseTool]] = None
    ):
        self.llm = llm or self._create_default_llm()
        self.tools = tools or self._get_default_tools()
    
    # Now easily testable with mocks!
```

### Factory Pattern

```python
# agents/factory.py

class AgentFactory:
    """Factory for creating different types of agents."""
    
    @staticmethod
    def create_agent(agent_type: str, **kwargs):
        """Create agent based on type."""
        if agent_type == "github":
            from agents.github_agent import GitHubAgent
            return GitHubAgent(**kwargs)
        elif agent_type == "custom":
            from agents.custom_agent import CustomAgent
            return CustomAgent(**kwargs)
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")

# Usage
agent = AgentFactory.create_agent("github")
```

### Plugin System

```python
# plugins/base.py

from abc import ABC, abstractmethod

class ToolPlugin(ABC):
    """Base class for tool plugins."""
    
    @abstractmethod
    def get_tools(self) -> List[BaseTool]:
        """Return list of tools provided by this plugin."""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Return plugin name."""
        pass

# plugins/github_plugin.py

class GitHubPlugin(ToolPlugin):
    def get_tools(self) -> List[BaseTool]:
        from tools.github_tools import get_tools
        return get_tools()
    
    def get_name(self) -> str:
        return "GitHub Tools"

# Load plugins dynamically
def load_plugins() -> List[BaseTool]:
    """Load all available plugins."""
    plugins = [
        GitHubPlugin(),
        # Add more plugins here
    ]
    
    all_tools = []
    for plugin in plugins:
        all_tools.extend(plugin.get_tools())
    
    return all_tools
```

---

**Document Information:**
- **Created:** January 2, 2026
- **Version:** 1.0
- **Lines:** 1,400+
- **Related:** [TESTING_GUIDE.md](TESTING_GUIDE.md), [API_REFERENCE.md](../reference/API_REFERENCE.md)
