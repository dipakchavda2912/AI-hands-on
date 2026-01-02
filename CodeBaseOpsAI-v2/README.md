# CodeBaseOpsAI v2 - Learning Version

This is the **learning/educational version** of CodeBaseOpsAI with minimal fixes to make the ReAct agent work.

## What's in v2?

This version contains your original code with **only the essential fixes** to run with LangChain 1.2.0:

- ✅ Fixed imports to use `langchain_classic.agents`
- ✅ Uses `create_react_agent` instead of deprecated tool-calling agent
- ✅ Simple `@tool` decorator for GitHub tools
- ✅ Basic ReAct agent with no production features

## Structure

```
CodeBaseOpsAI-v2/
├── agents/
│   └── github_agent.py       # Simple ReAct agent (~93 lines)
├── tools/
│   └── github_tools.py       # Simple tools with @tool decorator (~68 lines)
├── prompts/
│   └── github_prompts.py     # Original prompts
├── utils/                    # Original utility files
├── main.py                   # Simple example (~48 lines)
└── requirements.txt          # Dependencies
```

## Running the Code

```bash
# Activate virtual environment
source .venv/bin/activate

# Run the agent
python main.py
```

## For Production Code

👉 **See CodeBaseOpsAI-v3** for the production-grade implementation with:
- Modern LangGraph agent
- Async/streaming support
- State management
- REST API
- Tests and Docker deployment
- Complete documentation

## Key Differences from v3

| Feature | v2 (Learning) | v3 (Production) |
|---------|---------------|-----------------|
| Framework | langchain_classic | LangGraph |
| Lines of code | ~200 | ~800+ |
| State management | ❌ | ✅ |
| Async support | ❌ | ✅ |
| Streaming | ❌ | ✅ |
| API server | ❌ | ✅ |
| Tests | ❌ | ✅ |
| Docker | ❌ | ✅ |
| Pydantic validation | ❌ | ✅ |

Keep v2 for learning and understanding basics. Use v3 for production applications!
