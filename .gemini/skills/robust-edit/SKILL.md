---
name: robust-edit
description: Use this skill when you need to perform surgical code modifications using the 'replace' tool. It provides a strict protocol to prevent edit failures caused by indentation or literal string mismatches.
---

# Skill: Robust Surgical Editing

This skill provides a three-step protocol to ensure that the `replace` tool succeeds on the first attempt by eliminating guesswork regarding whitespace and literal content.

## The Protocol

### Step 1: Locating the Target (Grep)
Use `grep_search` with a specific pattern to identify the target file and the approximate line numbers. Do not proceed until you have a confirmed file path and a line number range.

### Step 2: Capturing Literal Content (Read Exact)
Once the region is identified, use `read_file` with the `start_line` and `end_line` parameters.
*   **Goal**: Capture the **EXACT** literal string of the code you intend to replace.
*   **Critical**: This includes all leading/trailing whitespace, tabs, and newline characters.

### Step 3: Executing the Replacement (Replace)
Using the literal string captured in Step 2 as your `old_string`, perform the replacement.
*   **Instruction**: In the `replace` tool call, provide the literal text exactly as it appeared in the `read_file` output.
*   **Validation**: If the tool returns a "replacement failed" error, **DO NOT RETRY** with a guessed string. Repeat Step 2 to re-capture the literal content and identify any invisible characters or unexpected formatting.

## Best Practices
- **Minimize Scope**: Keep the `old_string` as small as possible while remaining unique.
- **Avoid Wildcards**: The `replace` tool expects a literal match. Do not use regex or placeholders in `old_string`.
- **Batching**: You can read multiple regions in parallel before executing a batch of replacements.
