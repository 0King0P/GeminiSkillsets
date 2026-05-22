---
name: test-driven-dev
description: Use this skill to enforce a Test-Driven Development (TDD) workflow. It guides you through the Red-Green-Refactor cycle to ensure code correctness and testability.
---

# Skill: Test-Driven Development (TDD)

This skill provides a structured workflow for implementing features or fixing bugs using TDD principles.

## The TDD Cycle

### Phase 1: Red (Write a Failing Test)
1.  **Understand Requirements**: Identify the expected behavior.
2.  **Write Test**: Create a new test case that describes the behavior.
3.  **Run Test**: Execute the test suite. It **MUST FAIL** at this stage. This confirms the test is valid and targeting the right area.

### Phase 2: Green (Make it Pass)
1.  **Minimal Implementation**: Write the minimum amount of code required to make the test pass.
2.  **Run Test**: Execute the test suite. If it fails, fix the code and repeat until the test passes.

### Phase 3: Refactor (Clean up)
1.  **Improve Code**: Clean up the implementation (naming, structure, performance) without changing its behavior.
2.  **Run Tests**: Execute the test suite again to ensure no regressions were introduced during refactoring.

## Best Practices
- **AAA Pattern**: Organize tests into Arrange, Act, Assert sections.
- **Isolate Tests**: Ensure tests are independent and don't share state.
- **Coverage**: Aim for 100% coverage of the specific logic you are implementing.
