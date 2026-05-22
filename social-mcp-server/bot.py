import os
import logging
import asyncio
import json
import subprocess
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import imgbbpy

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def call_gemini_cli(prompt: str) -> str:
    """Calls the Gemini CLI in headless mode using the existing OAuth session."""
    try:
        # Construct the command
        # We use -p for headless mode and JSON output for parsing
        cmd = ["gemini", "-p", prompt, "--output-format", "json"]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd="/root"  # Run from workspace root to access tools/context
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            err_msg = stderr.decode()
            logger.error(f"Gemini CLI Error: {err_msg}")
            return f"❌ AI Error: {err_msg}"

        data = json.loads(stdout.decode())
        return data.get("response") or data.get("text", "No response received.")
        
    except Exception as e:
        logger.exception("Failed to call Gemini CLI")
        return f"⚠️ System Exception: {str(e)}"

# --- Setup Instructions Text ---
SETUP_INSTRUCTIONS = {
    "twitter": (
        "🐦 *Twitter / X Setup*\n\n"
        "💡 *Tip:* Use a mobile browser (Chrome/Safari) and select 'Request Desktop Site'.\n\n"
        "1. Open the [X Developer Portal](https://developer.twitter.com/en/portal/dashboard).\n"
        "2. Create a 'Project' -> 'App'.\n"
        "3. In App Settings, set Permissions to **'Read and write'**.\n"
        "4. Go to **'Keys and Tokens'** tab.\n"
        "5. Copy these to your `.env`:\n"
        "• `TWITTER_API_KEY`\n"
        "• `TWITTER_API_SECRET`\n"
        "• `TWITTER_ACCESS_TOKEN`\n"
        "• `TWITTER_ACCESS_SECRET`"
    ),
    "facebook": (
        "📘 *Facebook Setup*\n\n"
        "📱 *Finding Page ID on Mobile:*\n"
        "Open FB App -> Go to your Page -> About -> Scroll to bottom to see 'Page ID'.\n\n"
        "1. Open [Meta for Developers](https://developers.facebook.com/apps/).\n"
        "2. Create a 'Business' App.\n"
        "3. Add 'Facebook Login for Business'.\n"
        "4. Use the [Graph Explorer](https://developers.facebook.com/tools/explorer/) to get a **Page Access Token** with `pages_manage_posts`.\n"
        "5. Add to `.env`:\n"
        "• `FB_PAGE_ID`\n"
        "• `FB_PAGE_ACCESS_TOKEN`"
    ),
    "instagram": (
        "📸 *Instagram Setup*\n\n"
        "⚠️ *Requirement:* Your IG must be a **Professional/Creator** account linked to a FB Page.\n\n"
        "1. Go to [Meta Apps Dashboard](https://developers.facebook.com/apps/).\n"
        "2. Add **'Instagram Graph API'** product.\n"
        "3. To find your **IG User ID**:\n"
        "• Use [this lookup tool](https://commentpicker.com/instagram-user-id.php) or use the Graph Explorer.\n"
        "4. Add to `.env`:\n"
        "• `IG_USER_ID`\n"
        "• *(Use your FB_PAGE_ACCESS_TOKEN)*"
    ),
    "snapchat": (
        "👻 *Snapchat Setup*\n\n"
        "💡 *Note:* API setup is best done on a tablet or desktop browser.\n\n"
        "1. Login to [Snap Business Manager](https://business.snapchat.com/).\n"
        "2. Go to **'Business Details'** -> **'Apps'** -> **'Add App'**.\n"
        "3. Select **'Public Profile API'** access.\n"
        "4. Generate OAuth credentials.\n"
        "5. Add to `.env`:\n"
        "• `SNAP_CLIENT_ID`\n"
        "• `SNAP_CLIENT_SECRET`\n"
        "• `SNAP_REFRESH_TOKEN`"
    )
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! 👋 I am your Social Media AI Manager."
        "\n\nI am connected directly to your **Gemini Ultra** session."
        "\n\nExample: 'Post this photo to IG and Twitter with caption #AI'"
        "\n\nType /setup to configure your accounts."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Process user messages using the Gemini CLI subprocess."""
    user_text = update.message.text or update.message.caption or ""
    photo = update.message.photo
    
    await update.message.reply_chat_action("typing")

    if photo:
        imgbb_key = os.getenv("IMGBB_API_KEY")
        if not imgbb_key:
            await update.message.reply_text("⚠️ Please set IMGBB_API_KEY in .env to post photos.")
            return
            
        file = await context.bot.get_file(photo[-1].file_id)
        file_path = f"tmp_{photo[-1].file_id}.jpg"
        await file.download_to_drive(file_path)
        
        try:
            ib_client = imgbbpy.SyncClient(imgbb_key)
            image = ib_client.upload(file=file_path)
            media_url = image.url
            user_text = f"The user attached an image: {media_url}. \n\nRequest: {user_text}"
        except Exception as e:
            await update.message.reply_text(f"❌ Media upload failed: {str(e)}")
            return
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

    # Wrap the prompt with instructions for the CLI
    system_prompt = (
        "Context: Social Media AI Manager. \n"
        "Instructions: Post the following content to the requested platforms. "
        "Use the post_to_twitter, post_to_instagram, etc. tools available in the workspace. "
        "Confirm the result of each tool call.\n\n"
        f"User Prompt: {user_text}"
    )

    response_text = await call_gemini_cli(system_prompt)
    await update.message.reply_text(response_text)

async def setup(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with inline buttons to select a platform to set up."""
    keyboard = [
        [
            InlineKeyboardButton("🐦 Twitter / X", callback_data="setup_twitter"),
            InlineKeyboardButton("📘 Facebook", callback_data="setup_facebook"),
        ],
        [
            InlineKeyboardButton("📸 Instagram", callback_data="setup_instagram"),
            InlineKeyboardButton("👻 Snapchat", callback_data="setup_snapchat"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "⚙️ *Setup Menu*\nChoose a platform to view its step-by-step setup guide:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()

    data = query.data
    if data.startswith("setup_"):
        platform = data.split("_")[1]
        instruction_text = SETUP_INSTRUCTIONS.get(platform, "Instructions not found.")
        
        keyboard = [[InlineKeyboardButton("🔙 Back to Setup Menu", callback_data="setup_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text=instruction_text, reply_markup=reply_markup, parse_mode="Markdown", disable_web_page_preview=True)
    
    elif data == "setup_menu":
        keyboard = [
            [
                InlineKeyboardButton("🐦 Twitter / X", callback_data="setup_twitter"),
                InlineKeyboardButton("📘 Facebook", callback_data="setup_facebook"),
            ],
            [
                InlineKeyboardButton("📸 Instagram", callback_data="setup_instagram"),
                InlineKeyboardButton("👻 Snapchat", callback_data="setup_snapchat"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="⚙️ *Setup Menu*\nChoose a platform to view its step-by-step setup guide:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

def main() -> None:
    """Start the bot."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token or token == "your_telegram_bot_token":
        logger.error("No TELEGRAM_BOT_TOKEN provided in .env file.")
        print("ERROR: Please set TELEGRAM_BOT_TOKEN in social-mcp-server/.env")
        return

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("setup", setup))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_message))

    logger.info("Starting Social Media AI Bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
