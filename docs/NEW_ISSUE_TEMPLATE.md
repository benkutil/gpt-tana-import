# GitHub Issue Template

**Note:** This file contains the content for a GitHub issue to be created. 
Use this content to create a new issue in the repository.

---

**Title:** Implement ChatGPT to Tana Import CLI Tool

**Labels:** `feature`, `enhancement`, `documentation`

---

## Summary

Build a local CLI tool that reads ChatGPT export JSON files and imports conversations into Tana using the Tana Input API (events format). Imported conversations should be created under a configured Inbox node, tagged `#ai-chat`, and structured into prompt/response trees with preserved ordering.

## Requirements

Full requirements specification: [docs/spec/requirements.md](../spec/requirements.md)

### Key Features

- **CLI Tool**: Accept file or directory path as input
- **Configuration**: Validate required environment variables (fail-fast):
  - `TANA_API_ENDPOINT`
  - `TANA_API_TOKEN`
  - `TANA_INBOX_NODE_ID`
- **Parsing**: Parse ChatGPT export JSON files
- **Conversion**: Generate Tana Input API events payloads
- **Structure**: Create conversation hierarchy:
  - Conversation node: "ChatGPT conversation - YYYY-MM-DD HH:MM" (tagged `#ai-chat`)
  - Prompt nodes: Full user prompt text verbatim
  - Assistant/tool nodes: Split into parts, preserve order
- **Placement**: All conversations created as children of Inbox node
- **Logging**: Print counts (files scanned, conversations found, nodes generated)

### Out of Scope

- Daily note placement by date
- Deduplication/upsert logic
- Watching folders / background daemon
- Archiving/moving/deleting input JSON files after import

## Implementation Plan

Full implementation plan: [docs/plans/chatgpt-tana-import-implementation-plan.md](../plans/chatgpt-tana-import-implementation-plan.md)

### Phases

1. **Phase 1: Project Setup & Core Structure** (2-3 hours)
   - Create module structure: `cli.py`, `config.py`, `models.py`
   - Set up dependencies
   - Basic CLI skeleton

2. **Phase 2: Configuration Management** (1-2 hours)
   - Environment variable loading and validation
   - Fail-fast on missing config
   - Documentation and `.env.example`

3. **Phase 3: ChatGPT Export Parser** (3-4 hours)
   - Parse JSON files
   - Extract conversations and messages
   - Handle message ordering/linearization

4. **Phase 4: Tana Events Generator** (3-4 hours)
   - Convert conversations to Tana events format
   - Generate node hierarchy
   - Apply supertags

5. **Phase 5: Tana API Client** (2-3 hours)
   - HTTP client for Tana Input API
   - Dry-run mode
   - Error handling

6. **Phase 6: CLI Integration & File Handling** (2-3 hours)
   - Wire up all components
   - File/directory scanning
   - Progress logging

7. **Phase 7: Documentation & Examples** (2-3 hours)
   - README with usage examples
   - Example files
   - Docstrings and type hints

**Estimated Total:** 15-22 hours

## Acceptance Criteria

- [ ] CLI accepts file or directory path as input
- [ ] Configuration validation fails fast with clear error messages
- [ ] ChatGPT JSON files are parsed correctly
- [ ] Conversations are converted to Tana events format
- [ ] Node structure matches specification
- [ ] Conversation nodes titled "ChatGPT conversation - YYYY-MM-DD HH:MM"
- [ ] Conversation nodes tagged with `#ai-chat`
- [ ] Prompt nodes contain full prompt text verbatim
- [ ] Assistant/tool nodes split into parts in correct order
- [ ] All nodes created under configured Inbox node
- [ ] Events sent to Tana API successfully (or saved in dry-run mode)
- [ ] Logging shows counts (files, conversations, nodes)
- [ ] Documentation explains setup and usage
- [ ] Example files demonstrate input/output
- [ ] Tests cover core functionality (≥80% coverage per quality tooling plan)

## Technical Stack

- **Language:** Python 3.9+
- **CLI Framework:** click or argparse
- **HTTP Client:** requests
- **Environment Variables:** python-dotenv
- **Date/Time:** python-dateutil

## Open Questions

1. What is the exact Tana Input API events schema?
   - Event type names
   - Parent node specification format
   - Supertag application method (by name vs nodeId)

2. What is the ChatGPT export JSON format?
   - Message tree vs linear list structure
   - Tool call/output representation
   - Format variations across export versions

## Related Documents

- Requirements: [docs/spec/requirements.md](../spec/requirements.md)
- Implementation Plan: [docs/plans/chatgpt-tana-import-implementation-plan.md](../plans/chatgpt-tana-import-implementation-plan.md)
- Quality Tooling Plan: [docs/plans/quality-tooling-plan.md](../plans/quality-tooling-plan.md)

---

## How to Create This Issue

Use the GitHub CLI or web interface:

```bash
# Using GitHub CLI (if you have permissions)
gh issue create --title "Implement ChatGPT to Tana Import CLI Tool" \
  --body-file docs/NEW_ISSUE_TEMPLATE.md \
  --label "feature,enhancement,documentation"
```

Or copy this content and create a new issue via the GitHub web interface.
