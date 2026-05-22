# Gemini CLI Advanced Agent System (Next-Gen)

An enterprise-grade, multi-agent architecture for Gemini CLI designed for extreme reliability, token efficiency, and autonomous self-correction.

## 🚀 Key Features

*   **AgentsFleet**: A modular team of specialized sub-agents (Orchestrator, Scout, Builder, Reviewer).
*   **Robust Edit Protocol**: Eliminates `replace failed` loops by using a strict "Grep -> Read Exact -> Replace" surgical modification flow.
*   **Autonomous Self-Correction**: A formal S.S.V.E. loop (Stop, Speculate, Verify, Execute) for hypothesis-driven debugging.
*   **State Persistence**: Native integration with Gemini's `tracker_*` tools to manage long-running "Epics" via Directed Acyclic Graphs (DAGs).
*   **Spec-Driven Development**: Codifies requirements into physical artifacts to prevent "requirement drift" in long sessions.
*   **Social Media AI Manager**: A full-featured integration for Twitter (X), Facebook, Instagram, and Snapchat with mobile-optimized onboarding and AI orchestration.

---

## 🚀 Key Integrations: Social Media AI
The `social-mcp-server` provides a unified interface for cross-platform posting:
*   **Intelligent Posting**: Command the bot in plain English: "Post this photo to IG and Twitter".
*   **Automatic Media Handling**: Upload photos via Telegram; the bot handles CDN conversion and API delivery.
*   **Interactive /setup**: Guided walkthroughs for acquiring API keys on Android and iPhone.

---

## 🛠 Installation & Setup

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/0King0P/GeminiSkillsets.git ~/.gemini-custom
    ```

2.  **Deploy Instructions & Agents**:
    Copy the configuration files to your Gemini CLI root:
    ```bash
    cp ~/.gemini-custom/GEMINI.md ~/GEMINI.md
    cp -r ~/.gemini-custom/.gemini/agents/ ~/.gemini/
    cp -r ~/.gemini-custom/.gemini/skills/ ~/.gemini/
    cp ~/.gemini-custom/.gemini/policies/auto-allow.toml ~/.gemini/policies/
    ```

3.  **Enable Auto-Accept (Optional but Recommended)**:
    The included `auto-allow.toml` policy permits Gemini to run shell commands and file edits without manual confirmation prompts.

---

## 📖 How to Use

### 1. Task Classification
The system automatically classifies tasks:
*   **Trivial**: Handled by the Main Agent with the `robust-edit` skill.
*   **Moderate/Complex**: Delegated to the `orchestrator` agent.
*   **Epic**: Triggers the `spec-driven-dev` and `task-tracker-workflow`.

### 2. Manual Agent Invocation
You can manually call a specialist for specific tasks:
```bash
# In chat:
/invoke_agent agent_name="scout" prompt="Map the auth logic in this project."
/invoke_agent agent_name="builder" prompt="Apply the fix described in the plan."
```

### 3. Activating Skills
Skills are procedural guides. Use them to ensure high-quality output:
```bash
# Force a TDD workflow
/activate_skill name="test-driven-dev"
```

---

## 🔍 The S.S.V.E. Debugging Loop
When a build or test fails, the `reviewer` agent automatically triggers this loop:
1.  **S**top: Analyze the error output.
2.  **S**peculate: Formulate 3 hypotheses for the cause.
3.  **V**erify: Gather evidence for the top hypothesis (e.g., check for missing files).
4.  **E**xecute: Apply a targeted fix once verified.

---

## 🛠 Troubleshooting

| Issue | Cause | Solution |
| :--- | :--- | :--- |
| **Replacement Failed** | Mismatch in indentation or invisible characters. | Ensure you use the `robust-edit` skill. It mandates reading the file before replacing. |
| **Agent Not Found** | Incorrect directory structure. | Check that `.md` files are in `~/.gemini/agents/`. |
| **Token Usage High** | Over-exploration in main session. | Delegate the task to `orchestrator` to isolate tool calls in a sub-agent. |
| **Plan Drift** | Session too long for context window. | Initialize the `task-tracker-workflow` to persist progress in a DAG. |
| **Permission Denied** | Root/Sudo requirement or policy lock. | Ensure `auto-allow.toml` is in `~/.gemini/policies/` or run with `--yolo`. |
