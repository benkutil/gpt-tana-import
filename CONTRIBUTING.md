# Contributing to ChatGPT to Tana Import Tool

Thank you for your interest in contributing! This document provides guidelines and instructions for development.

## Development Setup

### Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- Git

### Setting Up Your Development Environment

1. **Clone the repository:**
   ```bash
   git clone https://github.com/benkutil/gpt-tana-import.git
   cd gpt-tana-import
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Install the package in editable mode:**
   ```bash
   pip install -e .
   ```

## Running Quality Checks

We use multiple tools to ensure code quality. You can run them individually or all at once.

### Quick Start with Make

```bash
# See all available targets
make help

# Install development dependencies
make install-dev

# Run all quality checks
make check

# Run tests with coverage
make test

# Auto-format code
make format

# Run linters
make lint

# Run type checking
make type-check

# Run security scans
make security

# Clean generated files
make clean
```

### Individual Tools

**Code Formatting:**
```bash
# Check formatting (use before committing)
black --check src tests

# Auto-format code
black src tests

# Check import sorting
isort --check-only src tests

# Auto-sort imports
isort src tests
```

**Linting:**
```bash
# Run flake8
flake8 src tests

# Run pylint
pylint src
```

**Type Checking:**
```bash
mypy src
```

**Security Scanning:**
```bash
# Check code for security issues
bandit -r src -c .bandit

# Check dependencies for vulnerabilities
safety check

# Audit Python packages
pip-audit
```

**Testing:**
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=src/tana_import

# Run tests with verbose output
pytest -v

# Run specific test file
pytest tests/test_config.py

# Run tests matching a pattern
pytest -k "test_config"
```

### Run All Checks

Use the helper script to run all quality checks at once:

```bash
./scripts/check-all.sh
```

## Code Style Guidelines

### Python Code Style

- **Line length:** Maximum 100 characters
- **Formatting:** Use `black` (enforced automatically)
- **Import sorting:** Use `isort` with black profile
- **Docstrings:** Use Google style docstrings for all public functions and classes
- **Type hints:** Required for all function signatures

### Example Function

```python
def parse_export_file(file_path: Path) -> List[ChatGPTConversation]:
    """Parse a ChatGPT export JSON file.

    Args:
        file_path: Path to the ChatGPT export JSON file.

    Returns:
        List of ChatGPTConversation objects.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file is not valid JSON.
    """
    # Implementation here
```

## Testing Guidelines

### Coverage Requirements

- **Overall coverage:** ≥80%
- **Critical modules (parser, converter):** ≥90%
- **CLI/integration modules:** ≥70%

### Writing Tests

1. **Test file naming:** `test_<module_name>.py`
2. **Test function naming:** `test_<what_is_being_tested>()`
3. **Use fixtures:** Define reusable test data in `conftest.py`
4. **Use parametrization:** For testing multiple scenarios
5. **Mock external dependencies:** Use `pytest-mock` for API calls, file I/O, etc.

### Example Test

```python
def test_tana_config_from_env_success(mock_tana_config: None) -> None:
    """Test loading configuration from environment variables."""
    config = TanaConfig.from_env()
    assert config.api_endpoint == "https://api.tana.example/addToNodeV2"
    assert config.api_token == "test_token_123"
```

## Pull Request Process

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the code style guidelines

3. **Run all quality checks:**
   ```bash
   ./scripts/check-all.sh
   ```

4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request** on GitHub

### Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Adding or updating tests
- `refactor:` Code refactoring
- `style:` Code style changes (formatting, etc.)
- `chore:` Maintenance tasks

## Project Structure

```
gpt-tana-import/
├── src/tana_import/       # Source code
│   ├── __init__.py
│   ├── cli.py             # CLI entry point
│   ├── parser.py          # ChatGPT JSON parser
│   ├── converter.py       # Convert to Tana events
│   ├── api_client.py      # Tana API client
│   ├── config.py          # Configuration handling
│   └── models.py          # Data models
├── tests/                 # Test suite
│   ├── conftest.py        # Pytest fixtures
│   ├── test_*.py          # Test files
│   ├── fixtures/          # Test data
│   └── integration/       # Integration tests
├── docs/                  # Documentation
├── .github/workflows/     # CI/CD pipelines
└── scripts/               # Helper scripts
```

## Getting Help

- **Issues:** Check existing [GitHub issues](https://github.com/benkutil/gpt-tana-import/issues)
- **Discussions:** Start a discussion for questions or ideas
- **Documentation:** See [docs/](docs/) for detailed documentation

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License.
