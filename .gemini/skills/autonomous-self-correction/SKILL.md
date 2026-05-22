---
name: autonomous-self-correction
description: Use this skill when a build, test, or linter fails. It enforces a rigorous, hypothesis-driven debugging loop to prevent blind 'trial and error' fixes.
---

# Skill: Autonomous Self-Correction (S.S.V.E. Loop)

This skill provides a structured method for resolving failures without user intervention, maximizing autonomous reliability.

## The S.S.V.E. Loop

### 1. **Stop (Analysis)**
Do not touch code immediately. Analyze the error output. Identify the specific file, line number, and error message.

### 2. **Speculate (Hypothesize)**
List 2-3 potential causes for the failure.
*   *Example*: "Hypothesis 1: Missing import for `X`", "Hypothesis 2: Type mismatch in `Y`", "Hypothesis 3: Environment variable `Z` is unset".

### 3. **Verify (Evidence Gathering)**
Use `read_file`, `grep_search`, or `run_shell_command` to gather evidence for your first hypothesis.
*   *Validation*: Do NOT apply a fix until you have seen the evidence (e.g., you've read the file and confirmed the import is indeed missing).

### 4. **Execute (Targeted Fix)**
Apply the fix only for the verified hypothesis. Use the `robust-edit` protocol.

### 5. **Evaluate (Re-verification)**
Re-run the failing command.
- **Success**: Update the handoff and proceed.
- **Failure**: Repeat the loop with a new hypothesis. If 3 loops fail, stop and escalate to the user with your findings.

## Best Practices
- **No Blind Retries**: Never apply the same fix twice hoping for a different result.
- **Isolate Changes**: Fix one error at a time.
- **Root Cause**: Aim to fix the source of the error, not just the symptom.
