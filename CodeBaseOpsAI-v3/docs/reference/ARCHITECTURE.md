# CodeBaseOpsAI-v3 Architecture & Execution Flow Documentation

**Complete technical guide to understanding how the production-grade agent system works.**

---

## 📚 Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Deep Dive](#architecture-deep-dive)
3. [Execution Flows](#execution-flows)
4. [Core Components](#core-components)
5. [Function Reference](#function-reference)
6. [Design Patterns](#design-patterns)
7. [State Management](#state-management)
8. [Error Handling](#error-handling)

---

## 🎯 System Overview

### What is CodeBaseOpsAI-v3?

CodeBaseOpsAI-v3 is a **production-grade AI agent system** that can:
- Read and analyze GitHub repositories
- Clone repositories to local filesystem
- Maintain conversation context across multiple requests
- Handle concurrent requests asynchronously
- Stream responses in real-time
- Provide REST API for integration

### Why LangGraph Instead of LangChain Classic?

```
❌ LangChain Classic (Deprecated)          ✅ LangGraph (Modern 2026)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• No state management                     • Built-in state checkpointing
• No conversation memory                  • Redis/Postgres persistence
• Sequential execution only               • Async/await support
• Limited observability                   • Full LangSmith integration
• Hard to debug                           • Visual graph debugging
• No streaming support                    • Native streaming
• Monolithic architecture                 • Modular graph nodes
• Poor error recovery                     • Retry & fallback patterns
```

---

## 🏗️ Architecture Deep Dive

### Layer 1: API Layer (FastAPI)

**File:** `api_server.py`

The entry point for external requests. Provides three API patterns:

```python
┌─────────────────────────────────────────────────────┐
│                FastAPI Application                  │
├─────────────────────────────────────────────────────┤
│                                                     │
│  GET  /health          → Health check              │
│  POST /agent/run       → Sync execution            │
│  POST /agent/stream    → SSE streaming             │
│  POST /agent/background → Fire-and-forget          │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Significance:**
- Decouples agent logic from transport layer
- Enables horizontal scaling (multiple API workers)
- Provides OpenAPI documentation automatically
- Handles request validation via Pydantic models

### Layer 2: Agent Orchestration (LangGraph)

**File:** `agents/github_agent.py`

The brain of the system. Manages:

```python
┌─────────────────────────────────────────────────────┐
│              GithubAgent Class                      │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────────────────────────────────┐          │
│  │   LangGraph ReAct Agent             │          │
│  │   • State: Messages + Metadata      │          │
│  │   • Checkpointing: MemorySaver      │          │
│  │   • Tools: GitHub operations        │          │
│  └─────────────────────────────────────┘          │
│                    ↓                               │
│  ┌─────────────────────────────────────┐          │
│  │   Execution Methods                 │          │
│  │   • run()        → Sync             │          │
│  │   • run_async()  → Async            │          │
│  │   • stream()     → Streaming        │          │
│  │   • continue_conversation()         │          │
│  └─────────────────────────────────────┘          │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Significance:**
- **ReAct Pattern**: Reason → Act → Observe loop for intelligent decision-making
- **State Graphs**: Visual debugging of agent decision flow
- **Checkpointing**: Resume conversations from any point
- **Async Design**: Non-blocking I/O for scalability

### Layer 3: LLM Interface (Gemini)

**Configuration:** `config.py`

```python
┌─────────────────────────────────────────────────────┐
│        ChatGoogleGenerativeAI                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Model: gemini-2.0-flash-exp                       │
│  Features:                                          │
│    • Function calling (tool use)                   │
│    • Structured outputs                            │
│    • Token streaming                               │
│    • Context window: 1M tokens                     │
│    • Multimodal support                            │
│                                                     │
│  Production Settings:                              │
│    • Temperature: 0.0 (deterministic)              │
│    • Max retries: 3                                │
│    • Timeout: 60s                                  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Significance:**
- Function calling enables native tool use (better than ReAct prompts)
- Deterministic outputs (temp=0) for consistent behavior
- Auto-retry handles transient failures
- Timeout prevents hanging requests

### Layer 4: Tool Layer (GitHub Operations)

**File:** `tools/github_tools.py`

```python
┌─────────────────────────────────────────────────────┐
│              GithubTools Class                      │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────────────────────────────────┐          │
│  │  Pydantic Input Schemas             │          │
│  │  • ReadRepositoryInput              │          │
│  │  • CloneRepositoryInput             │          │
│  │  → Validates all inputs             │          │
│  └─────────────────────────────────────┘          │
│                    ↓                               │
│  ┌─────────────────────────────────────┐          │
│  │  StructuredTool Instances           │          │
│  │  • read_repository                  │          │
│  │  • clone_repository                 │          │
│  │  → Type-safe tool calling           │          │
│  └─────────────────────────────────────┘          │
│                    ↓                               │
│  ┌─────────────────────────────────────┐          │
│  │  Business Logic Functions           │          │
│  │  • _read_repository_impl()          │          │
│  │  • _clone_repository_impl()         │          │
│  │  → Actual GitHub operations         │          │
│  └─────────────────────────────────────┘          │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Significance:**
- **Pydantic Validation**: Catches errors before they reach the LLM
- **Separation of Concerns**: Schema → Interface → Implementation
- **Error Handling**: Try/except at each layer with detailed logging
- **Mock-friendly**: Easy to swap implementations for testing

---

## 🔄 Execution Flows

### Flow 1: Synchronous Execution

**Entry Point:** `main.py` → `example_sync()`

```python
┌───────────────────────────────────────────────────────────────┐
│  1. User Request                                              │
│     "Read repository X on branch Y"                           │
└───────────────────────────────────────────────────────────────┘
                            ↓
┌───────────────────────────────────────────────────────────────┐
│  2. Initialize Components                                     │
│     tools = GithubTools().get_tools()                        │
│     agent = GithubAgent(tools, model_name, ...)              │
└───────────────────────────────────────────────────────────────┘
                            ↓
┌───────────────────────────────────────────────────────────────┐
│  3. Agent Execution                                           │
│     result = agent.run(user_request)                         │
│                                                               │
│     Internal Steps:                                           │
│     a) Create HumanMessage with request                      │
│     b) Execute LangGraph agent.invoke()                      │
│     c) Agent enters ReAct loop:                              │
│        → Thought: What do I need to do?                      │
│        → Action: call read_repository tool                   │
│        → Observation: tool returns result                    │
│        → Thought: I have the answer                          │
│        → Final Answer: formatted response                    │
└───────────────────────────────────────────────────────────────┘
                            ↓
┌───────────────────────────────────────────────────────────────┐
│  4. Extract Response                                          │
│     output = result["messages"][-1].content                  │
└───────────────────────────────────────────────────────────────┘
                            ↓
┌───────────────────────────────────────────────────────────────┐
│  5. Return to User                                            │
│     print(output)                                             │
└───────────────────────────────────────────────────────────────┘
```

**Code Walkthrough:**

```python
# main.py - example_sync()
def example_sync():
    # Step 1: Create tools
    github_tools = GithubTools()
    tools = github_tools.get_tools()  # Returns [read_repository, clone_repository]
    
    # Step 2: Initialize agent
    agent = GithubAgent(
        tools=tools,
        model_name="gemini-2.0-flash-exp",
        temperature=0.0,
        enable_checkpointing=True
    )
    # ↑ This creates:
    #   - ChatGoogleGenerativeAI instance
    #   - MemorySaver for state persistence
    #   - LangGraph ReAct agent with tools
    
    # Step 3: Execute
    user_request = "Read repository 'owner/repo' on branch 'develop'"
    result = agent.run(user_request=user_request)
    # ↑ This:
    #   - Wraps request in HumanMessage
    #   - Calls agent.invoke() with configuration
    #   - LangGraph orchestrates ReAct loop
    #   - Returns final message
    
    # Step 4: Use result
    print(result)  # "Successfully read repository..."
```

### Flow 2: Asynchronous Execution

**Entry Point:** `main.py` → `example_async()`

```python
┌───────────────────────────────────────────────────────────────┐
│  1. Async Event Loop                                          │
│     asyncio.run(example_async())                             │
└───────────────────────────────────────────────────────────────┘
                            ↓
┌───────────────────────────────────────────────────────────────┐
│  2. Initialize Agent (same as sync)                           │
│     agent = GithubAgent(...)                                 │
└───────────────────────────────────────────────────────────────┘
                            ↓
┌───────────────────────────────────────────────────────────────┐
│  3. Async Execution                                           │
│     result = await agent.run_async(                          │
│         user_request="...",                                   │
│         thread_id="user_123",                                │
│         metadata={"user_id": "123"}                          │
│     )                                                         │
│                                                               │
│     Internal Steps:                                           │
│     a) Generate thread_id if not provided                    │
│     b) Create RunnableConfig with thread_id                  │
│     c) await agent.ainvoke() (async invoke)                 │
│     d) Extract final message                                 │
│     e) Return structured dict with metadata                  │
└───────────────────────────────────────────────────────────────┘
                            ↓
┌───────────────────────────────────────────────────────────────┐
│  4. Response Structure                                        │
│     {                                                         │
│         "success": True,                                      │
│         "output": "Repository analysis...",                  │
│         "thread_id": "user_123",                             │
│         "execution_time": 2.34,                              │
│         "timestamp": "2026-01-02T10:30:00Z"                  │
│     }                                                         │
└───────────────────────────────────────────────────────────────┘
```

**Why Async?**

```python
# Synchronous (blocking)
result1 = agent.run(request1)  # Wait 3s
result2 = agent.run(request2)  # Wait 3s
result3 = agent.run(request3)  # Wait 3s
# Total: 9 seconds

# Asynchronous (concurrent)
results = await asyncio.gather(
    agent.run_async(request1),  # All run
    agent.run_async(request2),  # in parallel
    agent.run_async(request3)
)
# Total: ~3 seconds (fastest request)
```

**Significance:**
- **Scalability**: Handle 100+ requests simultaneously
- **Non-blocking**: Other requests don't wait for slow operations
- **Resource Efficient**: Single process, multiple concurrent operations
- **Production Ready**: FastAPI natively async

### Flow 3: Streaming Execution

**Entry Point:** `main.py` → `example_streaming()`

```python
┌───────────────────────────────────────────────────────────────┐
│  1. Start Streaming                                           │
│     async for chunk in agent.stream(user_request):           │
└───────────────────────────────────────────────────────────────┘
                            ↓
┌───────────────────────────────────────────────────────────────┐
│  2. Stream Events                                             │
│                                                               │
│     Event 1: {"type": "agent_start", ...}                    │
│              ↓ (print immediately)                            │
│                                                               │
│     Event 2: {"type": "tool_call", "tool": "read_repo"}     │
│              ↓ (print immediately)                            │
│                                                               │
│     Event 3: {"type": "tool_result", "output": "..."}       │
│              ↓ (print immediately)                            │
│                                                               │
│     Event 4: {"type": "agent_response", "content": "..."}   │
│              ↓ (print immediately)                            │
│                                                               │
│     Event 5: {"type": "agent_end", "final_output": "..."}   │
│              ↓ (print immediately)                            │
└───────────────────────────────────────────────────────────────┘
                            ↓
┌───────────────────────────────────────────────────────────────┐
│  3. User Sees Real-time Updates                               │
│     [10:30:01] Agent started...                              │
│     [10:30:02] Calling read_repository...                    │
│     [10:30:04] Tool returned: {"files": [...]}               │
│     [10:30:05] Agent thinking...                             │
│     [10:30:06] Final answer: Repository contains...          │
└───────────────────────────────────────────────────────────────┘
```

**Code Walkthrough:**

```python
# agents/github_agent.py - stream method
async def stream(
    self,
    user_request: str,
    thread_id: Optional[str] = None
) -> AsyncIterator[Dict[str, Any]]:
    """
    Stream agent execution in real-time.
    
    Yields events as they happen:
    - agent_start: Execution begins
    - tool_call: Agent decides to use a tool
    - tool_result: Tool execution completes
    - agent_response: Agent generates text
    - agent_end: Execution complete
    """
    thread_id = thread_id or f"thread_{datetime.utcnow().timestamp()}"
    
    config = RunnableConfig(
        configurable={"thread_id": thread_id}
    )
    
    # Stream from LangGraph
    async for event in self.agent.astream_events(
        {"messages": [HumanMessage(content=user_request)]},
        config=config,
        version="v2"  # Use streaming v2 API
    ):
        # Process different event types
        event_type = event.get("event", "")
        
        if event_type == "on_chat_model_start":
            yield {"type": "agent_start", "timestamp": datetime.utcnow().isoformat()}
        
        elif event_type == "on_tool_start":
            yield {
                "type": "tool_call",
                "tool": event.get("name"),
                "inputs": event.get("data", {}).get("input")
            }
        
        elif event_type == "on_tool_end":
            yield {
                "type": "tool_result",
                "tool": event.get("name"),
                "output": event.get("data", {}).get("output")
            }
        
        elif event_type == "on_chat_model_stream":
            chunk = event.get("data", {}).get("chunk")
            if chunk:
                yield {
                    "type": "agent_response",
                    "content": chunk.content
                }
```

**Why Streaming?**

```
Without Streaming:
User: "Analyze this repo"
[Wait 30 seconds...]
Agent: "Here's the complete analysis..."

With Streaming:
User: "Analyze this repo"
[Instant] Agent: "Starting analysis..."
[2s] Agent: "Reading files from main branch..."
[5s] Agent: "Found 47 files..."
[10s] Agent: "Analyzing package.json..."
[15s] Agent: "This is a Node.js project..."
[30s] Agent: "Complete analysis ready!"
```

**Significance:**
- **User Experience**: See progress instead of waiting
- **Early Termination**: Cancel if heading wrong direction
- **Debugging**: See exactly what agent is doing
- **Long Operations**: Keep user engaged during 30s+ tasks

### Flow 4: Conversation Continuation

**Entry Point:** `main.py` → `example_conversation()`

```python
┌───────────────────────────────────────────────────────────────┐
│  Turn 1: "Read repository X"                                  │
│                                                               │
│  State Graph:                                                 │
│  {                                                            │
│    "messages": [                                              │
│      HumanMessage("Read repository X"),                      │
│      AIMessage("Repository contains 47 files...")            │
│    ],                                                         │
│    "thread_id": "conv_123"                                   │
│  }                                                            │
└───────────────────────────────────────────────────────────────┘
                            ↓
┌───────────────────────────────────────────────────────────────┐
│  Turn 2: "What files are in it?" (with same thread_id)       │
│                                                               │
│  Agent has context from Turn 1!                               │
│  State Graph:                                                 │
│  {                                                            │
│    "messages": [                                              │
│      HumanMessage("Read repository X"),                      │
│      AIMessage("Repository contains 47 files..."),           │
│      HumanMessage("What files are in it?"),                  │
│      AIMessage("The files include: README.md, ...")          │
│    ],                                                         │
│    "thread_id": "conv_123"                                   │
│  }                                                            │
└───────────────────────────────────────────────────────────────┘
                            ↓
┌───────────────────────────────────────────────────────────────┐
│  Turn 3: "Clone it to /tmp/myrepo"                           │
│                                                               │
│  Agent remembers: repository name, branch, file list          │
│  Can make intelligent decisions based on conversation         │
└───────────────────────────────────────────────────────────────┘
```

**Code Example:**

```python
# First request - establish context
result1 = await agent.run_async(
    user_request="Read repository 'owner/repo'",
    thread_id="conv_123"  # ← Same ID for entire conversation
)

# Second request - agent has context
result2 = await agent.run_async(
    user_request="What's the main programming language?",
    thread_id="conv_123"  # ← Same ID
)
# Agent knows we're still talking about 'owner/repo'!

# Third request - continue conversation
result3 = await agent.run_async(
    user_request="Clone it to /tmp/myrepo",
    thread_id="conv_123"  # ← Same ID
)
# Agent knows which repo to clone without asking!
```

**How State Persistence Works:**

```python
# In GithubAgent.__init__
self.checkpointer = MemorySaver()  # Stores state in memory

# In run_async
config = RunnableConfig(
    configurable={"thread_id": thread_id}
)

# LangGraph automatically:
# 1. Loads previous messages for this thread_id
# 2. Appends new message
# 3. Saves updated state after execution

# State storage:
{
    "conv_123": {
        "messages": [...],
        "metadata": {...}
    },
    "conv_456": {
        "messages": [...],
        "metadata": {...}
    }
}
```

**Production State Storage:**

```python
# Development: MemorySaver (in-memory, lost on restart)
checkpointer = MemorySaver()

# Production: Redis (persistent, distributed)
from langgraph.checkpoint.redis import RedisSaver
checkpointer = RedisSaver(redis_url="redis://localhost:6379")

# Enterprise: Postgres (persistent, ACID, searchable)
from langgraph.checkpoint.postgres import PostgresSaver
checkpointer = PostgresSaver(postgres_url="postgresql://...")
```

---

## 🧩 Core Components

### 1. GithubAgent Class

**Location:** `agents/github_agent.py`

**Purpose:** Orchestrates the entire agent execution lifecycle.

**Key Methods:**

#### `__init__(tools, model_name, temperature, enable_checkpointing)`

```python
def __init__(
    self,
    tools: list,
    model_name: str = "gemini-2.0-flash-exp",
    temperature: float = 0.0,
    enable_checkpointing: bool = True
):
    """
    Initialize the agent with all components.
    
    This is where the magic happens:
    1. Creates the LLM client
    2. Sets up state persistence
    3. Builds the LangGraph agent
    """
    # 1. Store configuration
    self.tools = tools
    self.model_name = model_name
    
    # 2. Initialize LLM
    self.model = ChatGoogleGenerativeAI(
        model=model_name,
        temperature=temperature,
        max_retries=3,      # Auto-retry on transient failures
        timeout=60.0,       # Prevent hanging requests
    )
    
    # 3. Create checkpointer
    self.checkpointer = MemorySaver() if enable_checkpointing else None
    
    # 4. Build LangGraph agent
    self.agent = create_react_agent(
        model=self.model,
        tools=self.tools,
        checkpointer=self.checkpointer,  # Enables state persistence
    )
    
    logger.info(f"Initialized GithubAgent with model={model_name}")
```

**Significance:**
- **Lazy Initialization**: Only creates what's needed
- **Configuration Injection**: Easy to swap models/tools for testing
- **Production Defaults**: Retries, timeouts built-in
- **Observability**: Logs initialization for debugging

#### `run(user_request) -> str`

```python
def run(self, user_request: str) -> str:
    """
    Synchronous execution (blocks until complete).
    
    Use case: Simple scripts, CLI tools, single-threaded apps
    """
    # 1. Wrap request in LangChain message format
    result = self.agent.invoke(
        {"messages": [HumanMessage(content=user_request)]}
    )
    
    # 2. Extract final response
    final_message = result["messages"][-1]
    return final_message.content if hasattr(final_message, 'content') else str(final_message)
```

**Execution Timeline:**
```
0ms:  Function called
1ms:  Create HumanMessage
2ms:  Call agent.invoke()
      ↓
      [LangGraph ReAct Loop - 2-5 seconds]
      ↓
3000ms: Response ready
3001ms: Extract content
3002ms: Return string
```

#### `run_async(user_request, thread_id, metadata) -> Dict`

```python
async def run_async(
    self,
    user_request: str,
    thread_id: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Asynchronous execution (non-blocking).
    
    Use case: Web servers, concurrent requests, production APIs
    
    Returns structured dict instead of raw string for better
    integration with REST APIs and error handling.
    """
    start_time = datetime.utcnow()
    thread_id = thread_id or f"thread_{start_time.timestamp()}"
    
    try:
        logger.info(f"[{thread_id}] Starting async execution")
        
        # 1. Configure execution
        config = RunnableConfig(
            configurable={"thread_id": thread_id},
            metadata=metadata or {}
        )
        
        # 2. Execute asynchronously (await instead of blocking)
        result = await self.agent.ainvoke(
            {"messages": [HumanMessage(content=user_request)]},
            config=config
        )
        
        # 3. Extract response
        final_message = result["messages"][-1]
        output = final_message.content if hasattr(final_message, 'content') else str(final_message)
        
        execution_time = (datetime.utcnow() - start_time).total_seconds()
        
        logger.info(f"[{thread_id}] Completed in {execution_time:.2f}s")
        
        # 4. Return structured response
        return {
            "success": True,
            "output": output,
            "thread_id": thread_id,
            "execution_time": execution_time,
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": metadata
        }
        
    except Exception as e:
        logger.error(f"[{thread_id}] Error: {e}", exc_info=True)
        
        execution_time = (datetime.utcnow() - start_time).total_seconds()
        
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
            "thread_id": thread_id,
            "execution_time": execution_time,
            "timestamp": datetime.utcnow().isoformat()
        }
```

**Return Structure Breakdown:**

```python
{
    # Execution Status
    "success": True,              # Did it work?
    "output": "Repository...",    # The actual response
    
    # Conversation Management
    "thread_id": "thread_123",    # For continuing conversation
    
    # Performance Metrics
    "execution_time": 2.34,       # Seconds taken
    "timestamp": "2026-01-02...", # When it executed
    
    # Debugging & Tracking
    "metadata": {                 # Custom tracking data
        "user_id": "123",
        "request_id": "abc",
        "source": "web_ui"
    }
}
```

**Why Dict Instead of String?**

```python
# ❌ String return (hard to work with)
output = agent.run("Read repo")
# How do you know if it succeeded?
# How do you track performance?
# How do you continue the conversation?

# ✅ Dict return (production-ready)
result = await agent.run_async("Read repo")

if result["success"]:
    print(result["output"])
    
    # Track performance
    if result["execution_time"] > 5.0:
        logger.warning("Slow execution!")
    
    # Continue conversation
    result2 = await agent.run_async(
        "What files are in it?",
        thread_id=result["thread_id"]  # ← Maintains context
    )
else:
    logger.error(f"Failed: {result['error']}")
    # Retry logic, send alert, etc.
```

#### `stream(user_request, thread_id) -> AsyncIterator`

```python
async def stream(
    self,
    user_request: str,
    thread_id: Optional[str] = None
) -> AsyncIterator[Dict[str, Any]]:
    """
    Stream execution events in real-time.
    
    Use case: Chat UIs, progress indicators, long operations
    
    Yields events as they happen instead of waiting for completion.
    """
    thread_id = thread_id or f"thread_{datetime.utcnow().timestamp()}"
    
    try:
        config = RunnableConfig(
            configurable={"thread_id": thread_id}
        )
        
        # Use astream_events for event streaming
        async for event in self.agent.astream_events(
            {"messages": [HumanMessage(content=user_request)]},
            config=config,
            version="v2"  # Streaming API version
        ):
            event_type = event.get("event", "")
            
            # Parse and yield different event types
            if event_type == "on_chat_model_start":
                yield {
                    "type": "agent_start",
                    "thread_id": thread_id,
                    "timestamp": datetime.utcnow().isoformat()
                }
            
            elif event_type == "on_tool_start":
                yield {
                    "type": "tool_call",
                    "tool": event.get("name"),
                    "inputs": event.get("data", {}).get("input"),
                    "timestamp": datetime.utcnow().isoformat()
                }
            
            elif event_type == "on_tool_end":
                yield {
                    "type": "tool_result",
                    "tool": event.get("name"),
                    "output": event.get("data", {}).get("output"),
                    "timestamp": datetime.utcnow().isoformat()
                }
            
            elif event_type == "on_chat_model_stream":
                chunk = event.get("data", {}).get("chunk")
                if chunk and hasattr(chunk, 'content'):
                    yield {
                        "type": "agent_response",
                        "content": chunk.content,
                        "timestamp": datetime.utcnow().isoformat()
                    }
            
            elif event_type == "on_chain_end":
                final_output = event.get("data", {}).get("output")
                if final_output:
                    yield {
                        "type": "agent_end",
                        "final_output": final_output,
                        "thread_id": thread_id,
                        "timestamp": datetime.utcnow().isoformat()
                    }
    
    except Exception as e:
        logger.error(f"[{thread_id}] Stream error: {e}", exc_info=True)
        yield {
            "type": "error",
            "error": str(e),
            "error_type": type(e).__name__,
            "timestamp": datetime.utcnow().isoformat()
        }
```

**Event Types:**

| Event | When | Data | Use Case |
|-------|------|------|----------|
| `agent_start` | Execution begins | thread_id, timestamp | Show "Processing..." spinner |
| `tool_call` | Agent decides to use tool | tool name, inputs | Show "Calling GitHub API..." |
| `tool_result` | Tool execution completes | tool name, output | Show "Retrieved 47 files..." |
| `agent_response` | Agent generates text | content chunk | Stream text word-by-word |
| `agent_end` | Execution complete | final output, thread_id | Hide spinner, show final result |
| `error` | Error occurred | error message, type | Show error alert |

**Consumer Example:**

```python
# In a web UI
async for event in agent.stream("Read repo X"):
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
        show_error(event["error"])
```

### 2. GithubTools Class

**Location:** `tools/github_tools.py`

**Purpose:** Provides type-safe, validated GitHub operation tools.

**Architecture:**

```
Input Schema (Pydantic) → Tool Interface (StructuredTool) → Implementation
```

**Component 1: Input Schemas**

```python
class ReadRepositoryInput(BaseModel):
    """
    Validates inputs before they reach the implementation.
    
    Why Pydantic?
    - Type safety: repository must be string
    - Validation: custom validators ensure correct format
    - Documentation: auto-generates JSON schema for LLM
    - Error messages: clear feedback on invalid inputs
    """
    repository: str = Field(
        description="GitHub repository in format 'owner/repo' or full URL"
    )
    branch: str = Field(
        default="main",
        description="Branch name to read from"
    )
    clone_path: Optional[str] = Field(
        default=None,
        description="Local path to clone repository"
    )
    
    @field_validator('repository')
    @classmethod
    def validate_repository(cls, v: str) -> str:
        """
        Normalize repository format.
        
        Accepts:
        - owner/repo
        - https://github.com/owner/repo
        - https://github.com/owner/repo.git
        
        Returns: owner/repo
        """
        if v.startswith('http'):
            parts = v.rstrip('/').rstrip('.git').split('/')
            if len(parts) >= 2:
                return f"{parts[-2]}/{parts[-1]}"
        return v
```

**Validation Flow:**

```python
# ❌ Without validation
def read_repository(repository, branch="main"):
    # What if repository is None?
    # What if branch is 123 (number)?
    # What if repository is "invalid format"?
    # Runtime errors! 💥

# ✅ With Pydantic validation
def read_repository(input: ReadRepositoryInput):
    # Pydantic already validated:
    # - repository is string and properly formatted
    # - branch is string with default "main"
    # - clone_path is optional string or None
    # Type safe! ✨
```

**Component 2: Tool Interface**

```python
class GithubTools:
    def __init__(self):
        """Initialize tools with configuration."""
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.api_url = os.getenv("GITHUB_API_URL", "https://api.github.com")
    
    def get_tools(self) -> List[StructuredTool]:
        """
        Return list of LangChain tools.
        
        Each tool is a StructuredTool that:
        - Has Pydantic input schema
        - Has implementation function
        - Auto-generates description for LLM
        """
        return [
            StructuredTool(
                name="read_repository",
                description=(
                    "Read a GitHub repository and analyze its contents. "
                    "Returns JSON with repository metadata and file information. "
                    "Use this to understand repository structure before cloning."
                ),
                args_schema=ReadRepositoryInput,  # ← Pydantic schema
                func=self._read_repository_impl,  # ← Implementation
            ),
            StructuredTool(
                name="clone_repository",
                description=(
                    "Clone a GitHub repository to local filesystem. "
                    "Returns status of clone operation with local path."
                ),
                args_schema=CloneRepositoryInput,
                func=self._clone_repository_impl,
            )
        ]
```

**Why StructuredTool?**

```python
# Old way: @tool decorator
@tool
def read_repository(repository: str, branch: str = "main"):
    """Read a repository"""
    # Problems:
    # - No input validation
    # - Hard to test
    # - No type safety
    # - LLM gets minimal schema

# New way: StructuredTool
StructuredTool(
    name="read_repository",
    description="...",
    args_schema=ReadRepositoryInput,  # Full Pydantic validation
    func=implementation
)
# Benefits:
# - Full validation before execution
# - Rich JSON schema for LLM
# - Easy to mock for testing
# - Type-safe inputs
```

**Component 3: Implementation**

```python
def _read_repository_impl(self, input: ReadRepositoryInput) -> str:
    """
    Actual implementation of read_repository tool.
    
    Pattern: Try → Execute → Catch → Log → Return
    """
    try:
        logger.info(
            f"Reading repository {input.repository} "
            f"branch {input.branch}"
        )
        
        # Simulated implementation
        # In production: call GitHub API
        result = {
            "repository": input.repository,
            "branch": input.branch,
            "files": [
                {
                    "file": "README.md",
                    "content": "# Example Repository",
                    "sha": "abc123"
                },
                {
                    "file": "package.json",
                    "content": '{"name": "example"}',
                    "sha": "def456"
                }
            ],
            "status": "success",
            "message": f"Successfully read repository {input.repository}"
        }
        
        # Return as JSON string (LLM can parse JSON)
        import json
        return json.dumps(result, indent=2)
    
    except Exception as e:
        logger.error(
            f"Failed to read repository {input.repository}: {e}",
            exc_info=True
        )
        
        # Return error as JSON (structured error handling)
        error_result = {
            "status": "error",
            "error": str(e),
            "error_type": type(e).__name__,
            "repository": input.repository
        }
        
        import json
        return json.dumps(error_result, indent=2)
```

**Error Handling Pattern:**

```python
# ❌ Without proper error handling
def tool_impl(input):
    result = call_api(input.repository)
    return result
    # If API fails: Uncaught exception → agent crashes

# ✅ With proper error handling
def tool_impl(self, input: Schema) -> str:
    try:
        logger.info(f"Calling {input.repository}")
        result = call_api(input.repository)
        return json.dumps({"status": "success", "data": result})
    
    except APIException as e:
        logger.error(f"API error: {e}", exc_info=True)
        return json.dumps({
            "status": "error",
            "error": str(e),
            "retry_after": 60  # LLM can decide to retry
        })
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return json.dumps({
            "status": "error",
            "error": str(e),
            "error_type": type(e).__name__
        })
```

### 3. AppConfig Class

**Location:** `config.py`

**Purpose:** Centralized, validated configuration management.

```python
class AppConfig(BaseModel):
    """
    Production configuration with Pydantic validation.
    
    Benefits:
    - Type safety: int must be int, float must be float
    - Validation: temperature must be 0.0-2.0
    - Defaults: sensible production defaults
    - Environment: reads from .env automatically
    - Documentation: self-documenting via Field descriptions
    """
    
    # LLM Configuration
    model_name: str = Field(
        default=os.getenv("MODEL_NAME", "gemini-2.0-flash-exp"),
        description="LLM model name"
    )
    
    temperature: float = Field(
        default=float(os.getenv("TEMPERATURE", "0.0")),
        ge=0.0,    # Greater than or equal to 0.0
        le=2.0,    # Less than or equal to 2.0
        description="Model temperature (0=deterministic, 2=creative)"
    )
    
    max_retries: int = Field(
        default=int(os.getenv("MAX_RETRIES", "3")),
        ge=0,
        description="Maximum retry attempts for failed requests"
    )
    
    # Agent Configuration
    enable_checkpointing: bool = Field(
        default=os.getenv("ENABLE_CHECKPOINTING", "true").lower() == "true",
        description="Enable conversation state persistence"
    )
    
    # API Configuration
    api_host: str = Field(
        default=os.getenv("API_HOST", "0.0.0.0"),
        description="FastAPI host address"
    )
    
    api_port: int = Field(
        default=int(os.getenv("API_PORT", "8000")),
        gt=0,      # Greater than 0
        lt=65536,  # Less than 65536 (max port)
        description="FastAPI port number"
    )
    
    @field_validator('model_name')
    @classmethod
    def validate_model_name(cls, v: str) -> str:
        """Ensure model name is from allowed list."""
        allowed_models = [
            "gemini-2.0-flash-exp",
            "gemini-2.5-flash",
            "gemini-1.5-pro"
        ]
        if v not in allowed_models:
            raise ValueError(
                f"Model {v} not allowed. Choose from: {allowed_models}"
            )
        return v
```

**Usage:**

```python
# Load and validate config
config = AppConfig()

# Use in agent
agent = GithubAgent(
    tools=tools,
    model_name=config.model_name,        # Validated string
    temperature=config.temperature,      # Validated 0.0-2.0
    enable_checkpointing=config.enable_checkpointing  # Validated bool
)

# Use in API
uvicorn.run(
    "api_server:app",
    host=config.api_host,    # Validated IP
    port=config.api_port,    # Validated 1-65535
    workers=config.api_workers
)
```

**Environment Variables:**

```bash
# .env file
MODEL_NAME=gemini-2.0-flash-exp
TEMPERATURE=0.0
MAX_RETRIES=3
TIMEOUT=60.0
ENABLE_CHECKPOINTING=true
API_HOST=0.0.0.0
API_PORT=8000
GOOGLE_API_KEY=your_key_here
```

---

## 🎨 Design Patterns

### 1. Dependency Injection

**Pattern:** Pass dependencies through constructor instead of global state.

```python
# ❌ Bad: Global state
GLOBAL_TOOLS = GithubTools().get_tools()
GLOBAL_MODEL = "gemini-2.0-flash-exp"

class Agent:
    def __init__(self):
        self.tools = GLOBAL_TOOLS  # Tightly coupled
        self.model = GLOBAL_MODEL  # Hard to test

# ✅ Good: Dependency injection
class Agent:
    def __init__(self, tools: list, model_name: str):
        self.tools = tools          # Injected dependency
        self.model_name = model_name  # Injected dependency

# Usage
tools = GithubTools().get_tools()
agent = Agent(tools=tools, model_name="gemini-2.0-flash-exp")

# Testing
mock_tools = [MockTool()]
test_agent = Agent(tools=mock_tools, model_name="test-model")
```

**Benefits:**
- Easy to test with mocks
- No global state
- Clear dependencies
- Flexible configuration

### 2. Factory Pattern

**Pattern:** Centralized object creation.

```python
# GithubTools.get_tools() is a factory
class GithubTools:
    def get_tools(self) -> List[StructuredTool]:
        """Factory method that creates tools."""
        return [
            self._create_read_tool(),
            self._create_clone_tool()
        ]
    
    def _create_read_tool(self) -> StructuredTool:
        return StructuredTool(
            name="read_repository",
            description="...",
            args_schema=ReadRepositoryInput,
            func=self._read_repository_impl
        )
```

**Benefits:**
- Consistent tool creation
- Easy to add new tools
- Centralized configuration
- DRY (Don't Repeat Yourself)

### 3. Strategy Pattern

**Pattern:** Multiple execution strategies (sync, async, streaming).

```python
class GithubAgent:
    # Strategy 1: Synchronous
    def run(self, request: str) -> str:
        return self.agent.invoke(...)
    
    # Strategy 2: Asynchronous
    async def run_async(self, request: str) -> Dict:
        return await self.agent.ainvoke(...)
    
    # Strategy 3: Streaming
    async def stream(self, request: str) -> AsyncIterator:
        async for event in self.agent.astream_events(...):
            yield event

# Consumer chooses strategy
agent = GithubAgent(...)

# Blocking execution
result = agent.run("...")

# Concurrent execution
result = await agent.run_async("...")

# Real-time streaming
async for chunk in agent.stream("..."):
    print(chunk)
```

**Benefits:**
- Same agent, different execution modes
- Consumer chooses based on use case
- Clean API separation
- Each strategy optimized independently

### 4. Builder Pattern

**Pattern:** LangGraph's create_react_agent builds complex agent.

```python
# Instead of manually configuring:
agent = Agent()
agent.set_model(model)
agent.set_tools(tools)
agent.set_checkpointer(checkpointer)
agent.set_prompt(prompt)
agent.build()

# Use builder pattern:
agent = create_react_agent(
    model=model,
    tools=tools,
    checkpointer=checkpointer
)
# All configuration in one call
```

### 5. Repository Pattern

**Pattern:** Abstract data access (state persistence).

```python
# Abstract interface
class Checkpointer(ABC):
    @abstractmethod
    def get_state(self, thread_id: str) -> Dict:
        pass
    
    @abstractmethod
    def save_state(self, thread_id: str, state: Dict):
        pass

# Concrete implementations
class MemorySaver(Checkpointer):
    """In-memory storage (development)"""
    def __init__(self):
        self.storage = {}
    
    def get_state(self, thread_id):
        return self.storage.get(thread_id, {})
    
    def save_state(self, thread_id, state):
        self.storage[thread_id] = state

class RedisSaver(Checkpointer):
    """Redis storage (production)"""
    def __init__(self, redis_client):
        self.redis = redis_client
    
    def get_state(self, thread_id):
        data = self.redis.get(thread_id)
        return json.loads(data) if data else {}
    
    def save_state(self, thread_id, state):
        self.redis.set(thread_id, json.dumps(state))

# Swap implementations without changing agent code
dev_agent = GithubAgent(tools, checkpointer=MemorySaver())
prod_agent = GithubAgent(tools, checkpointer=RedisSaver(redis_client))
```

---

## 💾 State Management

### How Checkpointing Works

**State Structure:**

```python
{
    "thread_123": {
        "messages": [
            HumanMessage(content="Read repo X"),
            AIMessage(content="Repository contains..."),
            HumanMessage(content="What files are in it?"),
            AIMessage(content="Files include...")
        ],
        "metadata": {
            "created_at": "2026-01-02T10:00:00Z",
            "last_updated": "2026-01-02T10:05:00Z",
            "user_id": "user_123"
        }
    }
}
```

**Checkpoint Lifecycle:**

```python
# Request 1: Create new conversation
config = RunnableConfig(configurable={"thread_id": "conv_123"})
result1 = await agent.ainvoke(
    {"messages": [HumanMessage("Read repo X")]},
    config=config
)
# Checkpointer saves:
# conv_123 → {messages: [Human, AI]}

# Request 2: Continue conversation
result2 = await agent.ainvoke(
    {"messages": [HumanMessage("What files?")]},
    config=config  # Same thread_id
)
# Checkpointer:
# 1. Loads conv_123 state
# 2. Appends new Human message
# 3. Agent sees full history
# 4. Generates AI response
# 5. Saves updated state
# conv_123 → {messages: [Human, AI, Human, AI]}
```

### Production State Storage

**Development:** MemorySaver

```python
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()
# Pros: Simple, fast, no setup
# Cons: Lost on restart, single server only
```

**Production:** Redis

```python
from langgraph.checkpoint.redis import RedisSaver
import redis

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
    decode_responses=True
)

checkpointer = RedisSaver(redis_client)
# Pros: Persistent, distributed, fast
# Cons: External dependency, operational overhead
```

**Enterprise:** PostgreSQL

```python
from langgraph.checkpoint.postgres import PostgresSaver

checkpointer = PostgresSaver(
    postgres_url=os.getenv("DATABASE_URL")
)
# Pros: ACID, searchable, relational queries
# Cons: Slower than Redis, more complex
```

---

## 🚨 Error Handling

### Multi-Layer Error Handling

**Layer 1: Input Validation (Pydantic)**

```python
class ReadRepositoryInput(BaseModel):
    repository: str
    
    @field_validator('repository')
    @classmethod
    def validate_repository(cls, v: str) -> str:
        if not v:
            raise ValueError("Repository cannot be empty")
        if "/" not in v and not v.startswith("http"):
            raise ValueError("Repository must be 'owner/repo' or URL")
        return v

# Error caught before reaching implementation
try:
    input = ReadRepositoryInput(repository="")
except ValidationError as e:
    # {"repository": ["Repository cannot be empty"]}
```

**Layer 2: Tool Execution (Try/Catch)**

```python
def _read_repository_impl(self, input: ReadRepositoryInput) -> str:
    try:
        # Actual operation
        result = github_api.get_repo(input.repository)
        return json.dumps({"status": "success", "data": result})
    
    except GitHubAPIError as e:
        # Specific error handling
        logger.error(f"GitHub API error: {e}")
        return json.dumps({
            "status": "error",
            "error": "GitHub API unavailable",
            "retry_after": 60
        })
    
    except Exception as e:
        # Catch-all for unexpected errors
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return json.dumps({
            "status": "error",
            "error": str(e)
        })
```

**Layer 3: Agent Execution**

```python
async def run_async(self, user_request: str) -> Dict:
    try:
        result = await self.agent.ainvoke(...)
        return {"success": True, "output": result}
    
    except Exception as e:
        logger.error(f"Agent execution failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }
```

**Layer 4: API Endpoint**

```python
@app.post("/agent/run")
async def run_agent(request: AgentRequest):
    try:
        result = await agent.run_async(request.request)
        return AgentResponse(**result)
    
    except Exception as e:
        logger.error(f"API error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
```

### Retry Logic

**LLM Retries (Built-in)**

```python
self.model = ChatGoogleGenerativeAI(
    model=model_name,
    max_retries=3,  # Automatically retry 3 times
    timeout=60.0
)

# Execution:
# Try 1: Request → 500 error → Retry
# Try 2: Request → Timeout → Retry
# Try 3: Request → Success ✓
```

**Custom Retry Logic**

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10)
)
def call_github_api(repo: str):
    """
    Retry pattern:
    - Attempt 1: Immediate
    - Attempt 2: Wait 1s
    - Attempt 3: Wait 2s
    - Attempt 4: Wait 4s
    """
    response = requests.get(f"https://api.github.com/repos/{repo}")
    response.raise_for_status()
    return response.json()
```

---

## 📊 Complete Example Walkthrough

Let's trace a complete request through the entire system:

### Scenario: User makes API request to read a repository

**1. API Request**

```bash
curl -X POST http://localhost:8000/agent/run \
  -H "Content-Type: application/json" \
  -d '{
    "request": "Read repository dipakchavda2912/base-serverless on branch develop",
    "thread_id": "user_123_session",
    "metadata": {"user_id": "123", "source": "web_ui"}
  }'
```

**2. FastAPI Receives Request**

```python
# api_server.py
@app.post("/agent/run", response_model=AgentResponse)
async def run_agent(request: AgentRequest):
    # Pydantic validates request automatically
    # request.request = "Read repository..."
    # request.thread_id = "user_123_session"
    # request.metadata = {"user_id": "123", ...}
    
    result = await agent.run_async(
        user_request=request.request,
        thread_id=request.thread_id,
        metadata=request.metadata
    )
    
    return AgentResponse(**result)
```

**3. Agent Execution Begins**

```python
# agents/github_agent.py
async def run_async(self, user_request, thread_id, metadata):
    # Log start
    logger.info(f"[{thread_id}] Starting execution")
    
    # Configure with thread_id for state management
    config = RunnableConfig(
        configurable={"thread_id": thread_id},
        metadata=metadata
    )
    
    # Execute LangGraph agent
    result = await self.agent.ainvoke(
        {"messages": [HumanMessage(content=user_request)]},
        config=config
    )
```

**4. LangGraph ReAct Loop**

```
Step 1: Checkpointer loads state for thread_id
        → Finds previous messages (if any)

Step 2: Add new HumanMessage to state
        State: {messages: [...previous, new_human_message]}

Step 3: Send to LLM (Gemini)
        Prompt: "You have tools: read_repository, clone_repository
                 User said: Read repository dipakchavda2912/base-serverless on branch develop
                 What do you do?"

Step 4: LLM Response (Thought + Action)
        Thought: "I need to read the repository to get its contents"
        Action: {
          "tool": "read_repository",
          "input": {
            "repository": "dipakchavda2912/base-serverless",
            "branch": "develop"
          }
        }

Step 5: Execute Tool
        → Validate input with ReadRepositoryInput (Pydantic)
        → Call _read_repository_impl()
        → Return JSON result

Step 6: Tool Result → LLM
        Observation: {"repository": "...", "files": [...], "status": "success"}

Step 7: LLM Final Response
        Thought: "I have the repository information"
        Final Answer: "Successfully read repository dipakchavda2912/base-serverless on branch develop.
                       The repository contains the following files:..."

Step 8: Checkpointer saves updated state
        State: {messages: [...previous, human, ai_thought, tool_call, tool_result, ai_final]}
```

**5. Agent Returns Result**

```python
# agents/github_agent.py (continued)
    final_message = result["messages"][-1]
    output = final_message.content
    
    execution_time = (datetime.utcnow() - start_time).total_seconds()
    logger.info(f"[{thread_id}] Completed in {execution_time:.2f}s")
    
    return {
        "success": True,
        "output": output,
        "thread_id": thread_id,
        "execution_time": execution_time,
        "timestamp": datetime.utcnow().isoformat(),
        "metadata": metadata
    }
```

**6. API Response**

```python
# api_server.py (continued)
    return AgentResponse(**result)
    # FastAPI serializes to JSON
```

**7. Client Receives Response**

```json
{
  "success": true,
  "output": "Successfully read repository dipakchavda2912/base-serverless...",
  "thread_id": "user_123_session",
  "execution_time": 2.34,
  "timestamp": "2026-01-02T10:30:00Z",
  "error": null,
  "error_type": null
}
```

---

## 🎓 Key Takeaways

### Why This Architecture?

1. **Separation of Concerns**: API → Agent → LLM → Tools
2. **Type Safety**: Pydantic validation everywhere
3. **Scalability**: Async/await for concurrency
4. **Observability**: Logging at every layer
5. **Resilience**: Multi-layer error handling + retries
6. **Maintainability**: Clean interfaces, dependency injection
7. **Testability**: Mock-friendly design
8. **Production-Ready**: Docker, monitoring, health checks

### Industry Standards (2026)

✅ **Do This:**
- LangGraph for agent orchestration
- Pydantic for validation
- FastAPI for REST APIs
- Async/await for concurrency
- Structured logging
- Type hints everywhere
- Docker for deployment

❌ **Don't Do This:**
- langchain_classic (deprecated)
- No input validation
- Synchronous-only APIs
- Global state
- Print statements for debugging
- No type hints
- Manual server setup

---

## 📖 Further Reading

- **LangGraph Documentation**: https://langchain-ai.github.io/langgraph/
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Pydantic Documentation**: https://docs.pydantic.dev/
- **Google AI SDK**: https://ai.google.dev/

---

**End of Architecture Documentation**
