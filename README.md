# ChatGPT to Tana Import Tool

[![CI](https://github.com/benkutil/gpt-tana-import/actions/workflows/ci.yml/badge.svg)](https://github.com/benkutil/gpt-tana-import/actions/workflows/ci.yml)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A local CLI tool that imports ChatGPT conversation exports into Tana using the Tana Input API.

## Overview

This tool converts ChatGPT export JSON files into structured conversations in Tana. It preserves the full conversation history including prompts, assistant responses, and tool interactions, organizing them into a clean hierarchical structure under your Tana Inbox.

## Features

- **Simple CLI interface** - Run manually against single files or directories
- **Preserves conversation structure** - Maintains exact prompt/response ordering
- **Tool interaction support** - Captures tool calls and outputs as separate nodes
- **Inbox integration** - Creates conversations under your configured Inbox node
- **Automatic tagging** - Tags all conversations with `#ai-chat` for easy filtering
- **Safe imports** - Fails fast if configuration is missing to prevent accidental misplacement

## How It Works

The tool reads ChatGPT export JSON files and transforms each conversation into a Tana node hierarchy:

```
📥 Inbox
  └── 💬 ChatGPT conversation - 2026-01-01 14:30 #ai-chat
       ├── 📝 User prompt 1
       │    ├── 🤖 Assistant response part 1
       │    ├── 🔧 Tool call
       │    ├── ⚙️ Tool output
       │    └── 🤖 Assistant response part 2
       └── 📝 User prompt 2
            └── 🤖 Assistant response
```

Each conversation becomes a root node under your Inbox with:
- Title: `ChatGPT conversation - YYYY-MM-DD HH:MM` (from conversation creation time)
- Tag: `#ai-chat`
- Children: User prompts with nested assistant/tool responses

## Installation

### For Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for complete development setup instructions.

### For Production Use

_Coming soon - PyPI package installation will be available once the core functionality is implemented_

## Configuration

The tool requires three environment variables to be set:

```bash
export TANA_API_ENDPOINT="https://europe-west1-tagr-prod.cloudfunctions.net/addToNodeV2"
export TANA_API_TOKEN="your-tana-api-token"
export TANA_INBOX_NODE_ID="your-inbox-node-id"
```

### Getting Your Configuration Values

1. **TANA_API_ENDPOINT**: Use the endpoint shown above (current as of 2026)
2. **TANA_API_TOKEN**: Generate from Tana Settings → API tokens
3. **TANA_INBOX_NODE_ID**: 
   - Navigate to your Inbox in Tana
   - Copy the node ID from the URL or node context menu

⚠️ **Important**: If any of these values are missing, the tool will exit with an error message and will NOT send any data to Tana.

## Usage

_Coming soon - usage examples will be added once implementation is complete_

### Basic Examples

```bash
# Import a single ChatGPT export file
./import-chatgpt path/to/conversations.json

# Import all JSON files in a directory
./import-chatgpt path/to/exports/

# Dry run - generate events without sending to Tana
./import-chatgpt --dry-run conversations.json
```

## Node Structure

### Conversation Node
- **Title**: `ChatGPT conversation - YYYY-MM-DD HH:MM`
- **Tag**: `#ai-chat`
- **Parent**: Your Inbox node

### Prompt Nodes
- **Content**: Full user prompt text (verbatim, preserving newlines/markdown)
- **Parent**: Conversation node

### Assistant/Tool Nodes
- **Content**: Assistant responses and tool interactions
- **Parent**: Prompt node
- **Ordering**: Preserved exactly as in the ChatGPT export
- **Format**: Plain text (no prefixes like "Tool call:")

## Important Notes

### No Deduplication
The tool does **not** check for existing conversations. Running the import multiple times will create duplicate conversations in Tana.

### File Handling
Input JSON files are **not** moved, archived, or deleted after import. They remain in their original location.

### Timezone
Conversation timestamps use your system's local timezone unless overridden with `--timezone` flag.

## Development

### Running Quality Checks

The project uses comprehensive quality tooling to ensure code quality:

```bash
# Run all checks at once
make check
# or
./scripts/check-all.sh

# Run tests
make test

# Auto-format code
make format

# Or run individual checks:
black --check src tests    # Check code formatting
isort --check-only src tests  # Check import sorting
flake8 src tests          # Linting
pylint src                # Advanced linting
mypy src                  # Type checking
bandit -r src -c .bandit  # Security scanning
pytest                    # Run tests with coverage
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed development guidelines and [AGENTS.md](AGENTS.md) for development workflows.

## Documentation

- [Requirements Specification](docs/spec/requirements.md) - Complete functional and non-functional requirements
- [Quality Tooling Plan](docs/plans/) - Planned testing and code quality infrastructure
- [Architecture Decision Records](docs/adrs/) - Design decisions and rationale
- [Session Logs](docs/logs/) - Development session records

## Roadmap

### Phase 1: Core Functionality (Current)
- [ ] Basic CLI implementation
- [ ] ChatGPT export JSON parsing
- [ ] Tana Input API integration (events format)
- [ ] Conversation structure creation
- [ ] Configuration validation

### Phase 2: Quality & Testing ✅
- [x] Unit test suite (98% coverage)
- [x] Integration tests
- [x] Linting and code quality tools
- [x] CI/CD pipeline

### Future Enhancements (Out of Scope)
- Daily note placement by conversation date
- Deduplication/upsert logic
- Background daemon/folder watching
- Archive/cleanup of processed files

## Contributing

This is a personal utility tool. If you'd like to contribute improvements or report issues, please follow the development guidelines in AGENTS.md.

## License

_To be determined_

## Acknowledgments

Built to bridge ChatGPT and Tana, making conversation history portable and searchable within your personal knowledge management system.