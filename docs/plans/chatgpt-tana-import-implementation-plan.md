# ChatGPT to Tana Import Tool - Implementation Plan

**Created:** 2026-01-02  
**Status:** Planned  
**Purpose:** Implement the ChatGPT to Tana import CLI tool per requirements in `docs/spec/requirements.md`

---

## Overview

This plan outlines the implementation of a local CLI tool that converts ChatGPT export JSON files into Tana nodes via the Tana Input API (events format). The tool will import conversations under a configured Inbox node with proper structure and tagging.

## Goals

1. **CLI Tool**: Build a command-line interface for importing ChatGPT exports
2. **JSON Parsing**: Parse ChatGPT export JSON files accurately
3. **API Integration**: Generate Tana Input API events payloads
4. **Node Structure**: Create properly structured conversation hierarchies
5. **Configuration**: Handle required environment variables with fail-fast validation

---

## Implementation Phases

### Phase 1: Project Setup & Core Structure

**Objective:** Set up the basic project structure and dependencies

**Tasks:**
1. Create core module structure:
   - `src/tana_import/__init__.py`
   - `src/tana_import/cli.py` - CLI entry point
   - `src/tana_import/config.py` - Configuration management
   - `src/tana_import/models.py` - Data models

2. Set up dependencies:
   - `click` or `argparse` for CLI framework
   - `python-dotenv` for environment variables
   - `requests` for HTTP client (if sending to API)
   - `python-dateutil` for date/time parsing

3. Create basic CLI skeleton with:
   - File/directory input argument
   - Help text and usage documentation
   - Version information

**Deliverables:**
- [ ] Basic package structure created
- [ ] CLI entry point with argument parsing
- [ ] Configuration loader with validation
- [ ] Basic help/usage documentation

**Testing:**
- [ ] Test CLI help output
- [ ] Test configuration validation (fail-fast on missing vars)

---

### Phase 2: Configuration Management

**Objective:** Implement robust configuration handling with fail-fast validation

**Tasks:**
1. Implement `config.py`:
   - Load from environment variables
   - Validate required fields:
     - `TANA_API_ENDPOINT`
     - `TANA_API_TOKEN`
     - `TANA_INBOX_NODE_ID`
   - Optional: `--timezone` CLI flag override

2. Add clear error messages for missing configuration

3. Document configuration in README:
   - How to set environment variables
   - Example `.env` file
   - Security notes about API token

**Deliverables:**
- [ ] Configuration class with validation
- [ ] Clear error messages for missing config
- [ ] Documentation on configuration setup
- [ ] Example `.env.example` file

**Testing:**
- [ ] Test with all required vars present
- [ ] Test with each required var missing (fail-fast)
- [ ] Test configuration loading from .env file

---

### Phase 3: ChatGPT Export Parser

**Objective:** Parse ChatGPT export JSON files into internal data structures

**Tasks:**
1. Create `parser.py`:
   - Load and validate JSON file structure
   - Extract conversations from export
   - Parse message tree/list structure
   - Handle conversation metadata (create_time, title, etc.)

2. Create data models in `models.py`:
   - `Conversation` model
   - `Message` model (user prompts, assistant responses, tool calls/outputs)
   - Message ordering/linearization logic

3. Handle edge cases:
   - Empty conversations
   - Malformed JSON
   - Message tree vs linear message list
   - Missing timestamps

4. Linearize message trees using active/current path if available

**Deliverables:**
- [ ] Parser module that extracts conversations
- [ ] Data models for conversations and messages
- [ ] Message ordering/linearization logic
- [ ] Error handling for malformed JSON

**Testing:**
- [ ] Test with sample ChatGPT export JSON
- [ ] Test message ordering preservation
- [ ] Test with message trees (if applicable)
- [ ] Test error handling for invalid JSON

---

### Phase 4: Tana Events Generator

**Objective:** Convert parsed conversations into Tana Input API events format

**Tasks:**
1. Create `converter.py`:
   - Generate conversation root node events
   - Generate prompt node events (children of conversation)
   - Generate assistant/tool part node events (children of prompts)
   - Apply `#ai-chat` supertag to conversation nodes

2. Implement node structure:
   - Conversation node: "ChatGPT conversation - YYYY-MM-DD HH:MM"
   - Prompt nodes: Full prompt text verbatim
   - Assistant/tool parts: Split into separate nodes, preserve order

3. Handle timezone conversion:
   - Convert `create_time` to local time
   - Support optional `--timezone` override
   - Format: YYYY-MM-DD HH:MM

4. Research Tana Input API events schema:
   - Event type names
   - Parent node specification
   - Node text specification
   - Supertag application (by name vs nodeId)

**Deliverables:**
- [ ] Converter that generates Tana events JSON
- [ ] Proper node hierarchy (conversation → prompts → parts)
- [ ] Supertag application logic
- [ ] Timezone handling
- [ ] Example generated events JSON for inspection

**Testing:**
- [ ] Test conversation node generation
- [ ] Test prompt node generation
- [ ] Test assistant/tool parts splitting and ordering
- [ ] Test supertag application
- [ ] Validate generated events JSON structure

---

### Phase 5: Tana API Client

**Objective:** Send generated events to Tana Input API

**Tasks:**
1. Create `api_client.py`:
   - HTTP client for Tana Input API
   - Authentication with API token
   - POST events payload to endpoint
   - Error handling and retry logic

2. Implement dry-run mode:
   - `--dry-run` flag to generate events without sending
   - Save events JSON to file for inspection

3. Add request/response logging:
   - Log API calls (excluding sensitive data)
   - Log response status and errors
   - Count nodes/events sent

**Deliverables:**
- [ ] API client module
- [ ] Dry-run mode implementation
- [ ] Request/response logging
- [ ] Error handling for API failures

**Testing:**
- [ ] Test with mock API responses
- [ ] Test authentication headers
- [ ] Test dry-run mode (no actual API calls)
- [ ] Test error handling (network errors, API errors)

---

### Phase 6: CLI Integration & File Handling

**Objective:** Wire up all components in the CLI and handle file/directory input

**Tasks:**
1. Update `cli.py` to orchestrate:
   - Load configuration
   - Find and read JSON file(s)
   - Parse conversations
   - Generate events
   - Send to API (or save if dry-run)

2. Implement file/directory handling:
   - Accept single file path
   - Accept directory path (scan for .json files)
   - Document recursive vs non-recursive behavior

3. Add logging and progress output:
   - Print files scanned
   - Print conversations found
   - Print nodes/events generated
   - Print success/failure status

4. Implement stable ordering:
   - Sort conversations by `create_time` ascending
   - Ensure deterministic output

**Deliverables:**
- [ ] Complete CLI workflow
- [ ] File/directory scanning logic
- [ ] Progress logging
- [ ] Deterministic event ordering

**Testing:**
- [ ] Test with single file
- [ ] Test with directory of multiple files
- [ ] Test with empty directory
- [ ] Test with non-existent file/directory
- [ ] Test logging output

---

### Phase 7: Documentation & Examples

**Objective:** Create comprehensive documentation and usage examples

**Tasks:**
1. Update README.md:
   - Installation instructions
   - Configuration setup (environment variables)
   - Usage examples (file and directory input)
   - Node structure explanation
   - Troubleshooting guide

2. Create example files:
   - Example ChatGPT export JSON (anonymized)
   - Example generated Tana events JSON
   - Example `.env` file

3. Add inline documentation:
   - Docstrings for all public functions (Google style)
   - Code comments for complex logic
   - Type hints for function signatures

4. Create usage guide:
   - Step-by-step walkthrough
   - Common error messages and solutions
   - FAQ section

**Deliverables:**
- [ ] Comprehensive README with examples
- [ ] Example input/output files
- [ ] `.env.example` file
- [ ] Docstrings and type hints
- [ ] Usage guide/walkthrough

**Testing:**
- [ ] Verify all examples work
- [ ] Test installation instructions
- [ ] Validate configuration examples

---

## Technical Specifications

### Directory Structure

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
│   ├── conftest.py
│   ├── test_parser.py
│   ├── test_converter.py
│   ├── test_api_client.py
│   ├── test_config.py
│   ├── test_cli.py
│   └── fixtures/
│       ├── sample_chatgpt_export.json
│       └── expected_tana_events.json
├── examples/
│   ├── sample_export.json
│   ├── generated_events.json
│   └── .env.example
├── README.md
├── pyproject.toml
├── requirements.txt
└── requirements-dev.txt
```

### Data Models

```python
# models.py

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class Message:
    """Represents a single message in a conversation"""
    role: str  # 'user', 'assistant', 'tool'
    content: str
    timestamp: datetime
    message_type: str  # 'prompt', 'response', 'tool_call', 'tool_output'
    
@dataclass
class Conversation:
    """Represents a ChatGPT conversation"""
    id: str
    title: Optional[str]
    create_time: datetime
    messages: List[Message]
    
@dataclass
class TanaNode:
    """Represents a Tana node to be created"""
    text: str
    parent_id: Optional[str]
    supertags: List[str]
    children: List['TanaNode']
```

### Configuration Variables

Required environment variables:
- `TANA_API_ENDPOINT` - Tana API endpoint URL
- `TANA_API_TOKEN` - Authentication token for Tana API
- `TANA_INBOX_NODE_ID` - Node ID of the Inbox where conversations will be placed

### CLI Usage

```bash
# Import single file
python -m tana_import path/to/chatgpt_export.json

# Import directory of JSON files
python -m tana_import path/to/exports/

# Dry run (generate events but don't send)
python -m tana_import --dry-run path/to/export.json

# Save events to file
python -m tana_import --output events.json path/to/export.json

# Specify timezone
python -m tana_import --timezone "America/New_York" path/to/export.json

# Show help
python -m tana_import --help
```

---

## Node Structure Example

```
Inbox (TANA_INBOX_NODE_ID)
├── ChatGPT conversation - 2024-01-15 14:30 #ai-chat
│   ├── [User prompt 1 text verbatim]
│   │   ├── [Assistant response part 1]
│   │   ├── [Tool call]
│   │   ├── [Tool output]
│   │   └── [Assistant response part 2]
│   ├── [User prompt 2 text verbatim]
│   │   └── [Assistant response]
│   └── ...
└── ChatGPT conversation - 2024-01-16 09:15 #ai-chat
    └── ...
```

---

## Dependencies

### Production Dependencies (requirements.txt)

```
click>=8.1.0              # CLI framework
python-dotenv>=1.0.0      # Environment variables
requests>=2.31.0          # HTTP client
python-dateutil>=2.8.2    # Date/time parsing
```

### Development Dependencies (requirements-dev.txt)

```
# Testing (from quality-tooling-plan.md)
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
```

---

## Acceptance Criteria

The implementation is complete when:

1. ✅ CLI accepts file or directory path as input
2. ✅ Configuration validation fails fast with clear messages
3. ✅ ChatGPT JSON files are parsed correctly
4. ✅ Conversations are converted to Tana events format
5. ✅ Node structure matches specification:
   - Conversation node titled "ChatGPT conversation - YYYY-MM-DD HH:MM"
   - Conversation tagged with `#ai-chat`
   - Prompt nodes contain full prompt text verbatim
   - Assistant/tool nodes split into parts in correct order
6. ✅ Events are sent to Tana API successfully (or saved in dry-run)
7. ✅ Logging shows counts (files, conversations, nodes)
8. ✅ Documentation explains setup and usage
9. ✅ Example files demonstrate input/output
10. ✅ Tests cover core functionality (≥80% coverage per quality plan)

---

## Risk Mitigation

### Known Risks

1. **Tana Input API schema unknown**
   - **Mitigation:** Research API docs, test with sample payloads, or ask for clarification
   - **Fallback:** Generate events JSON for manual inspection/testing

2. **ChatGPT export format variations**
   - **Mitigation:** Handle multiple format versions, add validation
   - **Fallback:** Document supported format versions

3. **Message tree complexity**
   - **Mitigation:** Implement robust linearization logic
   - **Fallback:** Use simple timestamp-based ordering if tree path unavailable

4. **API rate limiting**
   - **Mitigation:** Add request throttling, batch processing
   - **Fallback:** Document rate limits, add retry logic

---

## Timeline Estimate

- **Phase 1:** 2-3 hours (project setup)
- **Phase 2:** 1-2 hours (configuration)
- **Phase 3:** 3-4 hours (parser)
- **Phase 4:** 3-4 hours (events generator)
- **Phase 5:** 2-3 hours (API client)
- **Phase 6:** 2-3 hours (CLI integration)
- **Phase 7:** 2-3 hours (documentation)

**Total:** 15-22 hours

Can be implemented incrementally with TDD approach.

---

## Open Questions

1. **Tana Input API events schema:**
   - What are the exact event type names?
   - How to specify parent node in events?
   - How to apply supertag `#ai-chat` (by name, nodeId, or tag list)?

2. **ChatGPT export format:**
   - Is it a message tree or linear list?
   - How are tool calls/outputs represented?
   - Are there format variations across export versions?

3. **Implementation choices:**
   - Use `click` or `argparse` for CLI?
   - Recursive directory scanning or single-level only?
   - Should tool calls/outputs have prefixes or be plain text?

4. **Error handling:**
   - Should partial imports be supported (some conversations succeed, some fail)?
   - How to handle duplicate detection (out of scope but may need consideration)?

---

## References

- Requirements: `docs/spec/requirements.md`
- Quality Tooling Plan: `docs/plans/quality-tooling-plan.md`
- Tana Input API Documentation: [TBD - needs link]
- ChatGPT Export Format: [TBD - needs sample or documentation]
