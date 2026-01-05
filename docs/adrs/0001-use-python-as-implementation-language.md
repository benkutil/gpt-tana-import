# ADR 0001: Use Python as Implementation Language

**Date:** 2026-01-01
**Status:** Accepted

## Context

We need to select an implementation language for the ChatGPT to Tana import CLI tool. The tool must:
- Parse JSON files (ChatGPT exports)
- Make HTTP requests to the Tana Input API
- Handle datetime/timezone conversions
- Provide a user-friendly CLI interface
- Be easy to deploy and run locally

The primary candidates considered were Python and Node.js/TypeScript.

## Decision

We will use **Python 3.9+** as the implementation language.

## Rationale

Python was chosen for the following reasons:

1. **Excellent JSON parsing capabilities**: Built-in `json` module handles complex nested structures well
2. **Rich CLI ecosystem**: Libraries like `click` and `argparse` make building robust CLIs straightforward
3. **Strong HTTP/API client libraries**: `requests` library is mature and widely used
4. **Superior datetime/timezone handling**: `datetime` and `dateutil` libraries provide robust timezone support
5. **Simpler deployment**: Single-file scripts or simple package distribution, no build/transpilation step required
6. **Great testing frameworks**: `pytest` is industry-standard with excellent plugin ecosystem
7. **Wide adoption**: Large community, extensive documentation, and many examples for similar tools

### Alternative Considered: Node.js/TypeScript

Node.js/TypeScript is also viable and has:
- Strong JSON handling
- Excellent HTTP clients (axios, fetch)
- Good CLI frameworks (commander, yargs)
- Strong typing with TypeScript

However, it was not chosen because:
- Requires build/transpilation step (TypeScript → JavaScript)
- More complex dependency management (node_modules)
- Datetime/timezone handling is more complex
- Additional overhead for simple CLI tool

## Consequences

### Positive
- Fast prototyping and development
- Easy for users to run (just requires Python installation)
- Strong ecosystem for all required functionality
- Excellent testing and quality tools available
- No build step simplifies deployment

### Negative
- Users must have Python 3.9+ installed
- Dynamic typing may allow some runtime errors (mitigated by using mypy for type checking)
- Slightly slower execution than compiled languages (not a concern for this use case)

### Neutral
- Team must follow Python best practices and style guides (PEP 8)
- Will use Python-specific tools (pytest, black, mypy, etc.)
