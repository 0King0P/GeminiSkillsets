import os
import logging
import asyncio
import json
import subprocess
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import imgbbpy
from PIL import Image

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
import re
from google import genai
from google.genai import types

async def call_gemini_cli(prompt: str) -> str:
    """Calls the Gemini CLI with speed and session optimizations."""
    session_name = "gemini-telegram-chat"
    try:
        # First attempt: Resume existing session
        cmd = [
            "gemini", 
            "-p", prompt, 
            "--output-format", "text", 
            "-m", "gemini-3-flash-preview",
            "--resume", session_name,
            "--yolo",
            "--skip-trust"
        ]
        logger.info(f"Calling Gemini CLI (Resume: {session_name}) with prompt: {prompt[:50]}...")
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd="/root"
        )
        
        try:
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=120)
        except asyncio.TimeoutError:
            process.kill()
            return "❌ AI Error: Request timed out."
            
        stdout_str = clean_ansi(stdout.decode()).strip()
        stderr_str = clean_ansi(stderr.decode()).strip()
        combined_output = stdout_str + " " + stderr_str

        # If resume failed because session doesn't exist, start a new one
        if process.returncode != 0 and "Invalid session identifier" in combined_output:
            logger.info(f"Session {session_name} not found. Initializing new session...")
            cmd_new = [
                "gemini", 
                "-p", prompt, 
                "--output-format", "text", 
                "-m", "gemini-3-flash-preview",
                "--session-id", session_name,
                "--yolo",
                "--skip-trust"
            ]
            process = await asyncio.create_subprocess_exec(
                *cmd_new,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd="/root"
            )
            try:
                stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=120)
            except asyncio.TimeoutError:
                process.kill()
                return "❌ AI Error: Request timed out."
                
            stdout_str = clean_ansi(stdout.decode()).strip()
            stderr_str = clean_ansi(stderr.decode()).strip()

        if process.returncode != 0 and not stdout_str:
            logger.error(f"Gemini CLI Error: {stderr_str} | {stdout_str}")
            return f"❌ AI Error: {stderr_str or stdout_str or 'Unknown system error'}"

        return stdout_str
        
    except Exception as e:
        logger.exception("Failed to call Gemini CLI")
        return f"⚠️ System Exception: {str(e)}"

def clean_ansi(text: str) -> str:
    """Removes ANSI escape sequences from a string."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

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
        rf"Hi {user.mention_html()}! 👋 I am your Universal AI Assistant."
        "\n\nI am connected directly to your **Gemini Ultra** session and have full tool capabilities."
        "\n\nYou can now:\n"
        "🔹 **Search the Web** (just ask!)\n"
        "🔹 **Send Voice Notes** for me to hear\n"
        "🔹 **Attach Documents** for analysis\n"
        "🔹 **Post to Social Media** (Twitter, IG, FB, Snap)\n\n"
        "Type /setup to configure your social accounts."
    )

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Verify the bot is alive."""
    await update.message.reply_text("🏓 Pong! Universal Bot is active.")

async def typing_loop(message):
    """Keep the typing indicator active during long requests."""
    while True:
        try:
            await message.reply_chat_action("typing")
            await asyncio.sleep(4)
        except Exception:
            break

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Process user messages with native multimodal support and tool access."""
    message = update.message
    user_text = message.text or message.caption or ""
    
    # Identify attachment
    attachment = message.photo or message.voice or message.document or message.video or message.audio
    
    # Start typing indicator in background
    typing_task = asyncio.create_task(typing_loop(message))

    local_file_path = None
    try:
        if attachment:
            # Determine which file to download
            if message.photo:
                file_obj = await context.bot.get_file(message.photo[-1].file_id)
                ext = "jpg"
            elif message.voice:
                file_obj = await context.bot.get_file(message.voice.file_id)
                ext = "ogg"
            elif message.document:
                file_obj = await context.bot.get_file(message.document.file_id)
                ext = message.document.file_name.split('.')[-1] if "." in message.document.file_name else "bin"
            elif message.video:
                file_obj = await context.bot.get_file(message.video.file_id)
                ext = "mp4"
            elif message.audio:
                file_obj = await context.bot.get_file(message.audio.file_id)
                ext = "mp3"

            # Create absolute path for Gemini CLI to ingest
            os.makedirs("/root/social-mcp-server/uploads", exist_ok=True)
            local_file_path = f"/root/social-mcp-server/uploads/{file_obj.file_id}.{ext}"
            await file_obj.download_to_drive(local_file_path)
            
            # Enrich prompt with file context
            user_text = f"The user attached a file: {local_file_path}\n\nUser Request: {user_text}"

        # Optimized Agent Prompt
        system_prompt = (
            "Role: Universal Agent. \n"
            "Capabilities: Web, Vision, Audio, Tool-calling. \n"
            "Task: Fulfill request. Use tools as needed. \n"
            "Media Output: To send a file/image, output '[FILE: /path/to/file]'. \n"
            "Charts: Generate charts as images and use the [FILE: ...] tag.\n\n"
            f"{user_text}"
        )

        response_text = await call_gemini_cli(system_prompt)
        
        # Parse for [FILE: path] or [IMAGE: path]
        media_pattern = re.compile(r'\[(?:FILE|IMAGE|CHART):\s*(.*?)\]', re.IGNORECASE)
        files_to_send = media_pattern.findall(response_text)
        
        # Clean the text of the tags
        clean_text = media_pattern.sub('', response_text).strip()
        
        if clean_text:
            await message.reply_text(clean_text, parse_mode="Markdown")
            
        for f_path in files_to_send:
            f_path = f_path.strip()
            if os.path.exists(f_path):
                file_size = os.path.getsize(f_path)
                is_image = f_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))
                
                # Telegram limits: Photo=10MB, Document=50MB
                if is_image and file_size > 9_500_000: # Slightly under 10MB to be safe
                    try:
                        logger.info(f"Compressing large image: {f_path} ({file_size} bytes)")
                        img = Image.open(f_path)
                        # Convert to RGB if it's RGBA (for JPEG compatibility)
                        if img.mode in ("RGBA", "P"): img = img.convert("RGB")
                        # Downscale maintaining aspect ratio
                        img.thumbnail((2048, 2048), Image.Resampling.LANCZOS)
                        
                        compressed_path = f_path + "_compressed.jpg"
                        img.save(compressed_path, "JPEG", quality=85, optimize=True)
                        
                        # Send compressed version
                        await message.reply_photo(photo=open(compressed_path, 'rb'))
                        os.remove(compressed_path)
                    except Exception as img_e:
                        logger.error(f"Image compression failed, sending as document: {img_e}")
                        # Fallback to document (50MB limit) if it's < 50MB
                        if file_size < 49_000_000:
                            await message.reply_document(document=open(f_path, 'rb'))
                        else:
                            await message.reply_text(f"⚠️ File is too large for Telegram (>50MB): {os.path.basename(f_path)}")
                elif is_image:
                    await message.reply_photo(photo=open(f_path, 'rb'))
                else:
                    # Not an image
                    if file_size < 49_000_000:
                        await message.reply_document(document=open(f_path, 'rb'))
                    else:
                        await message.reply_text(f"⚠️ File is too large for Telegram (>50MB): {os.path.basename(f_path)}")
            else:
                logger.warning(f"AI requested sending non-existent file: {f_path}")
    
    except Exception as e:
        logger.exception("Error in handle_message")
        await message.reply_text(f"⚠️ Error: {str(e)}")
    finally:
        typing_task.cancel()
        # Cleanup received file
        if local_file_path and os.path.exists(local_file_path):
            try:
                os.remove(local_file_path)
            except:
                pass

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
    application.add_handler(CommandHandler("ping", ping))
    application.add_handler(CommandHandler("setup", setup))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(
        filters.TEXT | filters.PHOTO | filters.VIDEO | filters.Document.ALL | filters.VOICE | filters.AUDIO, 
        handle_message
    ))

    logger.info("Starting Social Media AI Bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
