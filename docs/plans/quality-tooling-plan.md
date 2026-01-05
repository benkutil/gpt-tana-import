# Quality Tooling Implementation Plan

**Created:** 2026-01-01
**Status:** Planned
**Purpose:** Establish testing infrastructure, linting, and code quality tools for the ChatGPT to Tana import project

---

## Overview

This plan outlines the quality tooling and testing infrastructure needed to ensure code quality, reliability, and maintainability for the ChatGPT to Tana import tool.

## Goals

1. **Code Quality**: Establish linting and formatting standards
2. **Testing**: Implement comprehensive unit and integration tests
3. **CI/CD**: Automate quality checks in continuous integration
4. **Documentation**: Ensure code is well-documented and maintainable
5. **Security**: Add security scanning for dependencies and code

---

## Technology Stack Selection

### Programming Language
**Decision: Python 3.9+**

Rationale:
- Excellent JSON parsing capabilities
- Rich ecosystem for CLI tools (argparse, click)
- Strong HTTP/API client libraries
- Great testing frameworks
- Good datetime/timezone handling

Alternative considered: Node.js/TypeScript (also viable, but Python chosen for simplicity and fewer build steps)

### Testing Framework
**pytest**
- Industry standard for Python testing
- Rich plugin ecosystem
- Excellent fixtures and parametrization support
- Good integration with coverage tools

### Code Quality Tools

1. **Linting & Formatting**
   - `black` - Opinionated code formatter (uncompromising)
   - `flake8` - Style guide enforcement (PEP 8)
   - `pylint` - More comprehensive static analysis
   - `isort` - Import statement sorting

2. **Type Checking**
   - `mypy` - Static type checker for Python type hints

3. **Security**
   - `bandit` - Security linter for Python code
   - `safety` - Dependency vulnerability scanner
   - `pip-audit` - Audit Python packages for known vulnerabilities

4. **Coverage**
   - `pytest-cov` - Coverage plugin for pytest
   - Target: 80%+ code coverage

---

## Directory Structure

```
gpt-tana-import/
├── src/
│   └── tana_import/
│       ├── __init__.py
│       ├── cli.py              # CLI entry point
│       ├── parser.py           # ChatGPT JSON parser
│       ├── converter.py        # Convert to Tana events
│       ├── api_client.py       # Tana API client
│       ├── config.py           # Configuration handling
│       └── models.py           # Data models
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Pytest fixtures
│   ├── test_parser.py
│   ├── test_converter.py
│   ├── test_api_client.py
│   ├── test_config.py
│   ├── test_cli.py
│   ├── integration/
│   │   ├── __init__.py
│   │   └── test_end_to_end.py
│   └── fixtures/
│       ├── sample_chatgpt_export.json
│       └── expected_tana_events.json
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI
├── pyproject.toml             # Project config (PEP 517/518)
├── setup.py                   # Package setup
├── requirements.txt           # Production dependencies
├── requirements-dev.txt       # Development dependencies
├── .flake8                    # Flake8 configuration
├── .pylintrc                  # Pylint configuration
├── mypy.ini                   # MyPy configuration
└── pytest.ini                 # Pytest configuration
```

---

## Implementation Phases

### Phase 1: Project Structure & Dependencies

**Tasks:**
1. Create Python package structure (`src/tana_import/`)
2. Set up `pyproject.toml` with project metadata
3. Create `requirements.txt` and `requirements-dev.txt`
4. Set up virtual environment best practices (document in README)

**Deliverables:**
- [ ] Package directory structure
- [ ] Dependency files
- [ ] Basic `setup.py` or `pyproject.toml` for package installation

---

### Phase 2: Linting & Formatting Configuration

**Tasks:**
1. Configure `black` with line length 100
2. Configure `flake8` to work with black
3. Configure `isort` with black-compatible settings
4. Configure `pylint` with reasonable rules
5. Add pre-commit hooks (optional but recommended)

**Configuration files:**
```toml
# pyproject.toml snippet
[tool.black]
line-length = 100
target-version = ['py39']

[tool.isort]
profile = "black"
line_length = 100

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "--cov=src/tana_import --cov-report=term-missing --cov-report=html"
```

**Deliverables:**
- [ ] `.flake8` configuration
- [ ] `.pylintrc` configuration
- [ ] `pyproject.toml` with black/isort config
- [ ] Documentation on running linters

---

### Phase 3: Testing Infrastructure

**Tasks:**
1. Set up pytest with basic configuration
2. Create test fixtures for ChatGPT export samples
3. Create test fixtures for expected Tana events
4. Set up pytest-cov for coverage reporting
5. Add test data samples (anonymized)

**Test Categories:**

1. **Unit Tests**
   - Parser: ChatGPT JSON parsing logic
   - Converter: Conversation → Tana events transformation
   - Config: Environment variable validation
   - API Client: Request formatting (with mocks)

2. **Integration Tests**
   - End-to-end: File input → Events output (no actual API calls)
   - Configuration validation flow
   - Error handling paths

3. **Fixtures & Mocks**
   - Sample ChatGPT export (1-2 conversations)
   - Mock HTTP responses for Tana API
   - Environment variable fixtures

**Coverage Goals:**
- Minimum: 80% overall coverage
- Critical paths (parser, converter): 90%+
- CLI/integration: 70%+

**Deliverables:**
- [ ] `pytest.ini` configuration
- [ ] Basic test structure with fixtures
- [ ] Sample test data files
- [ ] Coverage reporting setup

---

### Phase 4: Type Checking

**Tasks:**
1. Add type hints to all function signatures
2. Configure mypy with strict mode (or gradual adoption)
3. Add py.typed marker for package
4. Document type checking in development workflow

**Type Hints Strategy:**
- All public APIs: Full type hints
- Internal functions: Gradual adoption
- Use `typing` module for complex types (Dict, List, Optional, etc.)

**Deliverables:**
- [ ] `mypy.ini` configuration
- [ ] Type hints in code
- [ ] Documentation on type checking

---

### Phase 5: Security Scanning

**Tasks:**
1. Add `bandit` for code security analysis
2. Add `safety` for dependency vulnerability checks
3. Add `pip-audit` for package vulnerability scanning
4. Configure security checks to run in CI

**Security Rules:**
- No hardcoded secrets
- Secure HTTP requests (verify SSL)
- Input validation for file paths
- Safe JSON parsing

**Deliverables:**
- [ ] Bandit configuration (`.bandit`)
- [ ] Security scan scripts
- [ ] Documentation on security practices

---

### Phase 6: CI/CD Pipeline

**Tasks:**
1. Create GitHub Actions workflow
2. Run tests on multiple Python versions (3.9, 3.10, 3.11, 3.12)
3. Run linters (black, flake8, pylint, isort)
4. Run type checker (mypy)
5. Run security scanners (bandit, safety)
6. Generate and upload coverage reports
7. Add status badges to README

**GitHub Actions Workflow:**
```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11', '3.12']

    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      - name: Run black
        run: black --check src tests
      - name: Run isort
        run: isort --check-only src tests
      - name: Run flake8
        run: flake8 src tests
      - name: Run pylint
        run: pylint src
      - name: Run mypy
        run: mypy src
      - name: Run bandit
        run: bandit -r src
      - name: Run safety
        run: safety check
      - name: Run tests
        run: pytest --cov=src --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

**Deliverables:**
- [ ] `.github/workflows/ci.yml`
- [ ] CI pipeline running on PRs
- [ ] Status badges in README

---

### Phase 7: Documentation & Developer Experience

**Tasks:**
1. Add docstrings to all public functions (Google or NumPy style)
2. Create development setup guide
3. Document testing procedures
4. Add contributing guidelines
5. Create example/sample data

**Documentation Standards:**
- Docstrings: Google style
- README: Usage examples, installation, configuration
- CONTRIBUTING.md: How to run tests, linters, etc.

**Deliverables:**
- [ ] Comprehensive docstrings
- [ ] Development setup docs
- [ ] CONTRIBUTING.md
- [ ] Example data files

---

## Quality Metrics & Goals

### Code Coverage
- **Overall:** ≥80%
- **Critical modules (parser, converter):** ≥90%
- **CLI/integration:** ≥70%

### Code Quality
- **Linting:** Zero flake8/pylint errors on main branch
- **Formatting:** 100% black compliance
- **Type hints:** All public APIs typed
- **Security:** Zero high/critical bandit findings

### Test Suite
- **Performance:** Test suite completes in <30 seconds
- **Reliability:** Zero flaky tests
- **Maintainability:** Tests use fixtures/factories, avoid duplication

---

## Tooling Command Reference

Once implemented, developers will use these commands:

```bash
# Setup
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements-dev.txt

# Formatting
black src tests
isort src tests

# Linting
flake8 src tests
pylint src

# Type checking
mypy src

# Security
bandit -r src
safety check
pip-audit

# Testing
pytest                          # Run all tests
pytest tests/test_parser.py     # Run specific test file
pytest -v                       # Verbose output
pytest --cov=src                # With coverage

# Run all quality checks (create helper script)
./scripts/check-all.sh
```

---

## Dependencies

### Production Dependencies (requirements.txt)
```
requests>=2.31.0        # HTTP client for Tana API
python-dateutil>=2.8.2  # Date/time parsing
click>=8.1.0            # CLI framework (or argparse if simpler)
python-dotenv>=1.0.0    # Environment variable management
```

### Development Dependencies (requirements-dev.txt)
```
# Testing
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-mock>=3.11.0

# Linting & Formatting
black>=23.7.0
flake8>=6.1.0
pylint>=2.17.0
isort>=5.12.0

# Type Checking
mypy>=1.5.0
types-requests
types-python-dateutil

# Security
bandit>=1.7.5
safety>=2.3.0
pip-audit>=2.6.0

# Development tools
ipython>=8.14.0         # Better REPL
```

---

## Success Criteria

The quality tooling setup is complete when:

1. ✅ All linting tools are configured and passing
2. ✅ Test suite exists with ≥80% coverage
3. ✅ CI pipeline runs all checks on every PR
4. ✅ Type checking is enabled and passing
5. ✅ Security scans are configured
6. ✅ Documentation explains how to use all tools
7. ✅ Pre-commit hooks are available (optional but recommended)
8. ✅ Status badges are visible in README

---

## Timeline Estimate

- **Phase 1:** 2-3 hours (structure & dependencies)
- **Phase 2:** 2-3 hours (linting setup)
- **Phase 3:** 4-6 hours (testing infrastructure)
- **Phase 4:** 2-3 hours (type checking)
- **Phase 5:** 1-2 hours (security scanning)
- **Phase 6:** 2-3 hours (CI/CD)
- **Phase 7:** 2-3 hours (documentation)

**Total:** 15-23 hours

This can be done incrementally alongside feature development.

---

## Open Questions

1. Should we use `click` or stick with standard `argparse` for CLI? (Click is more feature-rich but adds dependency)
2. Should we add pre-commit hooks as mandatory or optional?
3. Do we want to publish this as a PyPI package eventually?
4. Should we add `tox` for testing multiple Python versions locally?
5. Coverage threshold: enforce in CI or just report?

---

## Notes

- This plan assumes Python as the implementation language; adjust if using Node.js/TypeScript
- All tools selected are industry-standard and well-maintained
- Configuration files can be consolidated into `pyproject.toml` where possible (PEP 621)
- Focus on developer experience: make it easy to run all checks with one command
