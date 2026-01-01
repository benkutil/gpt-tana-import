# ADR 0004: Test Coverage Targets

**Date:** 2026-01-01  
**Status:** Accepted

## Context

We need to establish test coverage targets for the project to ensure adequate testing while maintaining practical development velocity. Coverage targets should be high enough to catch bugs but not so stringent that they slow down development unnecessarily.

Different parts of the codebase have different criticality levels and may warrant different coverage requirements.

## Decision

We will establish the following test coverage targets:

- **Overall project coverage**: ≥80%
- **Critical modules** (parser, converter): ≥90%
- **CLI/integration modules**: ≥70%

Coverage will be measured using pytest-cov and reported in CI/CD pipeline.

## Rationale

### 80% Overall Coverage

This is a **balanced target** that:
- Catches most bugs and edge cases
- Allows some flexibility for less critical code
- Is achievable without excessive effort
- Is considered industry best practice for production code

**Why not higher?** 
- 100% coverage can lead to diminishing returns (testing trivial code)
- Some code (like configuration loading, CLI argument parsing) provides less value when tested extensively
- Allows focus on meaningful tests rather than coverage numbers

**Why not lower?**
- Below 80% leaves too many code paths untested
- Increases risk of undetected bugs
- Doesn't provide adequate safety net for refactoring

### 90%+ for Critical Modules

The **parser** and **converter** modules are the core business logic:
- Parse ChatGPT export JSON → structured data
- Convert structured data → Tana API events

These modules should have higher coverage because:
- They handle complex data transformations
- Bugs here directly impact data integrity
- They have well-defined inputs and outputs (easy to test)
- They are pure functions with minimal side effects

### 70%+ for CLI/Integration

CLI and integration code is harder to test and less critical:
- Often involves I/O operations
- Harder to mock external dependencies
- Many paths are error handling for edge cases
- Lower coverage is acceptable if critical paths are tested

## Consequences

### Positive
- **Clear expectations**: Developers know what coverage is required
- **Balanced approach**: High coverage for critical code, reasonable for the rest
- **Quality assurance**: 80%+ overall ensures good test coverage
- **Flexibility**: Different targets for different module types
- **Practical**: Targets are achievable without excessive effort

### Negative
- **Not 100%**: Some code paths will remain untested
- **Requires discipline**: Must maintain coverage as code evolves
- **May need adjustments**: Targets might need refinement as project matures

### Neutral
- **CI enforcement**: Coverage checks should run in CI (considered for future)
- **Reporting**: Coverage reports should be generated and visible
- **Excludes**: Some files may be excluded from coverage (e.g., `__init__.py`, test files themselves)

## Implementation

1. **Configure pytest-cov** to measure coverage
2. **Generate reports** in multiple formats (terminal, HTML)
3. **Monitor coverage** in CI/CD pipeline
4. **Optional**: Fail CI if coverage drops below thresholds (can be added in Phase 6)

## Success Criteria

- Coverage reports are generated on every test run
- Critical modules (parser, converter) maintain ≥90% coverage
- Overall project maintains ≥80% coverage
- Coverage trends are visible and monitored
