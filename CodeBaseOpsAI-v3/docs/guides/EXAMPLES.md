# Practical Examples and Tutorials

Step-by-step tutorials showing real-world usage patterns for CodeBaseOpsAI-v3.

---

## Table of Contents

1. [Getting Started Examples](#getting-started-examples)
2. [Basic Repository Operations](#basic-repository-operations)
3. [Advanced Agent Patterns](#advanced-agent-patterns)
4. [Streaming and Real-Time Updates](#streaming-and-real-time-updates)
5. [Building a Web Application](#building-a-web-application)
6. [Integration Examples](#integration-examples)
7. [Production Workflows](#production-workflows)
8. [Custom Tools and Agents](#custom-tools-and-agents)
9. [Error Handling Patterns](#error-handling-patterns)
10. [Performance Optimization](#performance-optimization)

---

## Getting Started Examples

### Example 1: Your First Agent Query

**Goal:** Run a simple query to analyze a GitHub repository.

**Step-by-Step:**

```python
# 1. Import required modules
from agents.github_agent import GitHubAgent
from tools.github_tools import get_tools

# 2. Initialize agent
agent = GitHubAgent()

# 3. Run a query
result = agent.run("Read the repository microsoft/vscode")

# 4. Print results
print(f"Success: {result['success']}")
print(f"Output: {result['output']}")
```

**Expected Output:**
```
Success: True
Output: Repository: microsoft/vscode
Languages: TypeScript (79.2%), JavaScript (14.3%), CSS (3.1%)
Structure: 12,453 files across 156 directories
Main features: Code editor, extension system, integrated terminal...
```

**Complete Working Example:**

```python
# examples/01_first_query.py

"""
Example 1: Your First Agent Query

This example demonstrates the absolute basics:
- Importing the agent
- Running a simple query
- Handling the response
"""

from agents.github_agent import GitHubAgent


def main():
    # Create agent instance
    print("Creating agent...")
    agent = GitHubAgent()
    
    # Define your query
    query = "Read and analyze the repository facebook/react"
    
    # Execute
    print(f"\nExecuting: {query}")
    result = agent.run(query)
    
    # Handle result
    if result['success']:
        print("\n✓ Success!")
        print(f"\nAnalysis:\n{result['output']}")
        print(f"\nExecution time: {result['execution_time']:.2f}s")
    else:
        print(f"\n✗ Error: {result['error']}")


if __name__ == "__main__":
    main()
```

**Run it:**
```bash
cd CodeBaseOpsAI-v3
python examples/01_first_query.py
```

---

### Example 2: Customizing Agent Configuration

**Goal:** Configure the agent with specific settings.

```python
# examples/02_custom_config.py

"""
Example 2: Custom Agent Configuration

Learn how to customize:
- Model selection
- Temperature
- Checkpointing
- Custom tools
"""

from agents.github_agent import GitHubAgent
from tools.github_tools import get_tools


def main():
    # Get tools (you can filter or modify)
    tools = get_tools()
    
    # Create agent with custom configuration
    agent = GitHubAgent(
        tools=tools,
        model_name="gemini-1.5-flash",      # Specific model
        temperature=0.3,                     # Slight creativity
        enable_checkpointing=False           # Stateless (faster)
    )
    
    # Run query
    result = agent.run(
        query="What programming languages are used in pytorch/pytorch?",
        thread_id="custom_thread_1"
    )
    
    print(result['output'])


if __name__ == "__main__":
    main()
```

**Configuration options explained:**

```python
GitHubAgent(
    # Tools to make available to the agent
    tools=[tool1, tool2],  # Default: all GitHub tools
    
    # LLM model selection
    model_name="gemini-2.0-flash-exp",  # Fast and efficient
    # model_name="gemini-1.5-pro",       # Higher quality
    
    # Temperature (creativity level)
    temperature=0.0,    # Deterministic, consistent
    # temperature=0.5,  # Balanced
    # temperature=0.9,  # Creative
    
    # State management
    enable_checkpointing=True,   # Remember conversation context
    # enable_checkpointing=False, # Stateless, independent queries
)
```

---

## Basic Repository Operations

### Example 3: Analyzing Repository Structure

**Goal:** Get detailed repository structure and statistics.

```python
# examples/03_repo_analysis.py

"""
Example 3: Detailed Repository Analysis

Demonstrates:
- Repository structure analysis
- Language detection
- File tree navigation
- Statistics gathering
"""

import json
from agents.github_agent import GitHubAgent


def analyze_repository(owner: str, repo: str):
    """Analyze repository structure and return structured data."""
    
    agent = GitHubAgent()
    
    # Craft detailed query
    query = f"""
    Read the repository '{owner}/{repo}' and provide a detailed analysis:
    
    1. Primary programming languages with percentages
    2. Directory structure (top-level directories)
    3. Number of files and total size
    4. README summary (if exists)
    5. Main technologies used
    
    Format the response as structured data.
    """
    
    result = agent.run(query)
    
    if result['success']:
        return {
            "repository": f"{owner}/{repo}",
            "analysis": result['output'],
            "execution_time": result['execution_time']
        }
    else:
        return {"error": result['error']}


def main():
    # Analyze multiple repositories
    repos_to_analyze = [
        ("vercel", "next.js"),
        ("django", "django"),
        ("tensorflow", "tensorflow"),
    ]
    
    print("Repository Analysis Report")
    print("=" * 80)
    
    for owner, repo in repos_to_analyze:
        print(f"\nAnalyzing {owner}/{repo}...")
        analysis = analyze_repository(owner, repo)
        
        if "error" not in analysis:
            print(f"\nResults for {analysis['repository']}:")
            print(analysis['analysis'])
            print(f"Completed in {analysis['execution_time']:.2f}s")
        else:
            print(f"Error: {analysis['error']}")
        
        print("-" * 80)


if __name__ == "__main__":
    main()
```

---

### Example 4: Cloning and Reading Files

**Goal:** Clone repository and read specific files.

```python
# examples/04_clone_and_read.py

"""
Example 4: Clone Repository and Read Files

Demonstrates:
- Cloning repositories
- Reading specific files
- Parsing code content
- Sequential operations
"""

import os
import tempfile
from agents.github_agent import GitHubAgent


def clone_and_analyze(owner: str, repo: str, files_to_read: list[str]):
    """
    Clone repository and read specific files.
    
    Args:
        owner: Repository owner
        repo: Repository name
        files_to_read: List of file paths to read
    """
    
    agent = GitHubAgent(enable_checkpointing=True)
    thread_id = f"clone_{owner}_{repo}"
    
    # Step 1: Clone repository
    clone_dir = tempfile.mkdtemp()
    clone_query = f"Clone repository '{owner}/{repo}' to '{clone_dir}'"
    
    print(f"Step 1: Cloning...")
    clone_result = agent.run(clone_query, thread_id=thread_id)
    
    if not clone_result['success']:
        return {"error": f"Clone failed: {clone_result['error']}"}
    
    print(f"✓ Cloned to {clone_dir}")
    
    # Step 2: Read specific files
    file_contents = {}
    
    for file_path in files_to_read:
        read_query = f"Read the file '{file_path}' from the cloned repository"
        
        print(f"\nStep 2.{len(file_contents)+1}: Reading {file_path}...")
        read_result = agent.run(read_query, thread_id=thread_id)
        
        if read_result['success']:
            file_contents[file_path] = read_result['output']
            print(f"✓ Read {file_path} ({len(read_result['output'])} chars)")
        else:
            file_contents[file_path] = f"Error: {read_result['error']}"
    
    return {
        "clone_directory": clone_dir,
        "files": file_contents
    }


def main():
    # Example: Clone React and read specific files
    result = clone_and_analyze(
        owner="facebook",
        repo="react",
        files_to_read=[
            "README.md",
            "package.json",
            "LICENSE"
        ]
    )
    
    if "error" in result:
        print(f"Error: {result['error']}")
        return
    
    print(f"\n{'=' * 80}")
    print(f"Clone directory: {result['clone_directory']}")
    print(f"\nFile contents:")
    
    for file_path, content in result['files'].items():
        print(f"\n--- {file_path} ---")
        print(content[:500])  # First 500 chars
        if len(content) > 500:
            print(f"\n... ({len(content) - 500} more characters)")


if __name__ == "__main__":
    main()
```

---

## Advanced Agent Patterns

### Example 5: Async Concurrent Operations

**Goal:** Process multiple repositories concurrently for faster execution.

```python
# examples/05_async_concurrent.py

"""
Example 5: Async Concurrent Operations

Demonstrates:
- Async/await syntax
- Concurrent query execution
- Performance comparison
- Error handling in async code
"""

import asyncio
import time
from agents.github_agent import GitHubAgent


async def analyze_repo_async(agent: GitHubAgent, owner: str, repo: str) -> dict:
    """Analyze single repository asynchronously."""
    
    query = f"Analyze the repository {owner}/{repo} and provide a summary"
    
    try:
        result = await agent.run_async(
            query=query,
            thread_id=f"{owner}_{repo}"
        )
        
        return {
            "repo": f"{owner}/{repo}",
            "success": result['success'],
            "output": result['output'][:200],  # First 200 chars
            "time": result['execution_time']
        }
    except Exception as e:
        return {
            "repo": f"{owner}/{repo}",
            "success": False,
            "error": str(e)
        }


async def sequential_processing(repos: list[tuple[str, str]]):
    """Process repositories sequentially (slow)."""
    
    agent = GitHubAgent()
    results = []
    
    start_time = time.time()
    
    for owner, repo in repos:
        result = await analyze_repo_async(agent, owner, repo)
        results.append(result)
    
    total_time = time.time() - start_time
    
    return results, total_time


async def concurrent_processing(repos: list[tuple[str, str]]):
    """Process repositories concurrently (fast)."""
    
    agent = GitHubAgent()
    
    start_time = time.time()
    
    # Create tasks for all repositories
    tasks = [
        analyze_repo_async(agent, owner, repo)
        for owner, repo in repos
    ]
    
    # Run all concurrently
    results = await asyncio.gather(*tasks)
    
    total_time = time.time() - start_time
    
    return results, total_time


async def main():
    # List of repositories to analyze
    repos = [
        ("facebook", "react"),
        ("vuejs", "vue"),
        ("angular", "angular"),
        ("sveltejs", "svelte"),
        ("microsoft", "typescript"),
    ]
    
    print("Performance Comparison: Sequential vs Concurrent")
    print("=" * 80)
    
    # Sequential processing
    print("\n1. Sequential Processing (one at a time)...")
    seq_results, seq_time = await sequential_processing(repos)
    
    print(f"\n✓ Completed in {seq_time:.2f}s")
    print(f"Average time per repo: {seq_time / len(repos):.2f}s")
    
    # Concurrent processing
    print("\n2. Concurrent Processing (all at once)...")
    conc_results, conc_time = await concurrent_processing(repos)
    
    print(f"\n✓ Completed in {conc_time:.2f}s")
    print(f"Average time per repo: {conc_time / len(repos):.2f}s")
    
    # Performance improvement
    speedup = seq_time / conc_time
    print(f"\n🚀 Speedup: {speedup:.1f}x faster!")
    
    # Show results
    print(f"\n{'=' * 80}")
    print("Results:")
    for result in conc_results:
        status = "✓" if result['success'] else "✗"
        print(f"\n{status} {result['repo']}")
        if result['success']:
            print(f"  {result['output']}...")
        else:
            print(f"  Error: {result.get('error', 'Unknown')}")


if __name__ == "__main__":
    asyncio.run(main())
```

**Expected output:**
```
Performance Comparison: Sequential vs Concurrent
===============================================================

1. Sequential Processing (one at a time)...
✓ Completed in 45.32s
Average time per repo: 9.06s

2. Concurrent Processing (all at once)...
✓ Completed in 12.18s
Average time per repo: 2.44s

🚀 Speedup: 3.7x faster!
```

---

### Example 6: Multi-Turn Conversations

**Goal:** Maintain context across multiple queries.

```python
# examples/06_conversation.py

"""
Example 6: Multi-Turn Conversations

Demonstrates:
- Conversation state management
- Context preservation
- Thread IDs
- Follow-up questions
"""

import asyncio
from agents.github_agent import GitHubAgent


async def conversational_workflow():
    """
    Demonstrate multi-turn conversation with context.
    
    The agent remembers previous interactions within the same thread.
    """
    
    # Initialize agent with checkpointing enabled
    agent = GitHubAgent(enable_checkpointing=True)
    
    # Use consistent thread_id for conversation continuity
    thread_id = "conversation_demo_001"
    
    print("Multi-Turn Conversation Demo")
    print("=" * 80)
    
    # Turn 1: Initial query
    print("\n[User] Please analyze the repository tensorflow/tensorflow")
    result1 = await agent.run_async(
        query="Please analyze the repository tensorflow/tensorflow",
        thread_id=thread_id
    )
    print(f"\n[Agent] {result1['output'][:300]}...\n")
    
    # Turn 2: Follow-up (agent remembers context)
    print("[User] What are the main programming languages used?")
    result2 = await agent.run_async(
        query="What are the main programming languages used?",
        thread_id=thread_id  # Same thread = remembers TensorFlow
    )
    print(f"\n[Agent] {result2['output']}\n")
    
    # Turn 3: Another follow-up
    print("[User] Can you estimate the codebase size?")
    result3 = await agent.run_async(
        query="Can you estimate the codebase size?",
        thread_id=thread_id
    )
    print(f"\n[Agent] {result3['output']}\n")
    
    # Turn 4: Change subject (but still same thread)
    print("[User] Now switch to analyzing pytorch/pytorch instead")
    result4 = await agent.run_async(
        query="Now switch to analyzing pytorch/pytorch instead",
        thread_id=thread_id
    )
    print(f"\n[Agent] {result4['output'][:300]}...\n")
    
    # Turn 5: Reference previous conversation
    print("[User] How does this compare to the TensorFlow repo we discussed?")
    result5 = await agent.run_async(
        query="How does this compare to the TensorFlow repo we discussed?",
        thread_id=thread_id
    )
    print(f"\n[Agent] {result5['output']}\n")


async def separate_conversations():
    """
    Demonstrate separate conversations with different thread IDs.
    """
    
    agent = GitHubAgent(enable_checkpointing=True)
    
    print("\n\nSeparate Conversations Demo")
    print("=" * 80)
    
    # Conversation 1: About React
    print("\nConversation 1 (thread_react):")
    await agent.run_async(
        "Analyze facebook/react",
        thread_id="thread_react"
    )
    result1 = await agent.run_async(
        "What version is it?",  # References React from same thread
        thread_id="thread_react"
    )
    print(f"React version: {result1['output']}")
    
    # Conversation 2: About Vue (separate thread)
    print("\nConversation 2 (thread_vue):")
    await agent.run_async(
        "Analyze vuejs/vue",
        thread_id="thread_vue"
    )
    result2 = await agent.run_async(
        "What version is it?",  # References Vue from separate thread
        thread_id="thread_vue"
    )
    print(f"Vue version: {result2['output']}")


async def main():
    # Demo 1: Single conversation thread
    await conversational_workflow()
    
    # Demo 2: Multiple separate conversations
    await separate_conversations()


if __name__ == "__main__":
    asyncio.run(main())
```

---

## Streaming and Real-Time Updates

### Example 7: Streaming Responses

**Goal:** Display real-time updates as the agent processes.

```python
# examples/07_streaming.py

"""
Example 7: Streaming Responses

Demonstrates:
- Real-time event streaming
- Progress indicators
- Token-by-token responses
- Tool execution tracking
"""

import asyncio
from agents.github_agent import GitHubAgent


async def stream_with_progress():
    """Stream agent execution with progress indicators."""
    
    agent = GitHubAgent()
    
    query = "Analyze the repository microsoft/vscode in detail"
    
    print(f"Query: {query}\n")
    print("Streaming response...")
    print("=" * 80)
    
    # Track events
    event_counts = {
        "token": 0,
        "tool_start": 0,
        "tool_end": 0,
        "error": 0
    }
    
    # Stream events
    async for event in agent.stream(query):
        event_type = event.get("type")
        
        if event_type == "token":
            # Token from LLM
            content = event.get("content", "")
            print(content, end="", flush=True)
            event_counts["token"] += 1
        
        elif event_type == "tool_start":
            # Tool execution started
            tool_name = event.get("tool", "unknown")
            print(f"\n\n[Tool: {tool_name}] Starting...", flush=True)
            event_counts["tool_start"] += 1
        
        elif event_type == "tool_end":
            # Tool execution completed
            tool_name = event.get("tool", "unknown")
            output = event.get("output", "")
            print(f"\n[Tool: {tool_name}] Completed", flush=True)
            print(f"Output: {output[:100]}...", flush=True)
            event_counts["tool_end"] += 1
        
        elif event_type == "error":
            # Error occurred
            error = event.get("error", "Unknown error")
            print(f"\n\n❌ Error: {error}", flush=True)
            event_counts["error"] += 1
    
    # Summary
    print(f"\n\n{'=' * 80}")
    print("Streaming Summary:")
    print(f"  Tokens: {event_counts['token']}")
    print(f"  Tools started: {event_counts['tool_start']}")
    print(f"  Tools completed: {event_counts['tool_end']}")
    print(f"  Errors: {event_counts['error']}")


async def stream_to_file():
    """Stream response to a file for logging."""
    
    agent = GitHubAgent()
    query = "Analyze facebook/react"
    
    output_file = "stream_output.txt"
    
    print(f"Streaming to {output_file}...")
    
    with open(output_file, 'w') as f:
        f.write(f"Query: {query}\n")
        f.write("=" * 80 + "\n\n")
        
        async for event in agent.stream(query):
            if event.get("type") == "token":
                content = event.get("content", "")
                f.write(content)
                f.flush()  # Write immediately
                
                # Also print progress indicator
                print(".", end="", flush=True)
        
        f.write("\n\n" + "=" * 80)
    
    print(f"\n✓ Saved to {output_file}")


async def main():
    # Demo 1: Stream with progress
    await stream_with_progress()
    
    # Demo 2: Stream to file
    print("\n\n")
    await stream_to_file()


if __name__ == "__main__":
    asyncio.run(main())
```

---

## Building a Web Application

### Example 8: FastAPI Integration

**Goal:** Build a REST API for the agent.

```python
# examples/08_fastapi_app.py

"""
Example 8: FastAPI Web Application

Demonstrates:
- REST API endpoints
- Request/response models
- Error handling
- Streaming endpoints (SSE)
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import asyncio
import json

from agents.github_agent import GitHubAgent


# Request/Response models
class AnalyzeRequest(BaseModel):
    """Request model for repository analysis."""
    owner: str
    repo: str
    thread_id: Optional[str] = "default"


class AnalyzeResponse(BaseModel):
    """Response model for repository analysis."""
    success: bool
    output: Optional[str] = None
    error: Optional[str] = None
    execution_time: float
    thread_id: str


# Create FastAPI app
app = FastAPI(
    title="CodeBaseOpsAI API",
    description="AI-powered GitHub repository analysis",
    version="3.0.0"
)


# Initialize agent (singleton)
agent = GitHubAgent()


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "CodeBaseOpsAI",
        "version": "3.0.0"
    }


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_repository(request: AnalyzeRequest):
    """
    Analyze a GitHub repository.
    
    Example:
        POST /analyze
        {
            "owner": "facebook",
            "repo": "react",
            "thread_id": "user123"
        }
    """
    
    try:
        # Build query
        query = f"Analyze the repository {request.owner}/{request.repo}"
        
        # Execute
        result = await agent.run_async(
            query=query,
            thread_id=request.thread_id
        )
        
        # Return response
        return AnalyzeResponse(
            success=result['success'],
            output=result.get('output'),
            error=result.get('error'),
            execution_time=result['execution_time'],
            thread_id=result['thread_id']
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@app.post("/stream")
async def stream_analysis(request: AnalyzeRequest):
    """
    Stream repository analysis with real-time updates.
    
    Returns Server-Sent Events (SSE).
    """
    
    async def event_generator():
        """Generate SSE events."""
        try:
            query = f"Analyze repository {request.owner}/{request.repo}"
            
            async for event in agent.stream(query, thread_id=request.thread_id):
                # Format as SSE
                yield f"data: {json.dumps(event)}\n\n"
        
        except Exception as e:
            error_event = {"type": "error", "error": str(e)}
            yield f"data: {json.dumps(error_event)}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )


# Run with: uvicorn examples.08_fastapi_app:app --reload
```

**Client Example:**

```python
# examples/08_client.py

"""Client for FastAPI application."""

import httpx
import asyncio
import json


async def analyze_sync():
    """Call synchronous analyze endpoint."""
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/analyze",
            json={
                "owner": "facebook",
                "repo": "react",
                "thread_id": "client_demo"
            },
            timeout=60.0
        )
        
        result = response.json()
        
        print("Analysis Result:")
        print(f"  Success: {result['success']}")
        print(f"  Time: {result['execution_time']:.2f}s")
        print(f"\n{result['output']}")


async def analyze_streaming():
    """Call streaming endpoint with SSE."""
    
    async with httpx.AsyncClient() as client:
        async with client.stream(
            "POST",
            "http://localhost:8000/stream",
            json={
                "owner": "vuejs",
                "repo": "vue",
                "thread_id": "stream_demo"
            },
            timeout=120.0
        ) as response:
            
            print("Streaming response:\n")
            
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = json.loads(line[6:])
                    
                    if data.get("type") == "token":
                        print(data.get("content", ""), end="", flush=True)
                    elif data.get("type") == "tool_start":
                        print(f"\n[Tool: {data.get('tool')}]")
                    elif data.get("type") == "error":
                        print(f"\nError: {data.get('error')}")


async def main():
    # Test sync endpoint
    print("=== Sync Endpoint ===\n")
    await analyze_sync()
    
    # Test streaming endpoint
    print("\n\n=== Streaming Endpoint ===\n")
    await analyze_streaming()


if __name__ == "__main__":
    asyncio.run(main())
```

**Run the application:**

```bash
# Terminal 1: Start server
uvicorn examples.08_fastapi_app:app --reload --port 8000

# Terminal 2: Test with client
python examples/08_client.py

# Or test with curl
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"owner": "facebook", "repo": "react"}'
```

---

## Integration Examples

### Example 9: Integration with Django

**Goal:** Integrate agent into Django project.

```python
# examples/django_integration/views.py

"""
Example 9: Django Integration

Demonstrates:
- Django views with async support
- Form handling
- Template rendering
- Session management
"""

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import asyncio

from agents.github_agent import GitHubAgent


# Initialize agent (consider using Django cache)
agent = GitHubAgent()


@require_http_methods(["GET", "POST"])
async def analyze_repository(request):
    """
    Django view for repository analysis.
    
    GET: Show form
    POST: Process analysis
    """
    
    if request.method == "GET":
        return render(request, "analyze_form.html")
    
    # POST: Process form
    owner = request.POST.get("owner")
    repo = request.POST.get("repo")
    
    if not owner or not repo:
        return JsonResponse({
            "error": "Owner and repo are required"
        }, status=400)
    
    # Use session ID as thread_id for context persistence
    thread_id = request.session.session_key or "anonymous"
    
    try:
        query = f"Analyze repository {owner}/{repo}"
        result = await agent.run_async(query, thread_id=thread_id)
        
        return JsonResponse({
            "success": result['success'],
            "output": result.get('output'),
            "execution_time": result['execution_time']
        })
    
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)
```

```html
<!-- examples/django_integration/templates/analyze_form.html -->

<!DOCTYPE html>
<html>
<head>
    <title>Repository Analysis</title>
</head>
<body>
    <h1>Analyze GitHub Repository</h1>
    
    <form method="post" id="analyze-form">
        {% csrf_token %}
        
        <label for="owner">Owner:</label>
        <input type="text" name="owner" id="owner" required>
        
        <label for="repo">Repository:</label>
        <input type="text" name="repo" id="repo" required>
        
        <button type="submit">Analyze</button>
    </form>
    
    <div id="results"></div>
    
    <script>
        document.getElementById('analyze-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(e.target);
            
            document.getElementById('results').innerHTML = 'Analyzing...';
            
            const response = await fetch(window.location.href, {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (data.success) {
                document.getElementById('results').innerHTML = `
                    <h2>Results</h2>
                    <pre>${data.output}</pre>
                    <p>Time: ${data.execution_time.toFixed(2)}s</p>
                `;
            } else {
                document.getElementById('results').innerHTML = `
                    <p style="color: red;">Error: ${data.error}</p>
                `;
            }
        });
    </script>
</body>
</html>
```

---

### Example 10: Slack Bot Integration

**Goal:** Create a Slack bot powered by the agent.

```python
# examples/10_slack_bot.py

"""
Example 10: Slack Bot Integration

Demonstrates:
- Slack Events API integration
- Real-time chat responses
- Command handling
- Thread-based conversations
"""

from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
import os
import asyncio

from agents.github_agent import GitHubAgent


# Initialize Slack app
app = AsyncApp(token=os.environ["SLACK_BOT_TOKEN"])

# Initialize agent
agent = GitHubAgent(enable_checkpointing=True)


@app.message("analyze")
async def handle_analyze_command(message, say):
    """
    Handle 'analyze' command.
    
    Usage: @bot analyze owner/repo
    """
    
    text = message.get("text", "")
    user_id = message.get("user")
    channel_id = message.get("channel")
    
    # Parse repository from message
    # Format: "analyze facebook/react"
    parts = text.split()
    if len(parts) < 2:
        await say("Usage: analyze owner/repo")
        return
    
    repo_full_name = parts[1]
    
    try:
        # Use Slack thread_ts as conversation thread_id
        thread_id = message.get("thread_ts") or message.get("ts")
        
        # Send "thinking" message
        await say(f"Analyzing {repo_full_name}... ⏳", thread_ts=thread_id)
        
        # Execute agent
        query = f"Analyze repository {repo_full_name}"
        result = await agent.run_async(query, thread_id=f"slack_{user_id}_{thread_id}")
        
        # Send result
        if result['success']:
            await say(
                f"Analysis complete! ✅\n\n{result['output']}",
                thread_ts=thread_id
            )
        else:
            await say(
                f"Analysis failed ❌\n\nError: {result['error']}",
                thread_ts=thread_id
            )
    
    except Exception as e:
        await say(f"Error: {str(e)} ❌", thread_ts=thread_id)


@app.message("help")
async def handle_help(message, say):
    """Show help message."""
    
    help_text = """
    *CodeBaseOpsAI Commands:*
    
    • `analyze owner/repo` - Analyze a GitHub repository
    • `help` - Show this help message
    
    *Examples:*
    • analyze facebook/react
    • analyze microsoft/vscode
    """
    
    await say(help_text)


async def main():
    """Start the Slack bot."""
    handler = AsyncSocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    await handler.start_async()


if __name__ == "__main__":
    # Set environment variables first:
    # export SLACK_BOT_TOKEN=xoxb-your-token
    # export SLACK_APP_TOKEN=xapp-your-token
    
    asyncio.run(main())
```

---

**(Continuing in next response due to length...)**

---

**Document Information:**
- **Created:** January 2, 2026
- **Version:** 1.0 (Part 1 of 2)
- **Lines:** 1,100+
- **Related:** [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md), [API_REFERENCE.md](../reference/API_REFERENCE.md)
