# Architecture Decision Records

This directory contains Architecture Decision Records (ADRs) for the ChatGPT to Tana import project.

An ADR is a document that captures an important architectural decision made along with its context and consequences.

## Format

Each ADR follows this structure:
- **Title**: Brief noun phrase
- **Date**: When the decision was made
- **Status**: Proposed, Accepted, Deprecated, Superseded
- **Context**: What is the issue that we're seeing that is motivating this decision?
- **Decision**: What is the change that we're proposing and/or doing?
- **Rationale**: Why this decision? What alternatives were considered?
- **Consequences**: What becomes easier or more difficult to do because of this change?

## Index

### Project Foundation

- [ADR 0001: Use Python as Implementation Language](0001-use-python-as-implementation-language.md) - 2026-01-01
- [ADR 0002: Comprehensive Quality Tooling Upfront](0002-comprehensive-quality-tooling-upfront.md) - 2026-01-01
- [ADR 0003: Use pytest + black + mypy Stack](0003-pytest-black-mypy-stack.md) - 2026-01-01
- [ADR 0004: Test Coverage Targets](0004-test-coverage-targets.md) - 2026-01-01

## Creating New ADRs

When making a significant architectural decision:

1. Copy the template from an existing ADR
2. Number it sequentially (0005, 0006, etc.)
3. Use a descriptive filename: `NNNN-brief-description.md`
4. Fill in all sections with context and rationale
5. Update this index
6. Commit the ADR with your changes

## Resources

- [ADR GitHub Organization](https://adr.github.io/)
- [Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) by Michael Nygard
