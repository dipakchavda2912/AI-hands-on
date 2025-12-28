# AI-hands-on
This repository contains my handson work on AI

# Setup guidelines

## 1. Clone the repository
```sh
git clone <repo-url>
cd AI-hands-on/CodeBaseOpsAI
```

## 2. Install Python 3.12 (if not already installed)
On macOS, use Homebrew:
```sh
brew install python@3.12
```

## 3. Create and activate a Python 3.12 virtual environment
```sh
python3.12 -m venv .venv
source .venv/bin/activate
```

## 4. Upgrade pip
```sh
pip install --upgrade pip
```

## 5. Install dependencies
```sh
pip install -r requirements.txt
```

## 5. Add .venv to .gitignore
Ensure `.venv` is listed in `.gitignore` to avoid committing your local environment.

## 6. Troubleshooting
If you see `ERROR: Could not open requirements file: [Errno 2] No such file or directory: 'requirements.txt'`, make sure you are in the `CodeBaseOpsAI` directory before running the install command.
