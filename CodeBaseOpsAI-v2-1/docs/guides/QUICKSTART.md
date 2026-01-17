# 🚀 Quick Start Guide - CodeBaseOpsAI-v2-1

**Get up and running with the GitHub operations AI agent in under 10 minutes.**

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed and configured:

### Required Software

| Tool | Minimum Version | Check Command | Notes |
|------|----------------|---------------|-------|
| **Python** | 3.11+ | `python --version` | Python 3.11, 3.12, or 3.13 recommended |
| **pip** | Latest | `pip --version` | Package manager for Python |
| **git** | 2.0+ | `git --version` | For repository operations |
| **venv** | Included with Python | `python -m venv --help` | For virtual environments |

### Required API Keys

You'll need two API keys:

#### 1. Google Gemini API Key (Required)
- **Purpose**: Powers the AI agent with Google Gemini 2.5 Flash
- **Get it from**: [Google AI Studio](https://aistudio.google.com/app/apikey)
- **Free tier**: Yes (generous free quota)
- **Setup**: 
  1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
  2. Click "Create API Key"
  3. Copy the generated key

#### 2. GitHub Personal Access Token (Optional but Recommended)
- **Purpose**: Access private repositories and higher rate limits
- **Get it from**: [GitHub Settings → Developer Settings → Personal Access Tokens](https://github.com/settings/tokens)
- **Permissions needed**: `repo` (full control of private repositories)
- **Setup**:
  1. Go to GitHub Settings → Developer Settings → Personal Access Tokens → Tokens (classic)
  2. Click "Generate new token (classic)"
  3. Select scopes: `repo` (all sub-scopes)
  4. Generate token and copy it immediately

---

## 📦 Installation

Follow these steps to install and configure CodeBaseOpsAI-v2-1:

### Step 1: Clone the Repository

```bash
# Clone the repository (adjust path to your preferred location)
cd ~/Projects
git clone <your-repo-url> AI-hands-on
cd AI-hands-on/CodeBaseOpsAI-v2-1
```

Or if you already have the codebase:

```bash
# Navigate to the project directory
cd /path/to/AI-hands-on/CodeBaseOpsAI-v2-1
```

### Step 2: Create Virtual Environment

```bash
# Create a new virtual environment
python3 -m venv .venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
# .venv\Scripts\activate
```

You should see `(.venv)` prefix in your terminal prompt.

### Step 3: Upgrade pip (Recommended)

```bash
# Upgrade pip to the latest version
pip install --upgrade pip
```

### Step 4: Install Dependencies

```bash
# Install all required Python packages
pip install -r requirements.txt
```

This will install:
- `langchain==1.2.0` - Core LangChain framework
- `langchain-google-genai==4.1.2` - Google Gemini integration
- `langchain-classic==1.0.1` - Classic agent implementations
- `GitPython==3.1.46` - GitHub operations
- `python-dotenv` - Environment variable management
- And many more dependencies (see [requirements.txt](../../requirements.txt))

**Installation time**: ~2-3 minutes depending on your internet connection.

### Step 5: Verify Installation

```bash
# Check if LangChain is installed correctly
python -c "import langchain; print(f'LangChain {langchain.__version__} installed successfully')"

# Check Google GenAI integration
python -c "import langchain_google_genai; print('Google GenAI integration ready')"
```

Expected output:
```
LangChain 1.2.0 installed successfully
Google GenAI integration ready
```

---

## ⚙️ Environment Configuration

Configure your API keys and environment variables:

### Step 1: Create .env File

```bash
# Create .env file from template (if you have one)
# or create it manually:
touch .env
```

### Step 2: Add Your API Keys

Open `.env` in your favorite editor and add:

```bash
# Google Gemini API Key (Required)
GOOGLE_API_KEY=your_google_api_key_here

# GitHub Personal Access Token (Optional)
GITHUB_TOKEN=your_github_token_here
```

**Important Security Notes:**
- ⚠️ Never commit `.env` to version control
- ⚠️ Keep your API keys secure and private
- ⚠️ Add `.env` to `.gitignore` (should already be there)

### Step 3: Verify Environment Variables

```bash
# Check if environment variables are loaded
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('GOOGLE_API_KEY:', 'SET' if os.getenv('GOOGLE_API_KEY') else 'NOT SET')"
```

Expected output:
```
GOOGLE_API_KEY: SET
```

---

## 🎯 Quick Run Example

Now let's run the agent with a simple example:

### Default Example (Repository Analysis)

The default `main.py` is configured to analyze a GitHub repository and perform package updates.

```bash
# Make sure you're in the project directory and virtual environment is activated
python main.py
```

### What Happens:

1. **Repository Selection**: The agent targets `dipakchavda2912/base-serverless`
2. **Cloning**: Repository is cloned to `/tmp/base-serverless-<timestamp>/`
3. **Branch**: Works on the `develop` branch
4. **Node.js Version**: Uses LTS version 22.11.0 for package compatibility
5. **Operations**: Performs a series of automated tasks:
   - Clone repository
   - Analyze package.json
   - Check package versions against NPM registry
   - Scan for vulnerabilities
   - Update serverless.yml configurations
   - Generate reports

### Custom Repository Example

To analyze your own repository, modify [main.py](../../main.py):

```python
# Edit the get_query method in main.py
def get_query(self) -> List[str]:
    source_repository = "your-username/your-repo"  # Change this
    parent_folder_name = f"your-repo-{ExecutionUtils.get_current_datetime_string()}"
    clone_path = f"/tmp/{parent_folder_name}/your-repo-clone/"
    branch = "main"  # Change to your branch
    
    # Rest remains the same...
```

Then run:

```bash
python main.py
```

---

## 🔍 What to Expect When Running

### Console Output

You'll see structured output with progress indicators:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 QUERY 1/12
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Clone GitHub repository dipakchavda2912/base-serverless to /tmp/...
Branch: develop

════════════════════════════════════════════════════════════════

> Entering new AgentExecutor chain...

Agent: Calling tool: clone_github_repository...
Tool Response: Repository cloned successfully
Agent: Repository has been cloned to /tmp/base-serverless-20260117143022/

✅ Query 1 completed successfully
```

### Agent Behavior

The agent uses **ReAct (Reasoning + Acting)** pattern:

1. **Thought**: Agent analyzes what needs to be done
2. **Action**: Agent selects and calls appropriate tools
3. **Observation**: Agent observes tool results
4. **Repeat**: Until task is complete

Example reasoning chain:
```
Thought: I need to clone the repository first
Action: clone_github_repository
Observation: Repository cloned successfully to /tmp/...

Thought: Now I should read the package.json file
Action: read_file_from_repository
Observation: package.json contents retrieved

Thought: I can see the dependencies, let me check versions
Action: check_package_versions
...
```

### Execution Summary

At the end, you'll see a summary:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 EXECUTION SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total Queries: 12
✅ Successful: 11
❌ Failed: 1
⏭️  Skipped: 0

Overall Status: ⚠️  COMPLETED WITH ERRORS
```

### Output Files

Generated files will be in the cloned repository:

```
/tmp/base-serverless-<timestamp>/
├── base-serverless-clone/          # Cloned repository
│   ├── package.json                # Original + updated
│   ├── serverless.yml              # Updated configurations
│   └── ...
└── reports/                        # Generated reports (if any)
    ├── vulnerabilities.json
    └── package-updates.json
```

---

## 🛠️ Basic Customization

### 1. Change Target Repository

Edit [main.py](../../main.py):

```python
def get_query(self) -> List[str]:
    source_repository = "owner/repository"  # Your repository
    branch = "main"                          # Your branch
    # ...
```

### 2. Change Node.js LTS Version

For different Node.js compatibility:

```python
class Main():
    node_lts_version = '20.11.0'  # Change to 18.x, 20.x, or 22.x
```

### 3. Modify AI Model Parameters

Edit [src/agent.py](../../src/agent.py):

```python
def init_llm(self) -> ChatGoogleGenerativeAI:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,              # 0 = deterministic, 1 = creative
        max_output_tokens=2048,     # Increase for longer responses
        api_key=os.getenv("GOOGLE_API_KEY")
    )
    return llm
```

### 4. Customize Package List

Edit [src/services/instruction_service.py](../../src/services/instruction_service.py):

```python
self.node_packages = [
    {"name": "your-package", "is_dev": False, "npm_lookup": True},
    # Add your packages here
]
```

### 5. Change Clone Location

```python
def get_query(self) -> List[str]:
    # Use a different base path
    clone_path = f"/Users/your-username/temp/{parent_folder_name}/"
```

### 6. Add Custom Instructions

Create a new instruction file in [src/instructions/](../../src/instructions/):

```python
# src/instructions/my_custom_instructions.py
class MyCustomInstructions:
    def __init__(self, repository: str, clone_path: str):
        self.repository = repository
        self.clone_path = clone_path
    
    def get_instructions(self) -> List[str]:
        return [
            f"Analyze code quality in {self.clone_path}",
            f"Generate documentation for {self.repository}",
        ]
```

Then integrate in [src/services/instruction_service.py](../../src/services/instruction_service.py):

```python
from src.instructions.my_custom_instructions import MyCustomInstructions

def get_all_instructions(self) -> List[str]:
    # ... existing code ...
    custom = MyCustomInstructions(self.repository, self.clone_path)
    instructions.extend(custom.get_instructions())
    return instructions
```

---

## 🎓 Next Steps

### 1. Understand the Architecture

Read the comprehensive documentation:

- **[START_HERE.md](../START_HERE.md)** - Complete system overview (30 min read)
- **[TECHNICAL_DOCUMENTATION.md](../../TECHNICAL_DOCUMENTATION.md)** - Deep dive into implementation

### 2. Explore the Tools

The agent has access to multiple tool categories:

#### GitHub Tools
- `clone_github_repository` - Clone any public/private repository
- `read_file_from_repository` - Read file contents
- `list_directory_contents` - Browse directory structure
- `search_files_in_repository` - Find files by pattern

#### Package Management Tools
- `check_package_versions` - Check NPM package versions
- `get_latest_compatible_version` - Find compatible updates
- `check_package_vulnerabilities` - Scan for security issues
- `validate_semantic_version` - Validate version constraints

#### Configuration Tools
- `read_yaml_file` - Parse YAML configurations
- `update_yaml_file` - Modify YAML files
- `read_json_file` - Parse JSON files
- `update_json_file` - Modify JSON files

📖 **Learn more**: See [src/tools/](../../src/tools/) for complete tool implementations

### 3. Advanced Configuration

#### Enable Debug Logging

Add to your `.env`:

```bash
LANGCHAIN_VERBOSE=true
LANGCHAIN_TRACING_V2=false  # Set to true for LangSmith tracing
```

#### LangSmith Integration (Optional)

For advanced debugging and monitoring:

1. Sign up at [LangSmith](https://smith.langchain.com/)
2. Get your API key
3. Add to `.env`:

```bash
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=CodeBaseOpsAI-v2-1
```

### 4. Common Use Cases

#### Use Case 1: Dependency Audit

Analyze all dependencies for updates and vulnerabilities:

```python
# In instruction_service.py, focus only on package operations
def get_all_instructions(self) -> List[str]:
    return [
        f"Clone repository {self.repository} to {self.clone_path}",
        f"Read package.json from {self.clone_path}",
        f"Check all package versions for updates",
        f"Scan for known vulnerabilities",
        f"Generate update recommendations",
    ]
```

#### Use Case 2: Configuration Validation

Validate serverless.yml configurations:

```python
def get_all_instructions(self) -> List[str]:
    return [
        f"Clone {self.repository} to {self.clone_path}",
        f"Read serverless.yml",
        f"Validate provider configuration",
        f"Check plugin versions",
        f"Verify custom tags",
    ]
```

#### Use Case 3: Bulk Repository Analysis

Analyze multiple repositories:

```python
repositories = [
    "owner/repo1",
    "owner/repo2",
    "owner/repo3",
]

for repo in repositories:
    # Initialize agent for each repo
    instruction_service = InstructionService(
        repository=repo,
        clone_path=f"/tmp/{repo.split('/')[1]}-clone/",
        branch="main",
        node_lts_version=self.node_lts_version
    )
    # Execute queries...
```

### 5. Troubleshooting

#### Common Issues and Solutions

**Issue: `ModuleNotFoundError: No module named 'langchain'`**
```bash
# Solution: Ensure virtual environment is activated
source .venv/bin/activate
pip install -r requirements.txt
```

**Issue: `GOOGLE_API_KEY not found`**
```bash
# Solution: Check .env file exists and is properly formatted
cat .env  # Should show GOOGLE_API_KEY=your_key
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('GOOGLE_API_KEY'))"
```

**Issue: `API rate limit exceeded`**
```bash
# Solution: Add GITHUB_TOKEN to .env for higher limits
# Or wait for rate limit to reset (1 hour for unauthenticated requests)
```

**Issue: `Repository clone failed`**
```bash
# Solution: Check repository access and token permissions
git clone https://github.com/owner/repo.git  # Test manually
# For private repos, ensure GITHUB_TOKEN has 'repo' scope
```

**Issue: Agent gets stuck in a loop**
```bash
# Solution: Review agent prompts and add more specific instructions
# Check that tool responses are clear and actionable
# Consider reducing temperature to 0 for more deterministic behavior
```

---

## 📚 Additional Resources

### Documentation

- **[README.md](../../README.md)** - Project overview and version info
- **[TECHNICAL_DOCUMENTATION.md](../../TECHNICAL_DOCUMENTATION.md)** - Complete technical reference
- **[START_HERE.md](../START_HERE.md)** - Comprehensive learning guide

### Code Structure

```
CodeBaseOpsAI-v2-1/
├── main.py                          # Entry point (your starting point)
├── requirements.txt                 # Dependencies list
├── .env                            # Environment variables (create this)
│
├── src/
│   ├── agent.py                    # Agent initialization
│   ├── agent_prompt.py             # System prompts
│   │
│   ├── tools/                      # Tool implementations
│   │   ├── github_tools.py         # GitHub operations
│   │   ├── package_updates_tools.py # NPM package tools
│   │   ├── yaml_tools.py           # YAML operations
│   │   └── json_tools.py           # JSON operations
│   │
│   ├── schemas/                    # Pydantic validation schemas
│   │   ├── github_schemas.py
│   │   ├── package_schemas.py
│   │   ├── yaml_schemas.py
│   │   └── json_schemas.py
│   │
│   ├── services/                   # Business logic services
│   │   └── instruction_service.py  # Query generation
│   │
│   ├── instructions/               # Instruction templates
│   │   ├── github_instructions.py
│   │   ├── nodejs_packages_instructions.py
│   │   └── serverless_*_instructions.py
│   │
│   └── utils/                      # Utility functions
│       ├── execution_utils.py      # Execution management
│       ├── package_utils.py        # NPM utilities
│       └── github_utils.py         # GitHub utilities
│
└── docs/
    ├── START_HERE.md               # Learning guide
    └── guides/
        └── QUICKSTART.md           # This file!
```

### External Links

- **[LangChain Documentation](https://python.langchain.com/)** - Official LangChain docs
- **[Google Gemini API](https://ai.google.dev/)** - Gemini API documentation
- **[NPM Registry API](https://github.com/npm/registry/blob/master/docs/REGISTRY-API.md)** - NPM API reference
- **[GitHub API](https://docs.github.com/en/rest)** - GitHub REST API docs

---

## 🎉 You're Ready!

Congratulations! You've completed the quick start guide. You should now be able to:

- ✅ Install and configure CodeBaseOpsAI-v2-1
- ✅ Set up API keys and environment variables
- ✅ Run the default agent example
- ✅ Understand what the agent is doing
- ✅ Customize for your own use cases
- ✅ Troubleshoot common issues

### Quick Reference Commands

```bash
# Activate environment
source .venv/bin/activate

# Run the agent
python main.py

# Check environment
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('Ready to go!' if os.getenv('GOOGLE_API_KEY') else 'Set GOOGLE_API_KEY first')"

# Deactivate environment when done
deactivate
```

---

**Need Help?**
- 📖 Read [START_HERE.md](../START_HERE.md) for detailed explanations
- 🔧 Check [TECHNICAL_DOCUMENTATION.md](../../TECHNICAL_DOCUMENTATION.md) for implementation details
- 💬 Review the code in [src/](../../src/) for examples

**Happy Coding!** 🚀
