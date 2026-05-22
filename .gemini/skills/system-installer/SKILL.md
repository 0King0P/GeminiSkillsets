---
name: system-installer
description: Use this skill to perform a full interactive setup of the GeminiSkillsets architecture. It automates file deployment, environment configuration, and credential setup for the Social Media AI Manager.
---

# Skill: Interactive System Installer

This skill provides a comprehensive, automated onboarding experience for the GeminiSkillsets ecosystem.

## Activation
Trigger this skill by saying: "Run the system installer", "Setup my workspace", or "Install Gemini Skillsets".

## The Installation Protocol

### Step 1: File Deployment
Automatically copy the core architecture files from the repository to the global configuration:
- Copy `GEMINI.md` to `~/GEMINI.md`.
- Copy `.gemini/agents/` to `~/.gemini/agents/`.
- Copy `.gemini/skills/` to `~/.gemini/skills/`.
- Copy `.gemini/policies/` to `~/.gemini/policies/`.

### Step 2: Environment Provisioning
Initialize the Python environment for the Social Media AI Manager:
1. Navigate to `social-mcp-server/`.
2. Check for `uv` installation.
3. Run `uv sync` to install all dependencies.

### Step 3: Interactive Credential Setup
Prompt the user for the following required keys using `ask_user`:
- `TELEGRAM_BOT_TOKEN`: From @BotFather.
- `IMGBB_API_KEY`: From api.imgbb.com (to allow photo posting from your phone).

*Note: `GEMINI_API_KEY` is no longer required, as the system leverages your existing Ultra/OAuth session.*

Once provided, write them securely to `social-mcp-server/.env`.

### Step 4: Final Launch
Offer to start the bot immediately:
- "Would you like to start the Social Media AI Bot now?"
- If yes, run `uv run python bot.py` in the background.

## Troubleshooting
- If a step fails, use the `autonomous-self-correction` skill to diagnose issues (e.g., missing `uv`, write permissions).
- Ensure the user is running this from the `GeminiSkillsets` root directory.
