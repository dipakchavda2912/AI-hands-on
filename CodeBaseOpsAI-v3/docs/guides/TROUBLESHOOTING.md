# Troubleshooting Guide

Complete guide to debugging issues, resolving common errors, and optimizing your CodeBaseOpsAI-v3 application.

---

## Table of Contents

1. [Quick Diagnostic Checklist](#quick-diagnostic-checklist)
2. [Common Error Messages](#common-error-messages)
3. [Installation Issues](#installation-issues)
4. [API and Authentication Errors](#api-and-authentication-errors)
5. [Agent Execution Problems](#agent-execution-problems)
6. [Streaming Issues](#streaming-issues)
7. [Performance Problems](#performance-problems)
8. [Testing Failures](#testing-failures)
9. [Debugging Techniques](#debugging-techniques)
10. [Environment Issues](#environment-issues)
11. [Docker and Deployment Issues](#docker-and-deployment-issues)
12. [Advanced Debugging](#advanced-debugging)

---

## Quick Diagnostic Checklist

Before diving into specific issues, run through this checklist:

```bash
# 1. Check Python version (must be 3.11+)
python --version

# 2. Verify virtual environment is activated
which python  # Should show path to .venv/bin/python

# 3. Check dependencies are installed
pip list | grep -E "langgraph|langchain|google"

# 4. Verify environment variables
python -c "import os; print('GOOGLE_API_KEY:', 'SET' if os.getenv('GOOGLE_API_KEY') else 'NOT SET')"

# 5. Test basic imports
python -c "from agents.github_agent import GitHubAgent; print('✓ Imports OK')"

# 6. Run health check (if API server is running)
curl http://localhost:8000/health
```

**Expected Results:**
- Python: 3.11.0 or higher
- Virtual env: `/path/to/CodeBaseOpsAI-v3/.venv/bin/python`
- Dependencies: All packages listed
- GOOGLE_API_KEY: SET
- Imports: ✓ Imports OK
- Health: `{"status": "healthy", ...}`

---

## Common Error Messages

### 1. ImportError: No module named 'langgraph'

**Error:**
```
ImportError: No module named 'langgraph'
```

**Cause:** Dependencies not installed or wrong environment.

**Solution:**
```bash
# Ensure virtual environment is activated
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements-production.txt

# Verify installation
pip show langgraph
```

**External Reference:** [Python Virtual Environments Guide](https://docs.python.org/3/tutorial/venv.html)

---

### 2. google.api_core.exceptions.PermissionDenied: API key not valid

**Error:**
```
google.api_core.exceptions.PermissionDenied: 403 API key not valid. 
Please pass a valid API key.
```

**Cause:** Missing, invalid, or incorrectly formatted Google API key.

**Solution:**

1. **Get a valid API key:**
   - Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Create or copy your API key
   
2. **Set in .env file:**
   ```bash
   # .env file
   GOOGLE_API_KEY=AIzaSyD-your-actual-key-here
   ```

3. **Verify it's loaded:**
   ```python
   # test_api_key.py
   import os
   from dotenv import load_dotenv
   
   load_dotenv()
   api_key = os.getenv("GOOGLE_API_KEY")
   
   if not api_key:
       print("❌ API key not found")
   elif not api_key.startswith("AIzaSy"):
       print("❌ API key format incorrect")
   else:
       print(f"✓ API key loaded: {api_key[:10]}...")
   ```

4. **Common mistakes:**
   - Extra spaces: `GOOGLE_API_KEY= AIzaSy...` ❌
   - Quotes in .env: `GOOGLE_API_KEY="AIzaSy..."` ❌ (don't quote in .env)
   - Wrong file location: Ensure `.env` is in project root
   - Not calling `load_dotenv()` before accessing key

**Code Example from Project:**
```python
# From config.py
from dotenv import load_dotenv

load_dotenv()  # Must be called BEFORE accessing environment variables

class Settings(BaseSettings):
    google_api_key: str = Field(
        default_factory=lambda: os.getenv("GOOGLE_API_KEY", ""),
        description="Google API Key for Gemini models"
    )
```

---

### 3. ValueError: Model 'gemini-2.0-flash-exp' not found

**Error:**
```
ValueError: Model 'gemini-2.0-flash-exp' not found or not supported
```

**Cause:** Model name changed or deprecated, or API key doesn't have access.

**Solution:**

1. **Check available models:**
   ```python
   from langchain_google_genai import ChatGoogleGenerativeAI
   
   # Try different models
   models_to_try = [
       "gemini-2.0-flash-exp",
       "gemini-1.5-flash",
       "gemini-1.5-pro",
       "gemini-pro"
   ]
   
   for model in models_to_try:
       try:
           llm = ChatGoogleGenerativeAI(model=model, temperature=0)
           response = llm.invoke("Hi")
           print(f"✓ {model} works!")
           break
       except Exception as e:
           print(f"✗ {model} failed: {e}")
   ```

2. **Update config.py:**
   ```python
   # config.py
   model_name: str = Field(
       default="gemini-1.5-flash",  # More stable model
       description="Google Gemini model name"
   )
   ```

**External Reference:** [Google AI Gemini Models](https://ai.google.dev/models/gemini)

---

### 4. RuntimeError: Event loop is already running

**Error:**
```
RuntimeError: This event loop is already running
```

**Cause:** Trying to use `asyncio.run()` inside Jupyter notebook or when loop already exists.

**Solution:**

**In Jupyter Notebooks:**
```python
# ❌ Don't use asyncio.run() in Jupyter
# asyncio.run(agent.run_async("query"))

# ✓ Use await directly
result = await agent.run_async("What repositories exist?")
```

**In Regular Python Scripts:**
```python
# ✓ Use asyncio.run() for top-level
import asyncio

async def main():
    agent = GitHubAgent()
    result = await agent.run_async("query")
    return result

if __name__ == "__main__":
    result = asyncio.run(main())
```

**If you need to nest async calls:**
```python
# Use asyncio.create_task() instead
async def nested_calls():
    agent = GitHubAgent()
    
    # Run multiple queries concurrently
    tasks = [
        asyncio.create_task(agent.run_async("query 1")),
        asyncio.create_task(agent.run_async("query 2")),
    ]
    
    results = await asyncio.gather(*tasks)
    return results
```

**External Reference:** [AsyncIO Documentation](https://docs.python.org/3/library/asyncio.html)

---

### 5. langchain_core.messages.ToolMessage: Tool execution failed

**Error:**
```
langchain_core.messages.ToolMessage: Tool 'read_repository' execution failed: 
Repository not found
```

**Cause:** Tool received invalid input or encountered runtime error.

**Solution:**

1. **Enable debug logging to see tool inputs:**
   ```python
   import logging
   
   # Enable DEBUG level for tool execution
   logging.basicConfig(level=logging.DEBUG)
   logger = logging.getLogger("agents.github_agent")
   logger.setLevel(logging.DEBUG)
   
   # Now run agent and see detailed logs
   agent = GitHubAgent()
   result = agent.run("Read repository microsoft/vscode")
   ```

2. **Check tool validation:**
   ```python
   # From tools/github_tools.py
   from tools.github_tools import ReadRepositoryInput
   
   # Validate input before passing to agent
   try:
       validated = ReadRepositoryInput(
           owner="microsoft",
           repo="vscode"
       )
       print(f"✓ Valid input: {validated}")
   except Exception as e:
       print(f"✗ Invalid input: {e}")
   ```

3. **Test tools independently:**
   ```python
   from tools.github_tools import get_tools
   
   tools = get_tools()
   read_tool = next(t for t in tools if t.name == "read_repository")
   
   # Direct tool invocation
   result = read_tool.invoke({
       "owner": "microsoft",
       "repo": "vscode"
   })
   print(result)
   ```

---

### 6. TypeError: 'NoneType' object is not iterable

**Error:**
```
TypeError: 'NoneType' object is not iterable
  File "agents/github_agent.py", line 120, in stream
    async for chunk in stream:
```

**Cause:** Agent stream returned None instead of iterator.

**Solution:**

1. **Check agent initialization:**
   ```python
   # Ensure agent is properly initialized
   agent = GitHubAgent()
   
   # Verify agent.agent exists
   if agent.agent is None:
       print("❌ Agent not initialized")
   else:
       print("✓ Agent initialized")
   ```

2. **Verify stream is created:**
   ```python
   async def debug_stream():
       agent = GitHubAgent()
       config = {"configurable": {"thread_id": "test"}}
       
       # Check if astream_events exists
       if not hasattr(agent.agent, 'astream_events'):
           print("❌ Agent doesn't support streaming")
           return
       
       # Create stream
       stream = agent.agent.astream_events(
           {"messages": [("user", "test")]},
           config,
           version="v2"
       )
       
       print(f"✓ Stream created: {type(stream)}")
       
       # Try to consume
       async for event in stream:
           print(f"Event: {event['event']}")
   ```

**Code from project showing correct usage:**
```python
# From agents/github_agent.py - stream() method
async def stream(
    self,
    query: str,
    thread_id: str = "default",
    checkpoint: bool = True
) -> AsyncIterator[Dict[str, Any]]:
    """Stream agent execution with real-time updates."""
    config = {"configurable": {"thread_id": thread_id}}
    
    # Create async stream
    stream = self.agent.astream_events(
        {"messages": [("user", query)]},
        config,
        version="v2"
    )
    
    # Iterate over events
    async for event in stream:
        yield self._format_stream_event(event)
```

---

## Installation Issues

### Issue: pip install fails with dependency conflicts

**Symptoms:**
```
ERROR: Cannot install langchain and langgraph because these package 
versions have conflicting dependencies.
```

**Solutions:**

1. **Use clean virtual environment:**
   ```bash
   # Remove old environment
   rm -rf .venv
   
   # Create fresh environment
   python3.11 -m venv .venv
   source .venv/bin/activate
   
   # Upgrade pip first
   pip install --upgrade pip setuptools wheel
   
   # Install dependencies
   pip install -r requirements-production.txt
   ```

2. **Install in specific order:**
   ```bash
   # Install core dependencies first
   pip install langchain-core==0.3.29
   pip install langgraph==0.2.62
   
   # Then install remaining
   pip install -r requirements-production.txt
   ```

3. **Check for conflicting packages:**
   ```bash
   # List all installed packages
   pip list
   
   # Look for multiple versions or conflicts
   pip check
   ```

**External Reference:** [pip Dependency Resolution](https://pip.pypa.io/en/stable/topics/dependency-resolution/)

---

### Issue: Python version incompatibility

**Symptoms:**
```
SyntaxError: invalid syntax (pattern matching requires Python 3.10+)
```

**Solution:**

1. **Check Python version:**
   ```bash
   python --version  # Must be 3.11+
   ```

2. **Install correct Python version:**
   
   **macOS (using Homebrew):**
   ```bash
   brew install python@3.11
   python3.11 -m venv .venv
   ```
   
   **Ubuntu/Debian:**
   ```bash
   sudo apt update
   sudo apt install python3.11 python3.11-venv
   python3.11 -m venv .venv
   ```
   
   **Windows:**
   - Download from [python.org](https://www.python.org/downloads/)
   - Install and use `py -3.11 -m venv .venv`

**External Reference:** [Python 3.11 Release Notes](https://docs.python.org/3.11/whatsnew/3.11.html)

---

## API and Authentication Errors

### Issue: Rate limiting errors

**Error:**
```
google.api_core.exceptions.ResourceExhausted: 429 Quota exceeded for quota 
metric 'GenerateContent requests per minute'
```

**Solutions:**

1. **Implement exponential backoff:**
   ```python
   # From config.py - already configured
   max_retries: int = Field(
       default=3,
       description="Maximum number of retry attempts"
   )
   
   retry_min_seconds: int = Field(
       default=1,
       description="Minimum seconds between retries"
   )
   
   retry_max_seconds: int = Field(
       default=10,
       description="Maximum seconds between retries"
   )
   ```

2. **Add rate limiting to your code:**
   ```python
   import asyncio
   from typing import List
   
   class RateLimiter:
       def __init__(self, max_requests_per_minute: int = 10):
           self.max_requests = max_requests_per_minute
           self.requests = []
       
       async def acquire(self):
           """Wait if rate limit would be exceeded."""
           now = asyncio.get_event_loop().time()
           
           # Remove requests older than 1 minute
           self.requests = [req for req in self.requests if now - req < 60]
           
           # Wait if at limit
           if len(self.requests) >= self.max_requests:
               wait_time = 60 - (now - self.requests[0])
               await asyncio.sleep(wait_time)
               self.requests = []
           
           self.requests.append(now)
   
   # Usage
   rate_limiter = RateLimiter(max_requests_per_minute=10)
   
   async def call_api(query: str):
       await rate_limiter.acquire()
       agent = GitHubAgent()
       return await agent.run_async(query)
   ```

3. **Batch requests:**
   ```python
   # Instead of many small requests
   queries = ["query1", "query2", "query3"]
   
   # Combine into one request
   combined_query = "Please answer these questions:\n" + "\n".join(
       f"{i+1}. {q}" for i, q in enumerate(queries)
   )
   
   result = agent.run(combined_query)
   ```

**External Reference:** [Google AI Rate Limits](https://ai.google.dev/gemini-api/docs/quota)

---

## Agent Execution Problems

### Issue: Agent doesn't call tools

**Symptoms:**
Agent responds with generic text instead of using available tools.

**Diagnosis:**

1. **Check tools are passed to agent:**
   ```python
   from agents.github_agent import GitHubAgent
   
   agent = GitHubAgent()
   
   # Verify tools are registered
   print(f"Tools available: {[t.name for t in agent.tools]}")
   # Should show: ['read_repository', 'clone_repository']
   ```

2. **Check tool descriptions:**
   ```python
   from tools.github_tools import get_tools
   
   tools = get_tools()
   for tool in tools:
       print(f"\nTool: {tool.name}")
       print(f"Description: {tool.description}")
       print(f"Args: {tool.args}")
   ```

**Solutions:**

1. **Improve tool descriptions:**
   ```python
   # In tools/github_tools.py
   @tool
   def read_repository(owner: str, repo: str) -> str:
       """
       Read and analyze a GitHub repository.
       
       Use this tool when the user asks to:
       - "Analyze repository X"
       - "What's in the repo Y?"
       - "Show me repository Z"
       - "Read repository owner/name"
       
       Args:
           owner: Repository owner username (e.g., 'microsoft')
           repo: Repository name (e.g., 'vscode')
       
       Returns:
           Repository analysis including languages, structure, and details.
       """
       # ... implementation
   ```

2. **Use more specific queries:**
   ```python
   # ❌ Vague query - agent may not use tools
   result = agent.run("Tell me about VSCode")
   
   # ✓ Specific query - triggers tool usage
   result = agent.run("Read the repository microsoft/vscode")
   ```

3. **Force tool usage with system prompt:**
   ```python
   # Modify agent initialization
   from langchain_core.prompts import ChatPromptTemplate
   
   system_prompt = """You are a GitHub repository analyzer.
   
   ALWAYS use the available tools to answer questions:
   - Use 'read_repository' when user asks about a repository
   - Use 'clone_repository' when user wants to download a repository
   
   Never make up information - always use tools to get real data."""
   
   prompt = ChatPromptTemplate.from_messages([
       ("system", system_prompt),
       ("placeholder", "{messages}"),
   ])
   
   # Pass to agent (would need to modify agent creation)
   ```

---

### Issue: Agent gets stuck in infinite loop

**Symptoms:**
Agent keeps calling the same tool repeatedly without making progress.

**Diagnosis:**

Enable detailed logging to see the loop:
```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

agent = GitHubAgent()
result = agent.run("Your query here")
```

**Solutions:**

1. **Set max iterations (LangGraph handles this automatically):**
   ```python
   # LangGraph's create_react_agent has built-in recursion limits
   # Default is reasonable, but you can modify if needed
   
   from langgraph.prebuilt import create_react_agent
   
   agent = create_react_agent(
       llm,
       tools,
       state_modifier=system_prompt,
       # LangGraph automatically prevents infinite loops
   )
   ```

2. **Add timeout to agent execution:**
   ```python
   import asyncio
   from asyncio import TimeoutError
   
   async def run_with_timeout(query: str, timeout: int = 30):
       """Run agent with timeout."""
       agent = GitHubAgent()
       
       try:
           result = await asyncio.wait_for(
               agent.run_async(query),
               timeout=timeout
           )
           return result
       except TimeoutError:
           return {"error": f"Agent exceeded {timeout}s timeout"}
   
   # Usage
   result = asyncio.run(run_with_timeout("query", timeout=30))
   ```

3. **Fix tool outputs:**
   ```python
   # Ensure tools return complete, parseable responses
   @tool
   def my_tool(param: str) -> str:
       """Tool description."""
       try:
           result = do_something(param)
           
           # ✓ Return clear, complete response
           return f"Successfully completed: {result}"
           
       except Exception as e:
           # ✓ Return clear error message
           return f"Error: {str(e)}"
           
       # ❌ Never return None or empty string
       # return None  # This can cause loops!
   ```

---

## Streaming Issues

### Issue: Streaming doesn't work / no events received

**Symptoms:**
```python
async for event in agent.stream("query"):
    print(event)  # Nothing prints
```

**Diagnosis:**

1. **Verify async context:**
   ```python
   # ❌ Can't use streaming in sync code
   for event in agent.stream("query"):  # TypeError!
       print(event)
   
   # ✓ Must use async
   async def test_stream():
       async for event in agent.stream("query"):
           print(event)
   
   asyncio.run(test_stream())
   ```

2. **Check event filtering:**
   ```python
   # Full debug - see ALL events
   async def debug_stream():
       agent = GitHubAgent()
       config = {"configurable": {"thread_id": "debug"}}
       
       stream = agent.agent.astream_events(
           {"messages": [("user", "test")]},
           config,
           version="v2"
       )
       
       event_count = 0
       async for event in stream:
           event_count += 1
           print(f"Event {event_count}: {event['event']}")
           print(f"  Data: {event.get('data', {})}")
       
       print(f"Total events: {event_count}")
   
   asyncio.run(debug_stream())
   ```

**Solutions:**

1. **Use correct FastAPI endpoint:**
   ```python
   # api_server.py - streaming endpoint
   from fastapi.responses import StreamingResponse
   
   @app.post("/agent/stream")
   async def stream_agent(request: AgentRequest):
       """Stream agent execution with Server-Sent Events."""
       
       async def event_generator():
           agent = GitHubAgent()
           
           async for event in agent.stream(
               request.query,
               thread_id=request.thread_id
           ):
               # Format as SSE
               yield f"data: {json.dumps(event)}\n\n"
       
       return StreamingResponse(
           event_generator(),
           media_type="text/event-stream"
       )
   ```

2. **Client-side SSE consumption:**
   ```javascript
   // JavaScript client example
   const eventSource = new EventSource('/agent/stream', {
       method: 'POST',
       body: JSON.stringify({
           query: "Read repository microsoft/vscode",
           thread_id: "user-123"
       })
   });
   
   eventSource.onmessage = (event) => {
       const data = JSON.parse(event.data);
       console.log('Event:', data);
       
       if (data.type === 'end') {
           eventSource.close();
       }
   };
   
   eventSource.onerror = (error) => {
       console.error('Stream error:', error);
       eventSource.close();
   };
   ```

3. **Python client for SSE:**
   ```python
   import httpx
   import json
   
   async def consume_stream():
       async with httpx.AsyncClient() as client:
           async with client.stream(
               "POST",
               "http://localhost:8000/agent/stream",
               json={
                   "query": "Read repository microsoft/vscode",
                   "thread_id": "user-123"
               },
               timeout=60.0
           ) as response:
               async for line in response.aiter_lines():
                   if line.startswith("data: "):
                       data = json.loads(line[6:])
                       print(f"Event: {data}")
   
   asyncio.run(consume_stream())
   ```

**External Reference:** [Server-Sent Events Specification](https://html.spec.whatwg.org/multipage/server-sent-events.html)

---

## Performance Problems

### Issue: Agent responses are too slow

**Symptoms:**
Queries take 10-30 seconds to complete.

**Diagnosis:**

1. **Profile execution time:**
   ```python
   import time
   from agents.github_agent import GitHubAgent
   
   agent = GitHubAgent()
   
   start = time.time()
   result = agent.run("Read repository microsoft/vscode")
   end = time.time()
   
   print(f"Execution time: {end - start:.2f}s")
   ```

2. **Check model configuration:**
   ```python
   from config import get_settings
   
   settings = get_settings()
   print(f"Model: {settings.model_name}")
   print(f"Temperature: {settings.temperature}")
   print(f"Max tokens: {settings.max_tokens}")
   ```

**Solutions:**

1. **Use faster model:**
   ```python
   # In config.py or .env
   # gemini-2.0-flash-exp is faster than gemini-1.5-pro
   model_name: str = "gemini-2.0-flash-exp"
   ```

2. **Optimize temperature and tokens:**
   ```python
   # Lower temperature = faster, more deterministic
   temperature: float = 0.0  # vs 0.7
   
   # Limit max tokens for shorter responses
   max_tokens: int = 1024  # vs 4096
   ```

3. **Use async for concurrent requests:**
   ```python
   import asyncio
   from agents.github_agent import GitHubAgent
   
   async def process_multiple_repos():
       agent = GitHubAgent()
       
       # ❌ Sequential - takes 3x time
       # result1 = await agent.run_async("repo1")
       # result2 = await agent.run_async("repo2")
       # result3 = await agent.run_async("repo3")
       
       # ✓ Concurrent - much faster!
       tasks = [
           agent.run_async("Read repository microsoft/vscode"),
           agent.run_async("Read repository facebook/react"),
           agent.run_async("Read repository vercel/next.js"),
       ]
       
       results = await asyncio.gather(*tasks)
       return results
   
   # Run concurrently
   results = asyncio.run(process_multiple_repos())
   ```

4. **Add caching:**
   ```python
   from functools import lru_cache
   import hashlib
   
   class CachedAgent:
       def __init__(self):
           self.agent = GitHubAgent()
           self.cache = {}
       
       def _cache_key(self, query: str) -> str:
           """Generate cache key from query."""
           return hashlib.md5(query.encode()).hexdigest()
       
       def run(self, query: str) -> Dict[str, Any]:
           """Run with caching."""
           key = self._cache_key(query)
           
           if key in self.cache:
               print("Cache hit!")
               return self.cache[key]
           
           print("Cache miss - executing...")
           result = self.agent.run(query)
           self.cache[key] = result
           return result
   
   # Usage
   cached_agent = CachedAgent()
   result1 = cached_agent.run("query")  # Slow
   result2 = cached_agent.run("query")  # Fast (cached)
   ```

**External Reference:** [Python asyncio Performance](https://docs.python.org/3/library/asyncio-task.html#running-tasks-concurrently)

---

## Testing Failures

### Issue: Tests fail with "fixture not found"

**Error:**
```
fixture 'mock_llm' not found
```

**Solution:**

1. **Ensure conftest.py is present:**
   ```bash
   # Check file exists
   ls tests/conftest.py
   ```

2. **Verify pytest can find fixtures:**
   ```bash
   # List all available fixtures
   pytest --fixtures
   ```

3. **Check conftest.py content:**
   ```python
   # tests/conftest.py
   import pytest
   from unittest.mock import Mock, AsyncMock
   
   @pytest.fixture
   def mock_llm():
       """Mock LLM for testing."""
       mock = Mock()
       mock.invoke.return_value = "Mocked response"
       return mock
   
   @pytest.fixture
   def mock_async_llm():
       """Mock async LLM for testing."""
       mock = AsyncMock()
       mock.ainvoke.return_value = "Mocked async response"
       return mock
   ```

**External Reference:** [Pytest Fixtures](https://docs.pytest.org/en/stable/fixture.html)

---

### Issue: Async tests fail

**Error:**
```
TypeError: 'coroutine' object is not callable
```

**Solution:**

Use pytest-asyncio:

```python
# tests/test_async_agent.py
import pytest
from agents.github_agent import GitHubAgent

# Mark test as async
@pytest.mark.asyncio
async def test_async_run():
    """Test async agent execution."""
    agent = GitHubAgent()
    
    result = await agent.run_async("test query")
    
    assert result is not None
    assert "output" in result

# Test concurrent execution
@pytest.mark.asyncio
async def test_concurrent_execution():
    """Test multiple concurrent queries."""
    import asyncio
    
    agent = GitHubAgent()
    
    tasks = [
        agent.run_async("query 1"),
        agent.run_async("query 2"),
    ]
    
    results = await asyncio.gather(*tasks)
    
    assert len(results) == 2
    assert all(r is not None for r in results)
```

Install pytest-asyncio:
```bash
pip install pytest-asyncio
```

---

## Debugging Techniques

### Technique 1: Enable Comprehensive Logging

```python
# debug_logging.py
import logging
import sys

def setup_debug_logging():
    """Configure comprehensive debug logging."""
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    
    # File handler
    file_handler = logging.FileHandler('debug.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    # Set specific loggers
    logging.getLogger("agents.github_agent").setLevel(logging.DEBUG)
    logging.getLogger("tools.github_tools").setLevel(logging.DEBUG)
    logging.getLogger("langchain").setLevel(logging.INFO)  # Too verbose at DEBUG
    logging.getLogger("httpx").setLevel(logging.WARNING)

# Usage in main.py
if __name__ == "__main__":
    setup_debug_logging()
    
    from agents.github_agent import GitHubAgent
    agent = GitHubAgent()
    result = agent.run("test query")
```

---

### Technique 2: Interactive Debugging with pdb

```python
# Use Python debugger
import pdb

def debug_agent():
    from agents.github_agent import GitHubAgent
    
    agent = GitHubAgent()
    
    # Set breakpoint
    pdb.set_trace()  # Execution pauses here
    
    result = agent.run("test query")
    return result

# Or use breakpoint() (Python 3.7+)
def debug_agent_modern():
    from agents.github_agent import GitHubAgent
    
    agent = GitHubAgent()
    
    breakpoint()  # Modern way to set breakpoint
    
    result = agent.run("test query")
    return result
```

**pdb commands:**
- `n` (next): Execute next line
- `s` (step): Step into function
- `c` (continue): Continue execution
- `l` (list): Show current code
- `p variable`: Print variable value
- `pp variable`: Pretty-print variable
- `q` (quit): Exit debugger

**External Reference:** [Python pdb Documentation](https://docs.python.org/3/library/pdb.html)

---

### Technique 3: Inspect Agent State

```python
def inspect_agent_state():
    """Inspect internal agent state for debugging."""
    from agents.github_agent import GitHubAgent
    
    agent = GitHubAgent()
    
    # Check LLM configuration
    print("=== LLM Configuration ===")
    print(f"Model: {agent.llm.model_name}")
    print(f"Temperature: {agent.llm.temperature}")
    
    # Check tools
    print("\n=== Tools ===")
    for tool in agent.tools:
        print(f"- {tool.name}: {tool.description[:50]}...")
    
    # Check agent type
    print("\n=== Agent ===")
    print(f"Type: {type(agent.agent)}")
    print(f"Has checkpointer: {agent.checkpointer is not None}")
    
    # Try a query with detailed output
    print("\n=== Executing Query ===")
    result = agent.run("test query")
    
    print("\n=== Result ===")
    print(f"Type: {type(result)}")
    print(f"Keys: {result.keys() if isinstance(result, dict) else 'N/A'}")
    print(f"Messages: {len(result.get('messages', []))}")
    
    return result

if __name__ == "__main__":
    inspect_agent_state()
```

---

### Technique 4: Mock External Dependencies

```python
# tests/test_with_mocks.py
import pytest
from unittest.mock import Mock, patch, AsyncMock

def test_agent_with_mock_llm():
    """Test agent with mocked LLM to avoid API calls."""
    
    # Create mock LLM
    mock_llm = Mock()
    mock_llm.invoke.return_value = {
        "content": "Mocked response"
    }
    
    # Patch LLM initialization
    with patch("agents.github_agent.ChatGoogleGenerativeAI", return_value=mock_llm):
        from agents.github_agent import GitHubAgent
        
        agent = GitHubAgent()
        result = agent.run("test query")
        
        # Verify mock was called
        assert mock_llm.invoke.called
        print(f"LLM called with: {mock_llm.invoke.call_args}")

@pytest.mark.asyncio
async def test_async_agent_with_mock():
    """Test async agent with mocked async LLM."""
    
    mock_llm = AsyncMock()
    mock_llm.ainvoke.return_value = {
        "content": "Async mocked response"
    }
    
    with patch("agents.github_agent.ChatGoogleGenerativeAI", return_value=mock_llm):
        from agents.github_agent import GitHubAgent
        
        agent = GitHubAgent()
        result = await agent.run_async("test query")
        
        assert mock_llm.ainvoke.called
```

**External Reference:** [unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)

---

## Environment Issues

### Issue: .env file not loaded

**Symptoms:**
Environment variables from .env file are None.

**Diagnosis:**

```python
# test_env.py
import os
from dotenv import load_dotenv

print(f"Before load_dotenv:")
print(f"  GOOGLE_API_KEY: {os.getenv('GOOGLE_API_KEY')}")

load_dotenv()

print(f"\nAfter load_dotenv:")
print(f"  GOOGLE_API_KEY: {os.getenv('GOOGLE_API_KEY')}")

# Check .env file location
from pathlib import Path
env_path = Path(".env")
print(f"\n.env exists: {env_path.exists()}")
print(f".env path: {env_path.absolute()}")
```

**Solutions:**

1. **Ensure .env is in correct location:**
   ```bash
   # .env should be in project root
   CodeBaseOpsAI-v3/
   ├── .env          # ✓ Here
   ├── agents/
   ├── tools/
   └── main.py
   
   # Not in subdirectories
   CodeBaseOpsAI-v3/
   ├── agents/
   │   └── .env      # ✗ Wrong location
   ```

2. **Specify .env path explicitly:**
   ```python
   from dotenv import load_dotenv
   from pathlib import Path
   
   # Get project root
   project_root = Path(__file__).parent
   env_path = project_root / ".env"
   
   # Load with explicit path
   load_dotenv(dotenv_path=env_path)
   ```

3. **Check .env file format:**
   ```bash
   # ✓ Correct format
   GOOGLE_API_KEY=AIzaSyD...
   MODEL_NAME=gemini-2.0-flash-exp
   
   # ✗ Incorrect formats
   GOOGLE_API_KEY="AIzaSyD..."  # Don't use quotes
   GOOGLE_API_KEY = AIzaSyD...  # No spaces around =
   export GOOGLE_API_KEY=...    # Don't use 'export'
   ```

---

### Issue: Virtual environment not activated

**Symptoms:**
Using system Python instead of project Python.

**Diagnosis:**

```bash
# Check which Python is active
which python
# Should show: /path/to/CodeBaseOpsAI-v3/.venv/bin/python
# Not: /usr/bin/python or /usr/local/bin/python

# Check if in virtual environment
echo $VIRTUAL_ENV
# Should show: /path/to/CodeBaseOpsAI-v3/.venv
```

**Solution:**

```bash
# Activate virtual environment
cd CodeBaseOpsAI-v3

# macOS/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate

# Verify activation
which python  # Should show .venv path
python --version  # Should show correct version
```

**Add to .bashrc or .zshrc for auto-activation:**
```bash
# Add to ~/.zshrc
function codebase() {
    cd ~/Projects/python/labs/AI-hands-on/CodeBaseOpsAI-v3
    source .venv/bin/activate
}

# Usage: just type 'codebase' to activate
```

---

## Docker and Deployment Issues

### Issue: Docker build fails

**Error:**
```
ERROR [stage-0 5/7] RUN pip install -r requirements-production.txt
```

**Solutions:**

1. **Check Docker is installed:**
   ```bash
   docker --version
   docker-compose --version
   ```

2. **Verify Dockerfile syntax:**
   ```dockerfile
   # Dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   
   # Install dependencies first (caching layer)
   COPY requirements-production.txt .
   RUN pip install --no-cache-dir -r requirements-production.txt
   
   # Copy application code
   COPY . .
   
   CMD ["python", "main.py"]
   ```

3. **Build with no cache:**
   ```bash
   docker build --no-cache -t codebaseops:latest .
   ```

4. **Check .dockerignore:**
   ```
   # .dockerignore
   .venv/
   __pycache__/
   *.pyc
   .env
   .git/
   tests/
   *.md
   ```

---

### Issue: Container can't access API key

**Symptoms:**
Container starts but API calls fail with "API key not valid".

**Solution:**

1. **Pass environment variables to container:**
   ```bash
   # Using docker run
   docker run -e GOOGLE_API_KEY=your-key-here codebaseops:latest
   
   # Using .env file
   docker run --env-file .env codebaseops:latest
   ```

2. **docker-compose.yml:**
   ```yaml
   version: '3.8'
   
   services:
     api:
       build: .
       ports:
         - "8000:8000"
       environment:
         - GOOGLE_API_KEY=${GOOGLE_API_KEY}
       # Or use env_file
       env_file:
         - .env
   ```

3. **Verify in container:**
   ```bash
   # Start container shell
   docker run -it --entrypoint /bin/bash codebaseops:latest
   
   # Inside container
   echo $GOOGLE_API_KEY
   python -c "import os; print(os.getenv('GOOGLE_API_KEY'))"
   ```

**External Reference:** [Docker Environment Variables](https://docs.docker.com/engine/reference/commandline/run/#env)

---

## Advanced Debugging

### Trace Tool Calls

```python
# trace_tools.py
from typing import Dict, Any
import json

class ToolTracer:
    """Trace all tool calls for debugging."""
    
    def __init__(self):
        self.calls = []
    
    def wrap_tool(self, tool):
        """Wrap a tool to trace its calls."""
        original_func = tool.func
        
        def traced_func(*args, **kwargs):
            call_info = {
                "tool": tool.name,
                "args": args,
                "kwargs": kwargs,
                "timestamp": time.time()
            }
            
            try:
                result = original_func(*args, **kwargs)
                call_info["result"] = str(result)[:100]  # First 100 chars
                call_info["success"] = True
            except Exception as e:
                call_info["error"] = str(e)
                call_info["success"] = False
                raise
            finally:
                self.calls.append(call_info)
            
            return result
        
        tool.func = traced_func
        return tool
    
    def print_trace(self):
        """Print call trace."""
        print("\n=== Tool Call Trace ===")
        for i, call in enumerate(self.calls, 1):
            print(f"\n{i}. {call['tool']}")
            print(f"   Args: {call.get('args', 'N/A')}")
            print(f"   Kwargs: {call.get('kwargs', 'N/A')}")
            print(f"   Success: {call.get('success', 'N/A')}")
            if 'result' in call:
                print(f"   Result: {call['result']}")
            if 'error' in call:
                print(f"   Error: {call['error']}")

# Usage
tracer = ToolTracer()

from tools.github_tools import get_tools
tools = [tracer.wrap_tool(t) for t in get_tools()]

from agents.github_agent import GitHubAgent
agent = GitHubAgent()
agent.tools = tools  # Use traced tools

result = agent.run("test query")

tracer.print_trace()
```

---

### Profile Memory Usage

```python
# memory_profiler.py
import tracemalloc
import asyncio

async def profile_agent_memory():
    """Profile memory usage of agent execution."""
    from agents.github_agent import GitHubAgent
    
    # Start tracing
    tracemalloc.start()
    
    # Take snapshot before
    snapshot1 = tracemalloc.take_snapshot()
    
    # Run agent
    agent = GitHubAgent()
    result = await agent.run_async("Read repository microsoft/vscode")
    
    # Take snapshot after
    snapshot2 = tracemalloc.take_snapshot()
    
    # Compare snapshots
    top_stats = snapshot2.compare_to(snapshot1, 'lineno')
    
    print("=== Top 10 Memory Allocations ===")
    for stat in top_stats[:10]:
        print(stat)
    
    # Get current memory usage
    current, peak = tracemalloc.get_traced_memory()
    print(f"\nCurrent memory usage: {current / 1024 / 1024:.2f} MB")
    print(f"Peak memory usage: {peak / 1024 / 1024:.2f} MB")
    
    tracemalloc.stop()

if __name__ == "__main__":
    asyncio.run(profile_agent_memory())
```

Install memory_profiler for more detailed profiling:
```bash
pip install memory-profiler

# Use decorator
from memory_profiler import profile

@profile
def my_function():
    # Your code here
    pass
```

**External Reference:** [tracemalloc Documentation](https://docs.python.org/3/library/tracemalloc.html)

---

## Getting Help

### Community Resources

- **LangChain Discord:** [discord.gg/langchain](https://discord.gg/langchain)
- **LangGraph GitHub:** [github.com/langchain-ai/langgraph](https://github.com/langchain-ai/langgraph)
- **Google AI Forum:** [discuss.ai.google.dev](https://discuss.ai.google.dev/)
- **Stack Overflow:** Tag questions with `langchain`, `langgraph`, `google-gemini`

### Filing Bug Reports

Include this information:
1. Python version: `python --version`
2. Package versions: `pip list | grep -E "lang|google"`
3. Minimal reproduction code
4. Full error traceback
5. Expected vs actual behavior

### Next Steps

If you've tried everything and still stuck:
1. Review [UNDERSTANDING.md](UNDERSTANDING.md) for conceptual issues
2. Check [ARCHITECTURE.md](../reference/ARCHITECTURE.md) for system design
3. Review [API_REFERENCE.md](../reference/API_REFERENCE.md) for API details
4. Ask in community forums with specific error details

---

**Document Information:**
- **Created:** January 2, 2026
- **Version:** 1.0
- **Lines:** 1,300+
- **Related:** [UNDERSTANDING.md](UNDERSTANDING.md), [FAQ.md](FAQ.md), [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md)
