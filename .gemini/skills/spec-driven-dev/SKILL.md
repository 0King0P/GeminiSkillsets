---
name: spec-driven-dev
description: Use this skill to transition from ephemeral chat instructions to persistent, spec-driven engineering. It mandates the creation and maintenance of a physical Markdown specification file for any new feature.
---

# Skill: Spec-Driven Development

This skill eliminates "requirement drift" by ensuring that the source of truth for a feature is a physical file in the repository, not the chat history.

## The Protocol

### Step 1: Draft the Specification
Before writing code, create a `.gemini/specs/<feature-name>.md` file. The spec must include:
- **Background**: Why are we doing this?
- **Requirements**: Functional and non-functional.
- **Architecture**: How will it be built? (Components, APIs, Data Schema).
- **Verification**: How will we know it works?

### Step 2: User Review (Plan Mode)
Use `enter_plan_mode` to draft and refine the spec. Only exit once the user has approved the physical file.

### Step 3: Implementation via Spec
The `builder` agent must read the spec file at the start of every turn. It treats the spec as its primary directive, overriding ephemeral or conflicting chat history.

### Step 4: Maintaining the Living Doc
If requirements change during implementation, **update the spec file first** before modifying the code. This ensures documentation and implementation never diverge.

## Best Practices
- **Explicit Constraints**: Use the spec to define what is NOT in scope to prevent creep.
- **Traceability**: Link sub-tasks in the `task-tracker` back to specific requirement IDs in the spec.
