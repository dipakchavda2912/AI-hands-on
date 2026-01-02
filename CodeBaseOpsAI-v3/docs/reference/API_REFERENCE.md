# API Reference Documentation

**Complete reference for all functions, classes, and methods in CodeBaseOpsAI-v3.**

---

## Table of Contents

1. [Agent API](#agent-api)
2. [Tools API](#tools-api)
3. [Configuration API](#configuration-api)
4. [REST API](#rest-api)
5. [Examples](#examples)

---

## Agent API

### Class: `GithubAgent`

**Location:** `agents/github_agent.py`

Production-grade agent for GitHub operations with state management, streaming, and error handling.

#### Constructor

```python
def __init__(
    self,
    tools: list,
    model_name: str = "gemini-2.0-flash-exp",
    temperature: float = 0.0,
    enable_checkpointing: bool = True
)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `tools` | `list` | *Required* | List of LangChain tools (from `GithubTools.get_tools()`) |
| `model_name` | `str` | `"gemini-2.0-flash-exp"` | Google AI model name. Options: `gemini-2.0-flash-exp`, `gemini-2.5-flash`, `gemini-1.5-pro` |
| `temperature` | `float` | `0.0` | Model temperature (0.0 = deterministic, 2.0 = creative). Range: 0.0-2.0 |
| `enable_checkpointing` | `bool` | `True` | Enable conversation state persistence |

**Raises:**
- `ValueError`: If `model_name` is not supported
- `ImportError`: If required packages not installed

**Example:**

```python
from tools.github_tools import GithubTools
from agents.github_agent import GithubAgent

tools = GithubTools().get_tools()
agent = GithubAgent(
    tools=tools,
    model_name="gemini-2.0-flash-exp",
    temperature=0.0,
    enable_checkpointing=True
)
```

**Internal State:**

```python
self.tools: list               # Provided tools
self.model_name: str           # LLM model name
self.model: ChatGoogleGenerativeAI  # LLM instance
self.checkpointer: MemorySaver # State persistence (or None)
self.agent: CompiledGraph      # LangGraph ReAct agent
```

---

#### Method: `run()`

Synchronous execution of agent request. Blocks until completion.

```python
def run(self, user_request: str) -> str
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `user_request` | `str` | Natural language request for the agent. Max length: ~2000 characters |

**Returns:**
- `str`: Agent's final response as plain text

**Raises:**
- `Exception`: Any error during execution (not caught)

**Use Cases:**
- Simple scripts and CLI tools
- Single-threaded applications
- Quick testing and debugging

**Example:**

```python
agent = GithubAgent(tools=tools)

# Simple request
result = agent.run("Read repository owner/repo")
print(result)
# Output: "Successfully read repository owner/repo. The repository contains..."

# Complex request
result = agent.run("""
    Read the repository dipakchavda2912/base-serverless on branch develop.
    Analyze all JavaScript and TypeScript files and provide a summary.
""")
print(result)
```

**Performance:**
- Execution time: 2-10 seconds (depends on LLM response time)
- Blocks the calling thread
- No concurrent execution possible

**Note:** For production APIs, use `run_async()` instead.

---

#### Method: `run_async()`

Asynchronous execution of agent request. Non-blocking, supports concurrency.

```python
async def run_async(
    self,
    user_request: str,
    thread_id: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `user_request` | `str` | *Required* | Natural language request |
| `thread_id` | `Optional[str]` | Auto-generated | Conversation thread identifier. Use same ID to continue conversations |
| `metadata` | `Optional[Dict[str, Any]]` | `None` | Custom tracking data (user_id, request_id, etc.) |

**Returns:**

`Dict[str, Any]` with the following structure:

**Success Response:**
```python
{
    "success": True,
    "output": str,              # Agent's response
    "error": None,
    "error_type": None,
    "thread_id": str,          # Thread ID (for continuing conversation)
    "execution_time": float,   # Seconds
    "timestamp": str,          # ISO 8601 format
    "metadata": dict           # Passed metadata
}
```

**Error Response:**
```python
{
    "success": False,
    "output": None,
    "error": str,              # Error message
    "error_type": str,         # Exception class name
    "thread_id": str,
    "execution_time": float,
    "timestamp": str,
    "metadata": dict
}
```

**Use Cases:**
- Web servers and REST APIs
- Concurrent request handling
- Production applications
- Background task processing

**Example 1: Single Request**

```python
import asyncio

async def main():
    agent = GithubAgent(tools=tools)
    
    result = await agent.run_async(
        user_request="Read repository owner/repo",
        thread_id="user_123_session",
        metadata={"user_id": "123", "source": "web_ui"}
    )
    
    if result["success"]:
        print(f"Response: {result['output']}")
        print(f"Execution time: {result['execution_time']:.2f}s")
    else:
        print(f"Error: {result['error']}")

asyncio.run(main())
```

**Example 2: Concurrent Requests**

```python
async def main():
    agent = GithubAgent(tools=tools)
    
    # Execute 3 requests concurrently
    results = await asyncio.gather(
        agent.run_async("Read repo A"),
        agent.run_async("Read repo B"),
        agent.run_async("Read repo C")
    )
    
    for i, result in enumerate(results, 1):
        print(f"Request {i}: {result['output'][:100]}...")

asyncio.run(main())
```

**Example 3: Conversation**

```python
async def main():
    agent = GithubAgent(tools=tools)
    thread_id = "conversation_123"
    
    # Turn 1
    result1 = await agent.run_async(
        "Read repository owner/repo",
        thread_id=thread_id
    )
    print(result1["output"])
    
    # Turn 2 (agent remembers context)
    result2 = await agent.run_async(
        "What files are in it?",
        thread_id=thread_id  # Same ID
    )
    print(result2["output"])
    
    # Turn 3
    result3 = await agent.run_async(
        "Clone it to /tmp/myrepo",
        thread_id=thread_id  # Same ID
    )
    print(result3["output"])

asyncio.run(main())
```

**Performance:**
- Execution time: 2-10 seconds per request
- Can handle 100+ concurrent requests
- Non-blocking I/O
- Memory efficient

---

#### Method: `stream()`

Stream agent execution events in real-time. Returns async iterator.

```python
async def stream(
    self,
    user_request: str,
    thread_id: Optional[str] = None
) -> AsyncIterator[Dict[str, Any]]
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `user_request` | `str` | *Required* | Natural language request |
| `thread_id` | `Optional[str]` | Auto-generated | Conversation thread identifier |

**Yields:**

`Dict[str, Any]` - Event objects as they occur

**Event Types:**

1. **agent_start** - Execution begins
   ```python
   {
       "type": "agent_start",
       "thread_id": str,
       "timestamp": str  # ISO 8601
   }
   ```

2. **tool_call** - Agent decides to use a tool
   ```python
   {
       "type": "tool_call",
       "tool": str,         # Tool name
       "inputs": dict,      # Tool inputs
       "timestamp": str
   }
   ```

3. **tool_result** - Tool execution completes
   ```python
   {
       "type": "tool_result",
       "tool": str,
       "output": str,       # Tool output (JSON string)
       "timestamp": str
   }
   ```

4. **agent_response** - Agent generates text
   ```python
   {
       "type": "agent_response",
       "content": str,      # Text chunk
       "timestamp": str
   }
   ```

5. **agent_end** - Execution complete
   ```python
   {
       "type": "agent_end",
       "final_output": str,
       "thread_id": str,
       "timestamp": str
   }
   ```

6. **error** - Error occurred
   ```python
   {
       "type": "error",
       "error": str,
       "error_type": str,
       "timestamp": str
   }
   ```

**Use Cases:**
- Chat UIs with real-time updates
- Progress indicators
- Long-running operations
- Debugging and monitoring

**Example 1: Basic Streaming**

```python
async def main():
    agent = GithubAgent(tools=tools)
    
    async for event in agent.stream("Read repository owner/repo"):
        print(f"[{event['type']}] {event}")

asyncio.run(main())

# Output:
# [agent_start] {'type': 'agent_start', 'thread_id': 'thread_...', ...}
# [tool_call] {'type': 'tool_call', 'tool': 'read_repository', ...}
# [tool_result] {'type': 'tool_result', 'output': '{"repository": ...}', ...}
# [agent_response] {'type': 'agent_response', 'content': 'Successfully...', ...}
# [agent_end] {'type': 'agent_end', 'final_output': '...', ...}
```

**Example 2: Chat UI Integration**

```python
async def chat_ui_handler(user_request: str):
    agent = GithubAgent(tools=tools)
    
    async for event in agent.stream(user_request):
        if event["type"] == "agent_start":
            show_spinner()
        
        elif event["type"] == "tool_call":
            update_status(f"Calling {event['tool']}...")
        
        elif event["type"] == "agent_response":
            append_to_chat_bubble(event["content"])
        
        elif event["type"] == "agent_end":
            hide_spinner()
            mark_complete()
        
        elif event["type"] == "error":
            hide_spinner()
            show_error(event["error"])
```

**Example 3: Server-Sent Events (SSE)**

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.post("/agent/stream")
async def stream_endpoint(request: dict):
    async def event_generator():
        agent = GithubAgent(tools=tools)
        
        async for event in agent.stream(request["request"]):
            # Format as SSE
            yield f"data: {json.dumps(event)}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )
```

**Performance:**
- First event: ~100ms
- Subsequent events: As they occur (real-time)
- Total time: Same as `run_async()`
- Memory: Constant (streaming, not buffering)

---

## Tools API

### Class: `GithubTools`

**Location:** `tools/github_tools.py`

Provides validated GitHub operation tools.

#### Constructor

```python
def __init__(self)
```

No parameters. Reads configuration from environment variables.

**Environment Variables Used:**
- `GITHUB_TOKEN`: Optional GitHub personal access token
- `GITHUB_API_URL`: GitHub API base URL (default: `https://api.github.com`)

**Example:**

```python
from tools.github_tools import GithubTools

tools_instance = GithubTools()
tools = tools_instance.get_tools()
```

---

#### Method: `get_tools()`

Returns list of configured tools for agent.

```python
def get_tools(self) -> List[StructuredTool]
```

**Returns:**
- `List[StructuredTool]`: List of LangChain tools

**Example:**

```python
tools = GithubTools().get_tools()

# tools = [
#     StructuredTool(name="read_repository", ...),
#     StructuredTool(name="clone_repository", ...)
# ]

# Use with agent
agent = GithubAgent(tools=tools)
```

---

### Tool: `read_repository`

Read and analyze a GitHub repository.

**Input Schema:** `ReadRepositoryInput`

```python
class ReadRepositoryInput(BaseModel):
    repository: str           # Required
    branch: str = "main"      # Optional
    clone_path: Optional[str] = None  # Optional
```

**Fields:**

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `repository` | `str` | Yes | - | GitHub repository in format `owner/repo` or full URL |
| `branch` | `str` | No | `"main"` | Branch name to read from |
| `clone_path` | `Optional[str]` | No | `None` | Local path for cloning. If None, uses temp directory |

**Validation:**
- `repository` is normalized from URL to `owner/repo` format
- Accepts: `owner/repo`, `https://github.com/owner/repo`, `https://github.com/owner/repo.git`

**Returns:**

JSON string with repository information:

```json
{
    "repository": "owner/repo",
    "branch": "main",
    "files": [
        {
            "file": "README.md",
            "content": "# Repository Title\n...",
            "sha": "abc123..."
        },
        {
            "file": "package.json",
            "content": "{\"name\": \"example\"}",
            "sha": "def456..."
        }
    ],
    "status": "success",
    "message": "Successfully read repository owner/repo"
}
```

**Error Response:**

```json
{
    "status": "error",
    "error": "Error message",
    "error_type": "GitHubAPIError",
    "repository": "owner/repo"
}
```

**Example (Direct Call):**

```python
from tools.github_tools import GithubTools, ReadRepositoryInput

tools_instance = GithubTools()

# Create input
input_data = ReadRepositoryInput(
    repository="dipakchavda2912/base-serverless",
    branch="develop"
)

# Call implementation directly
result = tools_instance._read_repository_impl(input_data)
print(result)
```

**Example (Agent Call):**

```python
agent = GithubAgent(tools=GithubTools().get_tools())

result = agent.run(
    "Read repository dipakchavda2912/base-serverless on branch develop"
)
# Agent automatically:
# 1. Parses request
# 2. Calls read_repository tool
# 3. Formats response
```

**Use Cases:**
- Analyze repository structure
- Get file contents before cloning
- Check repository metadata
- Validate repository exists

---

### Tool: `clone_repository`

Clone a GitHub repository to local filesystem.

**Input Schema:** `CloneRepositoryInput`

```python
class CloneRepositoryInput(BaseModel):
    repository: str                    # Required
    clone_path: str = "/tmp/repo"     # Optional
    branch: str = "main"              # Optional
```

**Fields:**

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `repository` | `str` | Yes | - | GitHub repository in format `owner/repo` or full URL |
| `clone_path` | `str` | No | `"/tmp/repo"` | Local filesystem path for cloning |
| `branch` | `str` | No | `"main"` | Branch to clone |

**Validation:**
- `repository` normalized to `owner/repo` format
- `clone_path` must be valid filesystem path

**Returns:**

JSON string with clone status:

```json
{
    "repository": "owner/repo",
    "clone_path": "/tmp/myrepo",
    "branch": "main",
    "status": "success",
    "message": "Repository cloned successfully to /tmp/myrepo"
}
```

**Error Response:**

```json
{
    "status": "error",
    "error": "Error message",
    "error_type": "GitCloneError",
    "repository": "owner/repo"
}
```

**Example:**

```python
agent = GithubAgent(tools=GithubTools().get_tools())

result = agent.run(
    "Clone repository owner/repo to /tmp/myrepo on branch develop"
)
```

**Use Cases:**
- Download repository for local analysis
- Prepare repository for processing
- Backup repository contents

---

## Configuration API

### Class: `AppConfig`

**Location:** `config.py`

Validated application configuration.

```python
from config import AppConfig

config = AppConfig()
```

**Configuration Fields:**

| Field | Type | Default | Validation | Description |
|-------|------|---------|------------|-------------|
| `model_name` | `str` | `"gemini-2.0-flash-exp"` | Must be in allowed list | LLM model name |
| `temperature` | `float` | `0.0` | 0.0 ≤ temp ≤ 2.0 | Model temperature |
| `max_retries` | `int` | `3` | ≥ 0 | Max retry attempts |
| `timeout` | `float` | `60.0` | > 0 | Request timeout (seconds) |
| `github_token` | `Optional[str]` | `None` | - | GitHub PAT |
| `github_api_url` | `str` | `"https://api.github.com"` | Valid URL | GitHub API base |
| `enable_checkpointing` | `bool` | `True` | - | Enable state persistence |
| `log_level` | `str` | `"INFO"` | Valid log level | Logging level |
| `api_host` | `str` | `"0.0.0.0"` | Valid IP | API server host |
| `api_port` | `int` | `8000` | 1 ≤ port < 65536 | API server port |
| `api_workers` | `int` | `4` | ≥ 1 | API worker processes |

**Example:**

```python
from config import AppConfig

# Load from environment
config = AppConfig()

# Use in agent
agent = GithubAgent(
    tools=tools,
    model_name=config.model_name,
    temperature=config.temperature
)

# Use in API server
uvicorn.run(
    "api_server:app",
    host=config.api_host,
    port=config.api_port,
    workers=config.api_workers
)
```

**Environment File (.env):**

```bash
# LLM Configuration
MODEL_NAME=gemini-2.0-flash-exp
TEMPERATURE=0.0
MAX_RETRIES=3
TIMEOUT=60.0

# API Keys
GOOGLE_API_KEY=your_key_here
GITHUB_TOKEN=ghp_your_token_here

# Agent Configuration
ENABLE_CHECKPOINTING=true
LOG_LEVEL=INFO

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4
```

---

## REST API

### Base URL

```
http://localhost:8000
```

### Endpoints

#### GET `/health`

Health check endpoint.

**Response:**

```json
{
    "status": "healthy",
    "timestamp": "2026-01-02T10:30:00.000000",
    "version": "2.0.0"
}
```

**Status Codes:**
- `200 OK`: Service is healthy

---

#### POST `/agent/run`

Execute agent request synchronously.

**Request Body:**

```json
{
    "request": "Read repository owner/repo",
    "thread_id": "user_123_session",  // Optional
    "metadata": {                      // Optional
        "user_id": "123",
        "source": "web_ui"
    }
}
```

**Response:**

```json
{
    "success": true,
    "output": "Successfully read repository...",
    "error": null,
    "error_type": null,
    "thread_id": "user_123_session",
    "execution_time": 2.34,
    "timestamp": "2026-01-02T10:30:00.000000"
}
```

**Status Codes:**
- `200 OK`: Request completed
- `500 Internal Server Error`: Execution failed

**curl Example:**

```bash
curl -X POST http://localhost:8000/agent/run \
  -H "Content-Type: application/json" \
  -d '{
    "request": "Read repository dipakchavda2912/base-serverless",
    "thread_id": "my_session"
  }'
```

---

#### POST `/agent/stream`

Stream agent execution with Server-Sent Events (SSE).

**Request Body:**

```json
{
    "request": "Read repository owner/repo",
    "thread_id": "user_123_session"  // Optional
}
```

**Response:** Server-Sent Events stream

```
data: {"type": "agent_start", "thread_id": "...", "timestamp": "..."}

data: {"type": "tool_call", "tool": "read_repository", "inputs": {...}}

data: {"type": "tool_result", "output": "{...}"}

data: {"type": "agent_response", "content": "Successfully..."}

data: {"type": "agent_end", "final_output": "..."}
```

**Status Codes:**
- `200 OK`: Stream started

**curl Example:**

```bash
curl -X POST http://localhost:8000/agent/stream \
  -H "Content-Type: application/json" \
  -d '{"request": "Read repository owner/repo"}' \
  --no-buffer
```

**JavaScript Example:**

```javascript
const eventSource = new EventSource(
    '/agent/stream',
    {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({request: 'Read repository owner/repo'})
    }
);

eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    if (data.type === 'agent_start') {
        showSpinner();
    } else if (data.type === 'agent_response') {
        appendToChat(data.content);
    } else if (data.type === 'agent_end') {
        hideSpinner();
    }
};
```

---

#### POST `/agent/background`

Execute agent in background (fire-and-forget).

**Request Body:**

```json
{
    "request": "Clone repository owner/repo to /tmp/myrepo",
    "metadata": {"user_id": "123"}
}
```

**Response:**

```json
{
    "task_id": "task_1704192000.123",
    "status": "queued",
    "message": "Task queued for execution"
}
```

**Status Codes:**
- `200 OK`: Task queued

**Use Cases:**
- Long-running operations
- Batch processing
- Operations that don't need immediate response

---

## Examples

### Example 1: Simple Usage

```python
from tools.github_tools import GithubTools
from agents.github_agent import GithubAgent

# Initialize
tools = GithubTools().get_tools()
agent = GithubAgent(tools=tools)

# Execute
result = agent.run("Read repository owner/repo")
print(result)
```

### Example 2: Async with Error Handling

```python
import asyncio
from agents.github_agent import GithubAgent
from tools.github_tools import GithubTools

async def main():
    tools = GithubTools().get_tools()
    agent = GithubAgent(tools=tools)
    
    result = await agent.run_async(
        user_request="Read repository owner/repo",
        thread_id="session_123",
        metadata={"user_id": "user_456"}
    )
    
    if result["success"]:
        print(f"✓ Success: {result['output']}")
        print(f"  Execution time: {result['execution_time']:.2f}s")
    else:
        print(f"✗ Error: {result['error']}")
        print(f"  Error type: {result['error_type']}")

asyncio.run(main())
```

### Example 3: Streaming

```python
import asyncio
from agents.github_agent import GithubAgent
from tools.github_tools import GithubTools

async def main():
    tools = GithubTools().get_tools()
    agent = GithubAgent(tools=tools)
    
    print("Starting agent...")
    
    async for event in agent.stream("Read repository owner/repo"):
        event_type = event["type"]
        
        if event_type == "agent_start":
            print("🚀 Agent started")
        
        elif event_type == "tool_call":
            print(f"🔧 Calling tool: {event['tool']}")
        
        elif event_type == "tool_result":
            print(f"📦 Tool result received")
        
        elif event_type == "agent_response":
            print(f"💬 Agent: {event['content']}")
        
        elif event_type == "agent_end":
            print("✅ Agent completed")
        
        elif event_type == "error":
            print(f"❌ Error: {event['error']}")

asyncio.run(main())
```

### Example 4: Multi-turn Conversation

```python
import asyncio
from agents.github_agent import GithubAgent
from tools.github_tools import GithubTools

async def conversation():
    tools = GithubTools().get_tools()
    agent = GithubAgent(tools=tools)
    thread_id = "conversation_123"
    
    # Turn 1
    result1 = await agent.run_async(
        "Read repository owner/repo",
        thread_id=thread_id
    )
    print(f"Turn 1: {result1['output']}\n")
    
    # Turn 2 - Agent remembers context
    result2 = await agent.run_async(
        "What files are in it?",
        thread_id=thread_id
    )
    print(f"Turn 2: {result2['output']}\n")
    
    # Turn 3 - Still in context
    result3 = await agent.run_async(
        "Clone it to /tmp/myrepo",
        thread_id=thread_id
    )
    print(f"Turn 3: {result3['output']}")

asyncio.run(conversation())
```

### Example 5: Using Configuration

```python
from config import AppConfig
from agents.github_agent import GithubAgent
from tools.github_tools import GithubTools

# Load configuration
config = AppConfig()

# Create agent with config
tools = GithubTools().get_tools()
agent = GithubAgent(
    tools=tools,
    model_name=config.model_name,
    temperature=config.temperature,
    enable_checkpointing=config.enable_checkpointing
)

# Use agent
result = agent.run("Read repository owner/repo")
print(result)
```

---

**End of API Reference**
