from telethon import TelegramClient, events
import asyncio
import os
import re
from datetime import datetime, time

# Get credentials from environment variables (for security)
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Default settings
SOURCE_CHATS = []  # Set via Telegram commands
FORWARD_TO_CHAT_IDS = []  # Set via Telegram commands
KEYWORDS = []  # Filter messages with specific keywords
BLACKLISTED_WORDS = []  # Block messages with these words
CLEAN_WORDS = []  # Words to clean from messages
CLEAN_URLS = False
CLEAN_MENTIONS = False
FORWARD_MEDIA_ONLY = False
FORWARD_DELAY = 2  # Delay in seconds
auto_reply_enabled = True
AUTO_REPLY_TEXT = "Thank you for your message! Our team will get back to you soon."
FORMAT_HEADER = "\U0001F4E2 *Forwarded Message:*\n"
FORMAT_FOOTER = "\n\U0001F517 *Original Source:* {source}"
DUPLICATE_CACHE = set()
SCHEDULED_HOURS = None

# Initialize Telethon bot client
bot = TelegramClient("bot_session", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

async def start_bot():
    @bot.on(events.NewMessage(pattern="/start"))
    async def start(event):
        await event.reply("Welcome! Use /settings to configure.")

    @bot.on(events.NewMessage(pattern="/settings"))
    async def show_settings(event):
        settings_text = (
            f"✅ **Current Settings:**\n"
            f"**Forwarding to:** {FORWARD_TO_CHAT_IDS}\n"
            f"**Keywords:** {KEYWORDS}\n"
            f"**Blacklist Words:** {BLACKLISTED_WORDS}\n"
            f"**Schedule:** {SCHEDULED_HOURS if SCHEDULED_HOURS else 'Not Set'}\n"
        )
        await event.reply(settings_text)

    @bot.on(events.NewMessage)
    async def forward_message(event):
        message_text = event.message.message
        if any(blackword in message_text.lower() for blackword in BLACKLISTED_WORDS):
            return  # Block message

        if any(keyword in message_text.lower() for keyword in KEYWORDS) or not KEYWORDS:
            for chat_id in FORWARD_TO_CHAT_IDS:
                formatted_message = f"{FORMAT_HEADER}{message_text}{FORMAT_FOOTER.format(source=event.chat_id)}"
                await bot.send_message(chat_id, formatted_message)
    
    print("Bot is running...")
    await bot.run_until_disconnected()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    loop.run_until_complete(start_bot())
