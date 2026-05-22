---
name: task-tracker-workflow
description: Use this skill for any complex, multi-step task or 'Epic'. It mandates the use of Gemini's native 'tracker_*' tools to manage progress via a persistent Directed Acyclic Graph (DAG) of sub-tasks.
---

# Skill: Task Tracker Workflow (DAG Management)

This skill ensures that complex engineering tasks are broken down into manageable, trackable, and verifiable sub-tasks using Gemini's internal task tracking system.

## The Protocol

### Step 1: Initialize the DAG
For any task classified as "Epic" or "Massive", use `tracker_add_task` to create a parent task. Then, decompose the mission into specific sub-tasks (e.g., "Implement API", "Add Validation", "Write Tests").

### Step 2: Establish Dependencies
Use the `dependencies` parameter in `tracker_add_task` to link sub-tasks. For example, "Write Tests" should depend on "Implement API". This prevents starting work before prerequisites are met.

### Step 3: Progressive Execution
- **Set Active**: Use `tracker_update_task` to set a task's status to `in_progress`.
- **Verify**: Before marking a task as `completed`, run a specific verification command (e.g., test or lint).
- **Update**: Reflect progress in the tracker after every major sub-task completion.

### Step 4: Visualizing State
Periodically use `tracker_visualize` to show the current progress tree to the user. This provides high-transparency and ensures the agent and user are aligned on the current state.

## Best Practices
- **Atomic Tasks**: Keep sub-tasks small enough to be completed in 1-2 agent turns.
- **Dependency First**: Always resolve blocked tasks before moving to parallel tracks.
- **Persistence**: Since the tracker persists state outside the chat history, use it to resume long-running work across multiple sessions.
