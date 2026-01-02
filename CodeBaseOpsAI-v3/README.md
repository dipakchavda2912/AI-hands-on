# CodeBaseOpsAI v3

**Production-grade AI agent system for GitHub operations using LangGraph.**

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements-production.txt

# Configure API key
echo "GOOGLE_API_KEY=your_key_here" > .env

# Run examples
python main.py
```

## 📚 Documentation

All documentation is organized in the [`docs/`](docs/) folder:

### 📖 Guides
- **[Getting Started](docs/guides/README.md)** - Installation and quick start
- **[Documentation Index](docs/guides/DOCUMENTATION_INDEX.md)** - Navigation guide to all docs
- **[Documentation Summary](docs/guides/DOCUMENTATION_SUMMARY.md)** - Overview of all documentation
- **[Quick Reference](docs/guides/QUICKSTART.md)** - Command reference
- **[Success Summary](docs/guides/SUCCESS.md)** - Project summary

### 🔧 Technical Reference
- **[Architecture](docs/reference/ARCHITECTURE.md)** - Complete system architecture and execution flows
- **[API Reference](docs/reference/API_REFERENCE.md)** - Complete function and API documentation

### 🚀 Deployment
- **[Deployment Guide](docs/deployment/DEPLOYMENT.md)** - Docker, production deployment
- **[Production README](docs/deployment/README-PRODUCTION.md)** - Production features

### 🔄 Migration
- **[Migration Guide](docs/migration/MIGRATION.md)** - Upgrading from v2 to v3
- **[Comparison](docs/migration/COMPARISON.md)** - v2 vs v3 differences

## 🎯 Where to Start?

| Your Goal | Read This |
|-----------|-----------|
| **Understand how it works** | [Architecture](docs/reference/ARCHITECTURE.md) |
| **Build with the API** | [API Reference](docs/reference/API_REFERENCE.md) |
| **Deploy to production** | [Deployment Guide](docs/deployment/DEPLOYMENT.md) |
| **Migrate from v2** | [Migration Guide](docs/migration/MIGRATION.md) |
| **Quick commands** | [Quick Reference](docs/guides/QUICKSTART.md) |

## 📂 Project Structure

```
CodeBaseOpsAI-v3/
├── docs/                      # All documentation
│   ├── guides/               # Getting started & navigation
│   ├── reference/            # Technical documentation
│   ├── deployment/           # Production deployment
│   └── migration/            # v2 to v3 migration
├── agents/                    # Agent implementation
├── tools/                     # GitHub tools
├── tests/                     # Test suite
├── config.py                  # Configuration
├── main.py                    # Example usage
└── api_server.py             # REST API server
```

## ✨ Features

- ✅ LangGraph agent orchestration
- ✅ Async/streaming support
- ✅ State management with checkpointing
- ✅ REST API with FastAPI
- ✅ Pydantic validation
- ✅ Docker deployment ready
- ✅ Comprehensive test suite

## 📖 Full Documentation

👉 **Start here:** [Documentation Index](docs/guides/DOCUMENTATION_INDEX.md)

For complete technical documentation, see the [`docs/`](docs/) folder.
