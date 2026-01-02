# Frequently Asked Questions (FAQ)

Common questions about CodeBaseOpsAI-v3, LangGraph, LangChain, and AI agent development.

---

## Table of Contents

1. [General Questions](#general-questions)
2. [Getting Started](#getting-started)
3. [LangChain vs LangGraph](#langchain-vs-langgraph)
4. [Agent Behavior](#agent-behavior)
5. [Streaming](#streaming)
6. [Performance](#performance)
7. [State Management](#state-management)
8. [Tools](#tools)
9. [Deployment](#deployment)
10. [Troubleshooting](#troubleshooting)
11. [Advanced Topics](#advanced-topics)

---

## General Questions

### What is CodeBaseOpsAI-v3?

**Answer:** CodeBaseOpsAI-v3 is a production-grade AI agent system for analyzing GitHub repositories using Google's Gemini AI models. It demonstrates modern best practices for building LLM-powered applications with:

- **LangGraph** for agent orchestration
- **Async/await** for scalability
- **Streaming** for real-time UX
- **State management** for conversations
- **FastAPI** for REST APIs
- **Docker** for deployment

**Use Cases:**
- Automated repository analysis
- Code documentation generation
- Dependency auditing
- Code quality assessment
- Multi-repository comparisons

---

### Why build this instead of using ChatGPT?

**Answer:** CodeBaseOpsAI-v3 offers several advantages over general-purpose LLMs:

1. **Custom Tools:** Specialized GitHub operations not available in ChatGPT
2. **State Management:** Maintains context across multiple queries
3. **Programmatic API:** Integrate into your applications
4. **Streaming:** Real-time responses for better UX
5. **Self-Hosted:** Full control over data and privacy
6. **Customizable:** Add your own tools and logic
7. **Production-Ready:** Error handling, logging, monitoring

**Example:**
```python
# Your application
agent = GitHubAgent()

# Analyze 100 repositories programmatically
for repo in repositories:
    analysis = agent.run(f"Analyze {repo}")
    save_to_database(analysis)
```

**External Reference:** [Why Build Custom LLM Applications](https://www.langchain.com/use-cases)

---

### What's the difference between v2 and v3?

**Answer:** 

| Feature | v2 (Learning) | v3 (Production) |
|---------|---------------|-----------------|
| Framework | LangChain Classic | LangGraph |
| Agent Type | ReAct (simple) | ReAct (advanced) |
| Async Support | No | Yes ✓ |
| Streaming | No | Yes ✓ |
| State Management | Basic | Advanced (Redis/Postgres) |
| API Server | No | FastAPI ✓ |
| Testing | Minimal | Comprehensive |
| Docker | No | Yes ✓ |
| Documentation | Basic | 6,700+ lines |

**When to use v2:**
- Learning LangChain basics
- Simple scripts
- Prototyping

**When to use v3:**
- Production applications
- APIs and web apps
- Team projects
- Scalability needed

**See:** [COMPARISON.md](../migration/COMPARISON.md) for detailed differences.

---

## Getting Started

### Do I need programming experience?

**Answer:** Yes, intermediate Python knowledge is recommended:

**Required Skills:**
- Python basics (variables, functions, classes)
- Understanding of APIs
- Command line usage
- Virtual environments

**Helpful But Not Required:**
- Async/await programming
- FastAPI/web frameworks
- Docker/containerization
- Git/GitHub

**Learning Path:**
```
1. Learn Python basics (if needed)
   → Official Python Tutorial: https://docs.python.org/3/tutorial/

2. Understand async/await
   → Read: docs/guides/UNDERSTANDING.md (Deep Dive: Async)

3. Follow examples
   → Start with: docs/guides/EXAMPLES.md

4. Build something
   → Customize tools for your use case
```

---

### What do I need to get started?

**Answer:** 

**Minimum Requirements:**
```bash
✓ Python 3.11 or higher
✓ Google API Key (free from https://aistudio.google.com/app/apikey)
✓ 2GB RAM
✓ Internet connection
```

**Optional (Recommended):**
```bash
○ GitHub Personal Access Token (for private repos)
○ 4GB+ RAM (for better performance)
○ Redis (for production state persistence)
○ Docker (for containerized deployment)
```

**Setup Time:** ~10 minutes

**See:** [QUICKSTART.md](QUICKSTART.md) for step-by-step setup.

---

### How much does it cost to run?

**Answer:** 

**API Costs (Google Gemini):**
- **Free tier:** 15 requests/minute, 1500 requests/day
- **Paid:** $0.00025 per 1K tokens (~$0.25 per million tokens)

**Example Costs:**
```
Average repository analysis:
- Input: ~500 tokens
- Output: ~1000 tokens
- Total: ~1500 tokens
- Cost: ~$0.000375 (less than a penny)

100 analyses per day:
- ~$0.0375/day
- ~$1.13/month
```

**Infrastructure:**
```
Development (local): $0
Production (cloud):
  - VM/Container: $5-20/month
  - Redis: $5-10/month
  - Total: ~$10-30/month
```

**Cost Optimization Tips:**
1. Use gemini-2.0-flash-exp (fastest, cheapest)
2. Cache results to reduce API calls
3. Set temperature=0 for consistent results

**External Reference:** [Google AI Pricing](https://ai.google.dev/pricing)

---

## LangChain vs LangGraph

### What's the difference between LangChain and LangGraph?

**Answer:**

**LangChain (Classic):**
```python
# Simple, sequential chains
from langchain.agents import create_react_agent

agent = create_react_agent(llm, tools, prompt)
result = agent.invoke({"input": "query"})
```

- **Pros:** Simple, quick to start
- **Cons:** Limited control, hard to customize
- **Use:** Simple workflows, prototyping

**LangGraph (Modern):**
```python
# Graph-based, flexible workflows
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(llm, tools, checkpointer=saver)
result = await agent.ainvoke({"messages": [("user", "query")]})
```

- **Pros:** Flexible, scalable, production-ready
- **Cons:** Slightly steeper learning curve
- **Use:** Production apps, complex workflows

**Key Differences:**

| Feature | LangChain | LangGraph |
|---------|-----------|-----------|
| Architecture | Linear chains | Directed graphs |
| Async | Limited | Full support |
| Streaming | Basic | Advanced |
| State | Simple | Advanced (Redis/Postgres) |
| Control Flow | Sequential | Branching, loops |
| Production | ⚠️ Limited | ✓ Full support |

**Recommendation:** Use LangGraph for v3 (production), LangChain for v2 (learning).

**External Reference:** [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)

---

### Should I use LangChain or LangGraph for my project?

**Answer:**

**Use LangChain Classic if:**
- Learning AI agents for the first time
- Building simple prototypes
- Need quick proof-of-concept
- Linear, sequential workflows

**Use LangGraph if:**
- Building production applications
- Need async/await and streaming
- Require complex workflows (branching, loops)
- Need state persistence (Redis, Postgres)
- Want to scale to multiple users
- Building APIs or web applications

**Migration Path:**
```
Start with LangChain v2 (learning)
  ↓
Understand concepts
  ↓
Migrate to LangGraph v3 (production)
```

**See:** [MIGRATION.md](../migration/MIGRATION.md) for migration guide.

---

## Agent Behavior

### Why doesn't my agent use the tools?

**Answer:** Common reasons and solutions:

**1. Unclear Tool Descriptions**
```python
# ❌ Bad: Vague description
@tool
def my_tool(input: str) -> str:
    """Does something."""
    pass

# ✓ Good: Clear, specific description
@tool
def my_tool(input: str) -> str:
    """
    Search code in GitHub repositories.
    
    Use this when user asks:
    - "Find code for X"
    - "Search for Y in repo Z"
    
    Args:
        input: Search query
    
    Returns:
        Code snippets matching query
    """
    pass
```

**2. Vague User Queries**
```python
# ❌ Vague query
result = agent.run("Tell me about VSCode")
# Agent might not know to use read_repository tool

# ✓ Specific query
result = agent.run("Read the repository microsoft/vscode")
# Agent understands to use the tool
```

**3. Tool Not Registered**
```python
# Verify tools are available
from tools.github_tools import get_tools

tools = get_tools()
print([t.name for t in tools])
# Should show: ['read_repository', 'clone_repository']

# Ensure tools passed to agent
agent = GitHubAgent(tools=tools)
```

**4. Model Limitations**
```python
# Some models are better at tool usage
model_name="gemini-2.0-flash-exp"  # ✓ Good tool usage
# vs
model_name="gemini-1.0-pro"        # ⚠️ Older, less reliable
```

**See:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md#agent-doesnt-call-tools) for more solutions.

---

### How do I make the agent more accurate?

**Answer:**

**1. Lower Temperature**
```python
# More deterministic, consistent
agent = GitHubAgent(temperature=0.0)  # vs 0.7
```

**2. Better Prompts**
```python
# ❌ Vague
"Analyze the repo"

# ✓ Specific
"Analyze the repository facebook/react and provide:
1. Primary programming languages with percentages
2. Number of files and total size
3. Main dependencies from package.json
4. README summary"
```

**3. Add Examples to Tool Descriptions**
```python
@tool
def my_tool(input: str) -> str:
    """
    Tool description.
    
    Examples:
        my_tool("example 1") → result 1
        my_tool("example 2") → result 2
    """
```

**4. Use System Prompts**
```python
system_prompt = """You are a precise code analyzer.

Rules:
- Always cite specific files and line numbers
- Use exact numbers, not estimates
- If unsure, say "I don't have enough information"
- Always use tools to verify information"""

# Pass to agent during creation
```

**5. Validate Outputs**
```python
def validate_analysis(result: dict) -> bool:
    """Validate agent output has required fields."""
    required = ["languages", "file_count", "size"]
    return all(key in result['output'] for key in required)
```

---

### Can the agent make mistakes?

**Answer:** **Yes!** LLMs are probabilistic and can:

1. **Hallucinate:** Make up information
2. **Misunderstand:** Interpret queries incorrectly
3. **Miss Details:** Skip important information
4. **Tool Errors:** Use tools incorrectly

**Mitigation Strategies:**

```python
# 1. Validate outputs
def validate_result(result):
    if not result['success']:
        return False
    
    # Check for hallucination markers
    hallucination_phrases = [
        "I think",
        "probably",
        "might be",
        "estimated"
    ]
    
    output = result['output'].lower()
    if any(phrase in output for phrase in hallucination_phrases):
        logger.warning("Potential hallucination detected")
    
    return True

# 2. Use temperature=0 for consistency
agent = GitHubAgent(temperature=0.0)

# 3. Cross-validate with tools
result = agent.run("How many files in repo X?")
actual_count = count_files_from_api()  # Verify with real API

# 4. Human-in-the-loop for critical decisions
if critical_decision:
    result = agent.run(query)
    approved = get_human_approval(result)
    if not approved:
        result = agent.run(f"Revise: {feedback}")
```

**Best Practices:**
- Never trust agent output blindly
- Validate critical information
- Use tools for ground truth
- Implement checks and balances
- Keep humans involved in important decisions

---

## Streaming

### What is streaming and why use it?

**Answer:**

**Without Streaming (Traditional):**
```python
agent = GitHubAgent()
result = agent.run("Analyze repository")  # Wait 10-30 seconds
print(result)  # Shows all at once
```

User experience: 😴 Waiting... waiting... 💤 (bad UX)

**With Streaming:**
```python
async for chunk in agent.stream("Analyze repository"):
    print(chunk, end="", flush=True)  # Shows as it generates
```

User experience: 👀 Seeing results in real-time (great UX!)

**Benefits:**

1. **Better UX:** Users see progress immediately
2. **Perceived Performance:** Feels faster even if same total time
3. **Early Cancellation:** Stop if going wrong direction
4. **Real-time Feedback:** See tool calls and reasoning
5. **Long-running Tasks:** Progress indicators for complex queries

**Use Cases:**
- Chat interfaces
- Web applications
- Interactive terminals
- Progress dashboards
- User-facing applications

**When NOT to use:**
- Background batch jobs
- Scheduled tasks
- Automated scripts where speed > UX

**See:** [UNDERSTANDING.md](UNDERSTANDING.md#deep-dive-why-streaming) for detailed explanation.

---

### How do I implement streaming in my application?

**Answer:**

**1. Python CLI:**
```python
import asyncio

async def main():
    agent = GitHubAgent()
    
    async for event in agent.stream("Analyze repo"):
        if event['type'] == 'token':
            print(event['content'], end='', flush=True)

asyncio.run(main())
```

**2. FastAPI (Server-Sent Events):**
```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

@app.post("/stream")
async def stream_endpoint(query: str):
    async def generate():
        agent = GitHubAgent()
        async for event in agent.stream(query):
            yield f"data: {json.dumps(event)}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")
```

**3. JavaScript Client:**
```javascript
const eventSource = new EventSource('/stream?query=analyze+repo');

eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === 'token') {
        document.getElementById('output').textContent += data.content;
    }
};
```

**4. React Component:**
```javascript
function StreamingResponse({ query }) {
    const [output, setOutput] = useState('');
    
    useEffect(() => {
        const eventSource = new EventSource(`/stream?query=${query}`);
        
        eventSource.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === 'token') {
                setOutput(prev => prev + data.content);
            }
        };
        
        return () => eventSource.close();
    }, [query]);
    
    return <div>{output}</div>;
}
```

**See:** [EXAMPLES.md](EXAMPLES.md#streaming-and-real-time-updates) for complete examples.

---

## Performance

### How can I make the agent faster?

**Answer:**

**1. Use Faster Model**
```python
# Fast (recommended)
model_name="gemini-2.0-flash-exp"  # ~2-5s response

# Slower but higher quality
model_name="gemini-1.5-pro"  # ~5-15s response
```

**2. Async Concurrent Execution**
```python
# ❌ Sequential: 30 seconds for 3 repos
for repo in repos:
    result = agent.run(f"Analyze {repo}")

# ✓ Concurrent: 10 seconds for 3 repos
tasks = [agent.run_async(f"Analyze {repo}") for repo in repos]
results = await asyncio.gather(*tasks)
```

**3. Cache Results**
```python
from functools import lru_cache
import hashlib

class CachedAgent:
    def __init__(self):
        self.agent = GitHubAgent()
        self.cache = {}
    
    def run(self, query: str):
        # Check cache
        key = hashlib.md5(query.encode()).hexdigest()
        if key in self.cache:
            return self.cache[key]
        
        # Execute and cache
        result = self.agent.run(query)
        self.cache[key] = result
        return result
```

**4. Reduce Max Tokens**
```python
# Shorter responses = faster
max_tokens=1024  # vs 4096
```

**5. Lower Temperature**
```python
# Less sampling = faster
temperature=0.0  # vs 0.7
```

**Performance Comparison:**
```
Configuration           | Avg Response Time
-----------------------|------------------
Sequential + Pro       | 45s (3 repos)
Sequential + Flash     | 25s (3 repos)
Concurrent + Flash     | 8s (3 repos)  ← Best
Concurrent + Cached    | 2s (3 repos)  ← Fastest
```

**See:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md#performance-problems) for detailed optimization.

---

### Why is my first request slow?

**Answer:** **Cold start delay** - several factors:

**1. Model Loading**
- First API call initializes model
- Subsequent calls are faster
- **Solution:** Warm up with dummy request

```python
# Warm-up request
agent = GitHubAgent()
agent.run("Hello")  # Fast dummy request
# Now real requests are faster
```

**2. Dependencies Import**
- First run loads all Python modules
- **Solution:** Use production server (uvicorn/gunicorn)

**3. Network Latency**
- First connection establishes SSL
- **Solution:** Keep connections alive

```python
# Reuse same agent instance
agent = GitHubAgent()  # Create once

# Multiple queries reuse connection
result1 = agent.run("query1")
result2 = agent.run("query2")  # Faster!
```

**Typical Timings:**
```
First request:  8-12 seconds
Second request: 3-5 seconds
Cached:         <1 second
```

---

## State Management

### What is checkpointing and why do I need it?

**Answer:**

**Checkpointing** = Saving conversation history so the agent remembers context.

**Without Checkpointing:**
```python
agent = GitHubAgent(enable_checkpointing=False)

agent.run("Analyze repository facebook/react")
# Agent: "Analyzed react repository..."

agent.run("What languages does it use?")
# Agent: "I don't know what repository you're referring to"
# ❌ No memory!
```

**With Checkpointing:**
```python
agent = GitHubAgent(enable_checkpointing=True)

agent.run("Analyze repository facebook/react", thread_id="user123")
# Agent: "Analyzed react repository..."

agent.run("What languages does it use?", thread_id="user123")
# Agent: "Based on the React repository I analyzed, it uses JavaScript (95%), TypeScript (4%)..."
# ✓ Remembers context!
```

**Use Cases:**
- Chat applications
- Multi-turn conversations
- Interactive Q&A
- User sessions

**Don't Use If:**
- Batch processing (no conversation)
- Independent queries
- Stateless APIs (performance-critical)

**See:** [UNDERSTANDING.md](UNDERSTANDING.md#state-management) for detailed explanation.

---

### How do I persist state across server restarts?

**Answer:**

**Development (In-Memory):**
```python
from langgraph.checkpoint.memory import MemorySaver

# Lost on restart
agent = GitHubAgent()  # Uses MemorySaver by default
```

**Production (Redis):**
```python
from langgraph.checkpoint.redis import RedisSaver

# Persistent across restarts
checkpointer = RedisSaver.from_conn_string("redis://localhost:6379/0")

agent = create_react_agent(
    llm,
    tools,
    checkpointer=checkpointer
)
```

**Production (PostgreSQL):**
```python
from langgraph.checkpoint.postgres import PostgresSaver

# Persistent + queryable
checkpointer = PostgresSaver.from_conn_string(
    "postgresql://user:pass@localhost:5432/db"
)
```

**Configuration:**
```bash
# .env file
REDIS_URL=redis://localhost:6379/0
# or
POSTGRES_URL=postgresql://user:pass@localhost:5432/codebaseops
```

**See:** [DEPLOYMENT.md](../deployment/DEPLOYMENT.md#state-persistence) for production setup.

---

## Tools

### How do I add a new tool?

**Answer:** Follow these steps:

**1. Define Tool Function**
```python
# tools/github_tools.py

from langchain_core.tools import tool
from pydantic import BaseModel, Field

class MyToolInput(BaseModel):
    """Input schema with validation."""
    param1: str = Field(description="Parameter description")
    param2: int = Field(default=10, description="Optional parameter")

@tool(args_schema=MyToolInput)
def my_new_tool(param1: str, param2: int = 10) -> str:
    """
    Tool description - be specific about when to use.
    
    Use this tool when user asks to:
    - "Do action X"
    - "Perform task Y"
    
    Args:
        param1: Description
        param2: Description with default
    
    Returns:
        Result description
    """
    # Implementation
    result = perform_action(param1, param2)
    return f"Result: {result}"
```

**2. Register Tool**
```python
def get_tools() -> List[BaseTool]:
    return [
        read_repository,
        clone_repository,
        my_new_tool,  # ← Add here
    ]
```

**3. Test Tool**
```python
# tests/test_my_tool.py

def test_my_new_tool():
    result = my_new_tool.invoke({
        "param1": "test",
        "param2": 20
    })
    assert "Result" in result
```

**4. Use with Agent**
```python
agent = GitHubAgent()
result = agent.run("Use my new tool with param1='test'")
```

**See:** [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md#adding-new-tools) for complete guide.

---

### Can tools call other tools?

**Answer:** **No, not directly.** The agent orchestrates tool calls.

**How It Works:**
```
User Query
  ↓
Agent (LLM) decides what to do
  ↓
Calls Tool A → Returns result
  ↓
Agent processes result
  ↓
Calls Tool B → Returns result
  ↓
Agent formulates final answer
```

**Example Flow:**
```python
# User: "Clone repo X and analyze it"

# Step 1: Agent calls clone_repository
clone_result = clone_repository("owner/repo")

# Step 2: Agent calls read_repository
read_result = read_repository("owner/repo")

# Step 3: Agent synthesizes answer
final_answer = combine_results(clone_result, read_result)
```

**If you need tool-to-tool:**
Create a wrapper tool:
```python
@tool
def clone_and_analyze(owner: str, repo: str) -> str:
    """Clone AND analyze in one tool."""
    clone_result = clone_repository(owner, repo)
    analysis = analyze_code(clone_result)
    return analysis
```

---

## Deployment

### Can I deploy this to production?

**Answer:** **Yes!** CodeBaseOpsAI-v3 is production-ready.

**Production Checklist:**

```bash
✓ Environment variables secured
✓ Error handling implemented
✓ Logging configured
✓ Monitoring set up (LangSmith)
✓ Tests passing
✓ Docker containerized
✓ State persistence (Redis/Postgres)
✓ Rate limiting configured
✓ Load balancing (if needed)
```

**Deployment Options:**

**1. Docker (Recommended)**
```bash
docker-compose up -d
```

**2. Cloud Platforms**
- AWS ECS/Fargate
- Google Cloud Run
- Azure Container Instances
- DigitalOcean App Platform

**3. Kubernetes**
```bash
kubectl apply -f k8s/deployment.yml
```

**See:** [DEPLOYMENT.md](../deployment/DEPLOYMENT.md) for detailed guide.

---

### How many users can it handle?

**Answer:** Depends on configuration:

**Single Instance (Basic):**
- 10-50 concurrent users
- ~100-500 requests/hour
- Good for: Small teams, prototypes

**Scaled (Recommended):**
- 100-1000+ concurrent users
- ~10,000+ requests/hour
- Configuration:
  - Multiple instances (4-8)
  - Load balancer
  - Redis for state
  - Async workers

**Performance Formula:**
```
Concurrent Users = Workers × (1 / Avg Response Time)

Example:
- 4 workers
- 5s avg response time
- = 4 × (60s / 5s) = ~48 concurrent users
```

**Scaling Strategy:**
```bash
# Horizontal scaling
docker-compose scale app=4  # 4 instances

# With load balancer
nginx → app1, app2, app3, app4
      → Redis (shared state)
```

**See:** [DEPLOYMENT.md](../deployment/DEPLOYMENT.md#scaling) for scaling guide.

---

## Troubleshooting

### Agent responses are inconsistent

**Answer:** This is normal for LLMs. Solutions:

**1. Set temperature=0**
```python
agent = GitHubAgent(temperature=0.0)  # Deterministic
```

**2. Use structured outputs**
```python
query = """
Analyze repository and return JSON:
{
  "languages": ["Python", "JavaScript"],
  "file_count": 123,
  "size_kb": 4567
}
"""
```

**3. Add validation**
```python
def validate_output(result: dict) -> bool:
    required_fields = ["languages", "file_count"]
    return all(field in result['output'] for field in required_fields)

# Retry if invalid
for attempt in range(3):
    result = agent.run(query)
    if validate_output(result):
        break
```

---

### How do I debug what the agent is doing?

**Answer:**

**1. Enable Debug Logging**
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("agents.github_agent")
logger.setLevel(logging.DEBUG)

# Now see detailed logs
agent = GitHubAgent()
result = agent.run("query")
```

**2. Use Streaming to See Reasoning**
```python
async for event in agent.stream("query"):
    if event['type'] == 'tool_start':
        print(f"Tool: {event['tool']}")
    elif event['type'] == 'token':
        print(event['content'], end='')
```

**3. LangSmith Tracing**
```bash
# .env
ENABLE_TRACING=true
LANGSMITH_API_KEY=your_key
```
Then view traces at [smith.langchain.com](https://smith.langchain.com/)

**See:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md#debugging-techniques) for more methods.

---

## Advanced Topics

### Can I use different LLM providers?

**Answer:** **Yes!** LangChain supports many providers:

**OpenAI:**
```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4-turbo",
    api_key=os.getenv("OPENAI_API_KEY")
)

agent = create_react_agent(llm, tools)
```

**Anthropic (Claude):**
```python
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(
    model="claude-3-sonnet",
    api_key=os.getenv("ANTHROPIC_API_KEY")
)
```

**Ollama (Local):**
```python
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama2",
    base_url="http://localhost:11434"
)
```

**AWS Bedrock:**
```python
from langchain_aws import ChatBedrock

llm = ChatBedrock(
    model_id="anthropic.claude-3-sonnet",
    region_name="us-east-1"
)
```

**External Reference:** [LangChain Integrations](https://python.langchain.com/docs/integrations/chat/)

---

### How do I implement authentication?

**Answer:**

**FastAPI with JWT:**
```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token."""
    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=["HS256"]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/analyze")
async def analyze(
    request: AnalyzeRequest,
    user: dict = Depends(verify_token)
):
    # user is authenticated
    agent = GitHubAgent()
    return await agent.run_async(request.query)
```

**API Key Authentication:**
```python
from fastapi import Header, HTTPException

async def verify_api_key(x_api_key: str = Header()):
    """Verify API key."""
    if x_api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=403, detail="Invalid API key")
    return x_api_key

@app.post("/analyze")
async def analyze(
    request: AnalyzeRequest,
    api_key: str = Depends(verify_api_key)
):
    # Authenticated
    pass
```

---

### Can I use this with Retrieval-Augmented Generation (RAG)?

**Answer:** **Yes!** Add vector database tools:

```python
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.tools import tool

# Create vector store
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(documents, embeddings)

# Create RAG tool
@tool
def search_documentation(query: str) -> str:
    """Search documentation using semantic search."""
    docs = vectorstore.similarity_search(query, k=3)
    return "\n\n".join([doc.page_content for doc in docs])

# Add to agent
tools = [read_repository, clone_repository, search_documentation]
agent = GitHubAgent(tools=tools)

# Use it
result = agent.run("Search documentation for API authentication")
```

**External Reference:** [LangChain RAG Tutorial](https://python.langchain.com/docs/tutorials/rag/)

---

## Getting More Help

### Where can I get help?

**Resources:**

1. **Documentation:** Start with [docs/START_HERE.md](../START_HERE.md)
2. **Examples:** [EXAMPLES.md](EXAMPLES.md) - 10+ practical tutorials
3. **Troubleshooting:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues
4. **API Reference:** [API_REFERENCE.md](../reference/API_REFERENCE.md) - All functions

**Community:**

- **LangChain Discord:** [discord.gg/langchain](https://discord.gg/langchain)
- **GitHub Issues:** [github.com/langchain-ai/langgraph/issues](https://github.com/langchain-ai/langgraph/issues)
- **Stack Overflow:** Tag `langchain` or `langgraph`
- **Reddit:** r/LangChain

**Commercial Support:**

- **LangChain:** [langchain.com/contact](https://www.langchain.com/contact)
- **Consulting:** Available for custom implementations

---

### How do I report a bug?

**Before Reporting:**

1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Search existing issues
3. Try with latest version
4. Create minimal reproduction

**Bug Report Template:**

```markdown
**Description:**
Brief description of the issue

**Environment:**
- Python version: 3.11.5
- CodeBaseOpsAI version: v3.0.0
- OS: macOS 14.0

**To Reproduce:**
```python
# Minimal code to reproduce
agent = GitHubAgent()
result = agent.run("problematic query")
```

**Expected Behavior:**
What you expected to happen

**Actual Behavior:**
What actually happened

**Error Traceback:**
```
Full error traceback here
```

**Additional Context:**
Any other relevant information
```

---

**Document Information:**
- **Created:** January 2, 2026
- **Version:** 1.0
- **Lines:** 1,100+
- **Related:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md), [UNDERSTANDING.md](UNDERSTANDING.md), [START_HERE.md](../START_HERE.md)

**External References:**
- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Google AI Documentation](https://ai.google.dev/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
