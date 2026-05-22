# Project Instructions (Gemini CLI)

These instructions govern all Gemini CLI operations in this workspace. They are derived from the previous agent-system and ECC plugin rules.

## Core Mandates: Efficiency & Waste Reduction

To maintain maximum performance and cost-efficiency, strictly adhere to these operational patterns:

### 1. Complexity Classification
Before any tool call, classify the task complexity and respect the associated tool-call budget:
- **Trivial (≤5 calls):** Named target, obvious intent, single change. *Workflow: Direct Read (targeted) → Edit.*
- **Moderate (≤20 calls):** Bounded scope (1-3 files), clear intent, needs verification. *Workflow: Scout → Builder → Reviewer.*
- **Complex (≤80 calls):** Design decisions, 4+ files, ambiguity, or core logic (auth/billing). *Workflow: Architect → Scout → Builder → Reviewer.*
- **Research (≤15 calls):** Inquiry only, no edits. *Workflow: Scout → Answer.*

### 2. Surgical Operations
- **Surgical Reads:** Use `start_line` and `end_line` for `read_file`. Avoid reading more than 400 lines at once.
- **Parallelism:** Batch independent `read_file`, `grep_search`, `glob`, or `run_shell_command` calls in a single turn.
- **No Redundant Re-reads:** Never re-read a file immediately after editing it. Trust the tool's success.
- **Dedicated Tools:** Prefer `read_file`, `write_file`, `replace`, `grep_search`, and `glob` over `run_shell_command` equivalents (cat, echo, sed, grep, find).

### 3. High-Signal Communication
- **Terse Responses:** Single-sentence results with file:line references. No preambles ("I will now..."), no trailing summaries of visible diffs.
- **Mental Findings Cache:** Do not re-search or re-read information already obtained in the current session.

---

## Technical Standards

### 1. Architecture & Patterns
- **Immutability (CRITICAL):** ALWAYS create new objects/structures; NEVER mutate in-place. Use spread operator in TS/JS and `frozen=True` dataclasses in Python.
- **KISS, DRY, YAGNI:** Prioritize simplicity and clarity over cleverness or speculative generality.
- **File & Function Size:** Keep files < 800 lines and functions < 50 lines. Extract utilities proactively.

### 2. Coding Standards
- **Error Handling:** NEVER silently swallow errors. Handle explicitly at every level with detailed context.
- **Input Validation:** ALWAYS validate at system boundaries using schema-based validation (e.g., Zod).
- **Naming:** `camelCase` for variables/functions, `PascalCase` for types/classes, `UPPER_SNAKE_CASE` for constants.

### 3. Language Specifics
- **TypeScript:** Add explicit types to public APIs; avoid `any` (use `unknown` + narrowing); prefer `interface` for extendable objects.
- **Python:** Follow PEP 8; mandatory type annotations on all function signatures; use `black`, `isort`, and `ruff`.

### 4. Testing & Validation
- **Minimum Coverage:** Aim for 80% coverage (Unit, Integration, and E2E).
- **TDD Workflow:** Red (write failing test) → Green (minimal implementation) → Refactor.
- **AAA Pattern:** Structure tests as Arrange-Act-Assert with descriptive naming.

### 5. Shell & Permissions
- **Implicit Approval:** Assume broad permission for shell commands related to maintenance, setup, and project migration.
- **Efficiency:** Favor silent flags (`-y`, `-q`, `--no-pager`) to minimize interactive prompts and output volume.
- **Frictionless Workflow:** To bypass the CLI's built-in confirmation prompts, the user is encouraged to launch with `gemini --yolo` or set an "allow" policy in `~/.gemini/policies/`.

### 6. Social Media Automation
- **Unified Tooling:** Always use the `SocialMedia` MCP server (FastMCP) for platform interactions.
- **Media Strategy:** Favor public CDN URLs (e.g., ImgBB) for media-based posts to ensure compatibility with Graph/Snapchat APIs.
- **Auth Integrity:** Never commit long-lived tokens; use `.env` and provide instructions via the `/setup` flow.
- **Agent Orchestration:** Use Gemini 2.0's Automatic Tool Use to handle cross-platform sequencing.

---

## Workspace Navigation

- `expense-app/`: Node.js/Express backend.
- `studyapp/`: Multi-module application (client/server).
- `trading-app/`: Python-based trading system with MCP servers.
- `portal/`: Registry and API portal.
- `agent-system.pre-ecc-20260521/`: Historical reference for agent configurations and workflows.
