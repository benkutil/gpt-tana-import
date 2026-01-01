# Agent Workflow and Guidelines

## Task Tracking

🛑 Don't continue working until you can find an associated issue in the repository. If you can't find one, create one that captures the work being done and acceptance criteria for the work.

## Test-Driven Development

Start new features and refactors by writing failing tests, then implement the minimal code needed to pass, and finally refactor while keeping the suite green. Treat red/green/refactor as non-negotiable guardrails so quality and design evolve together.

## Architectural Decision Records

Capture architecture and process choices in lightweight ADRs stored under docs/adrs/. Log context, decision, and consequences so future contributors understand why we did what we did.

## Trunk-Based Development with Atomic Commits

Integrate to the main branch frequently via small, self-contained commits that each keep the build passing. Use short-lived branches when necessary, but merge back quickly to keep integration friction low.

Agents must commit atomically as they work. After completing each logical unit of work:

- Stage the relevant changes
- Commit with a conventional commit message
- Continue to the next task

Do not batch multiple unrelated changes into a single commit. Each commit should be independently reviewable and revertable.

When starting a new task or feature:

- Create a GitHub issue describing the work
- Create a draft PR linked to the issue
- Work in small, atomic commits
- Mark PR ready for review when complete

## Commit Messages & Versioning

Use consistent, structured commit messages following:

- Conventional Commits
- Semantic Commit Messages

Examples:

- `feat: add user authentication flow`
- `fix: resolve null pointer in payment module`
- `docs: update API reference for v2 endpoints`
- `refactor: extract validation logic into shared utility`
- `test: add integration tests for checkout process`

## Compounding Engineering Philosophy

Each unit of engineering work should make subsequent units of work easier—not harder.

When working on this repository, follow the compounding engineering approach:

- **Brainstorm** – Explore the problem space and potential solutions
- **Plan** – Define scope, acceptance criteria, and approach
- **Implement** – Build incrementally with TDD and atomic commits
- **Review** – Validate against requirements and coding standards
- **Improve** – Assess what improvements could be made to agents, commands, or this AGENTS.md file

Every change should leave the codebase better than you found it.

## Agent Workflow Requirements

### Pre-Work Checklist

Before making any code or documentation changes, complete these steps in order:

1. **Create a feature branch from main**

```bash
git checkout main && git pull origin main
git checkout -b <descriptive-branch-name>
```

2. **Create a GitHub issue describing the work**

- Use gh issue create with a clear title and description
- Document the problem and proposed solution

3. **Create a draft PR linked to the issue**

- Reference the issue number in the PR body
- Use --draft flag to indicate work in progress

4. **Start a session log in docs/logs/**

- Format: docs/logs/YYYY-MM-DD<branch-name>.md
- Include objective and link to the issue/PR

Only then proceed with implementation. This ensures all work is tracked and reviewable from the start.

## Session Logging

When starting a new feature or branch:

1. **Create the log file first before any other work**

- Format: docs/logs/YYYY-MM-DD<branch-name>.md
- Include: Objective, Related (issue/PR links), empty Work Completed section

2. **Update incrementally after each commit:**

- Add entry to Work Completed with timestamp
- Document your reasoning: why this approach? what alternatives were considered?
- Capture what you learned or discovered during implementation
- Note any assumptions made or constraints encountered
- Include the commit message for traceability

3. **Capture decisions and lessons as they happen**

- Don't wait until session end to record insights
- Document "why" not just "what"—future contributors need context
- Record sources consulted (docs, existing code, external references)

Logs should contain:

- **Objective** – What the session aims to accomplish
- **Related** – Links to issues and PRs
- **Work completed** – Summary of each task with timestamps, reasoning, and commit references
- **Decisions made** – Choices, alternatives considered, and rationale
- **Lessons learned** – What would you do differently? What should be improved?

## Proactive Self-Improvement

At the end of each session (or when prompted), agents should:

- Review the conversation for lessons learned
- Identify gaps or friction in the current workflows
- Propose or implement improvements to AGENTS.md, agents, commands, or skills

This ensures the repository continuously evolves based on real usage.

## Landing the Plane (Session Completion)

When ending a work session, you MUST complete ALL steps below. Work is NOT complete until git push succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates (if code changed)** - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:

```bash
git pull --rebase
git push
git status  # MUST show "up to date with origin"
```

5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**

- Work is NOT complete until git push succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds
