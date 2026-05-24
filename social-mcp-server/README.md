# Social Media AI Manager (Telegram Bot)

A highly capable, multimodal Telegram bot that integrates directly with the Gemini CLI as a Universal AI Assistant. This bot allows you to manage social media platforms, search the web, analyze documents, and interact with the AI using text, voice, and media.

## 🚀 Features

*   **Universal Multimodal Input:** Accepts Voice Notes, Audio, Video, Documents, and Images. Files are downloaded locally and fed directly to the Gemini agent's vision/audio systems.
*   **Intelligent Media Output:** The bot can generate charts or fetch documents, returning them directly in Telegram. (The AI uses `[FILE: /path/...]` tags to trigger file sending).
*   **Smart Compression:** Automatically compresses images that exceed Telegram's 10MB limit using `Pillow`, or falls back to sending them as documents (up to 50MB).
*   **Session Isolation:** Operates in a dedicated, persistent session (`gemini-telegram-chat`) so it never interrupts or overwrites your active terminal workflows.
*   **Tool Calling (Agentic):** Uses the `gemini-3-flash-preview` model, giving it the ability to perform live web searches, execute code, and call custom FastMCP tools.
*   **Social Media Integrations:** Ships with tools to post to Twitter, Facebook, Instagram, and Snapchat (Requires credentials via `.env`).
*   **Zero-Friction Execution:** Runs silently in the background with auto-approval for tool calls (`--yolo` and `--skip-trust`).

## ⚙️ Setup & Installation

1.  **Environment Variables:**
    Copy `.env.example` to `.env` and fill in your details:
    ```bash
    cp .env.example .env
    ```
    *Required:* `TELEGRAM_BOT_TOKEN`
    *Optional (for posting):* `TWITTER_API_KEY`, `FB_PAGE_ID`, `IG_USER_ID`, etc.

2.  **Dependencies:**
    The project relies on `uv` for fast dependency management.
    ```bash
    uv pip install -r requirements.txt  # Or rely on the pyproject.toml
    # Specifically requires: python-telegram-bot, Pillow, imgbbpy, google-genai
    ```

3.  **Running the Bot:**
    To run the bot silently in the background, use:
    ```bash
    nohup uv run python bot.py > bot.log 2>&1 &
    ```

## 🤖 Usage (Telegram Commands)

*   `/start` - Initializes the bot and provides a welcome overview.
*   `/setup` - Displays an interactive menu with step-by-step guides for obtaining API keys for various social platforms.
*   `/ping` - A quick health check to verify the background service is running.

## 🛠️ Architecture

*   **bot.py:** The Telegram polling loop. Intercepts messages and media, downloads attachments to `/uploads`, and constructs the prompt.
*   **call_gemini_cli:** An async wrapper that spawns the `gemini` command-line tool, injecting the user's prompt and any local file paths.
*   **MCP Server (`server.py`):** Provides the specific tools (e.g., `post_to_twitter`) that the Gemini agent can invoke during its reasoning process.

## 📝 Recent Upgrades
*   Migrated to `gemini-3-flash-preview` for enhanced agentic capabilities.
*   Implemented `Pillow` image downscaling to respect Telegram's strict payload limits.
*   Detached background service lifecycle management to ensure terminal independence.
