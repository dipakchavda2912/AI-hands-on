# CodeBaseOpsAI-v2-1 Tests

This directory contains tests for the CodeBaseOpsAI-v2-1 project.

## Structure

```
tests/
├── conftest.py                    # Shared pytest fixtures
├── __init__.py                    # Package initialization
├── unit/                          # Unit tests
│   ├── __init__.py
│   ├── test_yaml_utils.py        # Tests for YAML utilities
│   ├── test_yaml_tools.py        # Tests for YAML LangChain tools
│   ├── test_github_utils.py      # Tests for GitHub utilities
│   ├── test_github_tools.py      # Tests for GitHub LangChain tools
│   └── old_tests_backup/         # Backup of previous test files
└── integration/                   # Integration tests
    ├── __init__.py
    └── test_agent_integration.py  # Tests for complete agent workflow
```

## Running Tests

### Run all tests
```bash
pytest
```

### Run only unit tests
```bash
pytest tests/unit/
```

### Run only integration tests
```bash
pytest tests/integration/
```

### Run with coverage
```bash
pytest --cov=src --cov-report=html
```

### Run specific test file
```bash
pytest tests/unit/test_yaml_utils.py
```

### Run specific test class
```bash
pytest tests/unit/test_yaml_utils.py::TestYamlUtils
```

### Run specific test method
```bash
pytest tests/unit/test_yaml_utils.py::TestYamlUtils::test_parse_yaml
```

## Fixtures

The `conftest.py` file contains shared fixtures:

- `temp_yaml_file`: Creates a temporary YAML file with sample serverless.yml structure
- `temp_yaml_with_custom_string`: Creates a YAML file with `custom: '{}'` (string instead of dict)
- `temp_directory`: Provides a temporary directory for file operations
- `sample_repo_url`: Returns a sample GitHub repository URL for testing

## Test Organization

### Unit Tests
- Test individual functions and classes in isolation
- Mock external dependencies (GitHub API, file system where appropriate)
- Fast and deterministic

### Integration Tests
- Test the complete agent workflow
- May require actual API calls (marked with `@pytest.mark.skip` if so)
- Test interaction between multiple components

## Notes

- Tests marked with `@pytest.mark.skip` require actual API tokens or long-running operations
- Use environment variables for sensitive data (e.g., `GITHUB_TOKEN`)
- Old test files are backed up in `tests/unit/old_tests_backup/`
