import logging
from telegram.ext import ApplicationBuilder, CommandHandler
from config.settings import TELEGRAM_BOT_TOKEN
from bot.handlers.start_handler import start
from bot.handlers.settings_handler import settings
from bot.handlers.report_handler import report
from config.logging_config import setup_logging
from database.db import init_db, SessionLocal
from database.models import User, ContactedSeller
from telegram import BotCommand
import nest_asyncio
nest_asyncio.apply()

async def set_bot_commands(application):
    commands = [
        BotCommand("start", "🚀 Start the bot"),
        BotCommand("search", "🔍 New vehicle search"),
        BotCommand("preferences", "My preferences"),
        BotCommand("update", "🔄 Update"),
        BotCommand("settings", "⚙️ Settings"),
        BotCommand("support", "💬 Support")
    ]
    await application.bot.set_my_commands(commands)

async def main():
    # Initialize logging
    setup_logging()
    logger = logging.getLogger(__name__)

    # Check for token
    if not TELEGRAM_BOT_TOKEN:
        logger.error("The TELEGRAM_BOT_TOKEN is missing. Please check your .env file.")
        raise ValueError("The TELEGRAM_BOT_TOKEN is missing. Please check your .env file.")
    
    # Initialize database
    init_db()
    logger.info("Database initialized successfully.")
    
    # Create the Telegram Bot application
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("settings", settings))
    application.add_handler(CommandHandler("report", report))
    
    # Set bot commands
    await set_bot_commands(application)
    
    # Start polling
    logger.info("Starting bot polling...")
    await application.run_polling()
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())


