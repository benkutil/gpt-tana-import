# ChatGPT to Tana Import Tool - Requirements Specification

**Title:** Import ChatGPT exports into Tana via Input API (events) → Inbox

**Summary**  
Build a local CLI tool that reads ChatGPT export JSON and imports conversations into Tana using the Tana Input API (**events-style payload**). Imported conversations should be created under a configured **Inbox nodeId**, tagged `#ai-chat`, and structured into prompt/response trees with preserved ordering.

---

## Goals / Outcomes

- Convert ChatGPT export conversations into a Tana node hierarchy.
- Use **Tana Input API (events format)**.
- Place imported conversations under **Inbox** (not daily notes).
- Preserve prompt text and message ordering exactly as specified below.
- No dedupe behavior; reruns may create duplicates.

---

## Scope

### In-scope
- Local CLI (manual run).
- Parse one or more ChatGPT export JSON files.
- Produce and (optionally) send Tana Input API "events" payload.
- Create a conversation node per conversation.
- Build nested children:
  - Prompt nodes (user prompts)
  - Assistant/tool nodes split into parts and ordered

### Out-of-scope (for this ticket)
- Daily note placement by date
- Deduping/upsert
- Watching folders / background daemon
- Archiving/moving/deleting input JSON files after import

---

## Functional Requirements

### 1) CLI / Execution model
- Run as a **local CLI script** (manually executed).
- Input can be:
  - a file path, or
  - a directory of JSON files (implementation choice: recursive or not, but document it).

### 2) Required configuration
Must fail fast (exit non-zero, do not send anything) unless these are configured:

- `TANA_API_ENDPOINT` (string)
- `TANA_API_TOKEN` (string)
- `TANA_INBOX_NODE_ID` (string) **required**
- `#ai-chat` supertag must exist in Tana (how it's referenced in API depends on schema; see TBD).

### 3) Placement
- All imported conversation root nodes must be created as children of **Inbox** (`TANA_INBOX_NODE_ID`).

### 4) Conversation node
For each ChatGPT conversation:

- Create a conversation root node under Inbox with title:  
  `ChatGPT conversation - YYYY-MM-DD HH:MM`  
  derived from conversation `create_time` (timezone handling: use system local time unless a CLI `--timezone` override is implemented).
- Apply supertag: `#ai-chat`.

### 5) Prompt nodes
Under each conversation node:
- Create one child node per **user prompt**.
- The prompt node **text is the full prompt verbatim** (including newlines/markdown).

### 6) Assistant/tool nodes (split into parts)
Under each prompt node:
- Create multiple child nodes representing the assistant/tool "parts"
- Split into parts so that assistant responses and tool call/outputs are **not merged into one node**
- Preserve original export order exactly, e.g.:
  - assistant message 1
  - tool call
  - tool output
  - assistant message 2
- Tool calls/outputs should be included as **plain text nodes** (no special prefixes like "Tool call:").

### 7) Ordering
- Preserve the chronological order as it appears in the export.
- If ChatGPT export is a message tree, linearize using the "active/current" path if available; otherwise sort by message timestamps.

### 8) No dedupe
- Do **not** attempt deduplication.
- Rerunning the importer can create duplicates.

### 9) Input files handling
- Leave the JSON files where they are after import (no move/delete/archive).

---

## Non-Functional Requirements

- **Safety:** Fail fast if `TANA_INBOX_NODE_ID` is not available (to avoid importing into an unintended location).
- **Logging:** Print counts (files scanned, conversations found, nodes/events generated).
- **Determinism:** Stable ordering of generated events (e.g., sort conversations by `create_time` ascending).

---

## Deliverables

1) CLI script
2) Documentation/README covering:
   - how to provide `TANA_API_ENDPOINT`, `TANA_API_TOKEN`, `TANA_INBOX_NODE_ID`
   - how to run against a file or directory
   - what node structure will be created
3) Example generated "events" JSON payload (saved to file or printed) for inspection.

---

## Acceptance Criteria

- Given a ChatGPT export JSON containing ≥1 conversation, running the CLI with valid Tana config:
  - creates one conversation node per conversation under Inbox
  - conversation node is titled `ChatGPT conversation - YYYY-MM-DD HH:MM`
  - conversation node is tagged `#ai-chat`
  - for each user prompt:
    - a prompt node is created with full prompt text verbatim
    - assistant/tool nodes are created underneath, split into parts and in correct order
    - tool call/outputs appear as plain text nodes
- With `TANA_INBOX_NODE_ID` missing:
  - CLI exits non-zero
  - prints a clear message explaining how to supply the Inbox node id
  - does not send any requests to Tana

---

## TBD / Open Questions

1) **Tana Input API (events) exact schema** being used:
   - exact event type names
   - how to specify parent node
   - how to specify node text
   - how to apply supertag `#ai-chat` (by name vs nodeId vs tag list)
2) Exact ChatGPT export JSON schema details in your files (fields for:
   - conversation list
   - message tree structure
   - tool call/output representation)
