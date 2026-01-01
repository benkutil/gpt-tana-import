# ADR 0003: Use pytest + black + mypy Stack for Quality Tooling

**Date:** 2026-01-01  
**Status:** Accepted

## Context

Having decided to implement comprehensive quality tooling (ADR 0002), we need to select specific tools for:
- Testing framework
- Code formatting
- Type checking
- Linting

The Python ecosystem offers many options for each category. We need a cohesive stack that works well together and is well-maintained.

## Decision

We will use the following quality tooling stack:

- **Testing**: pytest (with pytest-cov for coverage, pytest-mock for mocking)
- **Formatting**: black (with isort for import sorting)
- **Type Checking**: mypy
- **Linting**: flake8 and pylint
- **Security**: bandit and safety

## Rationale

This combination is the **industry standard** for professional Python projects.

### pytest
- Most popular Python testing framework
- Rich plugin ecosystem (over 1000 plugins)
- Excellent fixtures and parametrization support
- Clean, readable test syntax
- Great integration with coverage tools
- Active maintenance and community support

**Alternatives considered**: unittest (built-in but more verbose), nose2 (less popular)

### black
- "Uncompromising" code formatter - minimal configuration needed
- Eliminates formatting debates
- Deterministic output ensures consistency
- Wide adoption in Python community
- Integrates well with other tools

**Alternatives considered**: autopep8 (less opinionated), yapf (more configurable but requires more decisions)

### mypy
- Official type checker for Python type hints
- Best-in-class static type analysis
- Good error messages
- Gradual typing support (can adopt incrementally)
- Actively developed by Python core team

**Alternatives considered**: pytype (Google's checker), pyre (Facebook's checker) - both less widely adopted

### flake8 + pylint
- **flake8**: Fast, checks PEP 8 compliance, good for catching common issues
- **pylint**: More comprehensive, catches logic errors and code smells
- Together they provide complete linting coverage

**Alternatives considered**: Using only one (but combination catches more issues)

### bandit + safety
- **bandit**: Security linter for Python code (catches common security anti-patterns)
- **safety**: Checks dependencies for known vulnerabilities
- Both are lightweight and integrate well into CI

## Consequences

### Positive
- **Industry-standard tools**: Easy to find documentation, examples, and help
- **Well-maintained**: All tools are actively developed with strong communities
- **Excellent ecosystem**: Tools work well together with minimal configuration conflicts
- **Complete quality coverage**: Testing, formatting, type safety, linting, and security all addressed
- **CI/CD friendly**: All tools have good CLI interfaces and CI integration

### Negative
- **Multiple tools to learn**: New contributors need to understand several tools
- **Some redundancy**: flake8 and pylint have overlapping checks
- **Configuration required**: Each tool needs setup (though minimal for black)

### Neutral
- **Opinionated**: black is uncompromising, which is both a feature and a constraint
- **Type hints required**: mypy effectiveness depends on adding type hints
- **Coverage targets**: Need to establish and maintain coverage goals (80% overall, 90% for critical modules)

## Configuration

All tools will be configured via:
- `pyproject.toml` (for black, isort, pytest)
- `.flake8` (flake8-specific)
- `.pylintrc` (pylint-specific)
- `mypy.ini` (mypy-specific)

Configuration will prioritize:
- black compatibility (100-character line length)
- Reasonable linting rules (avoid overly strict checks)
- Strict type checking where practical
