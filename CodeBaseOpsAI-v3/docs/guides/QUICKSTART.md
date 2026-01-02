# CodeBaseOpsAI v3 - Quick Reference

## 🚀 Installation (30 seconds)

```bash
cd CodeBaseOpsAI-v3
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-production.txt
echo "GOOGLE_API_KEY=your_key" >> .env
python main.py
```

## 📝 Common Commands

### Run Examples
```bash
python main.py                    # All examples
```

### Run API Server
```bash
pip install -r requirements-api.txt
uvicorn api_server:app --reload
```

### Run with Docker
```bash
docker-compose up -d              # Start all services
docker-compose logs -f api        # View logs
docker-compose down               # Stop
```

### Run Tests
```bash
pip install pytest pytest-asyncio
pytest tests/ -v                  # All tests
pytest tests/test_github_agent.py # Specific test
```

## 💻 Code Snippets

### Simple Usage
```python
from tools.github_tools import GithubTools
from agents.github_agent import GithubAgent

tools = GithubTools().get_tools()
agent = GithubAgent(tools=tools)
result = agent.run("Clone repo owner/name")
print(result['output'])
```

### Async Usage
```python
import asyncio

async def main():
    result = await agent.run_async("Your request")
    print(result)

asyncio.run(main())
```

### Streaming
```python
async for chunk in agent.stream("Your request"):
    print(chunk)
```

### API Call
```bash
curl -X POST http://localhost:8000/agent/run \
  -H "Content-Type: application/json" \
  -d '{"request": "Clone repo xyz"}'
```

## 📁 Key Files

- `agents/github_agent.py` - Main agent logic
- `tools/github_tools.py` - Tool definitions
- `main.py` - Usage examples
- `api_server.py` - REST API
- `config.py` - Configuration
- `.env` - Environment variables

## 🔗 Documentation

- [README.md](README.md) - Quick start
- [README-PRODUCTION.md](../deployment/README-PRODUCTION.md) - Full features
- [COMPARISON.md](../migration/COMPARISON.md) - v2 vs v3
- [DEPLOYMENT.md](../deployment/DEPLOYMENT.md) - Production deployment
- [MIGRATION.md](../migration/MIGRATION.md) - Migration guide

## ⚡ Quick Tips

1. Always activate virtual environment first
2. Configure `.env` before running
3. Use `python main.py` for quick tests
4. Use API server for production
5. Check logs for debugging
6. Run tests before deploying

## 🆘 Troubleshooting

**Import Error?**
```bash
source .venv/bin/activate
pip install -r requirements-production.txt
```

**API Key Error?**
```bash
echo "GOOGLE_API_KEY=your_actual_key" >> .env
```

**Port Already in Use?**
```bash
uvicorn api_server:app --port 8001
```

**Docker Issues?**
```bash
docker-compose down
docker-compose up --build
```

---

**For detailed information, see [README.md](README.md)**
