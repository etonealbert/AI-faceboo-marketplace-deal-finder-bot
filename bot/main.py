import logging
from telegram.ext import ApplicationBuilder, CommandHandler
from telegram.ext import  CommandHandler, MessageHandler, filters, ConversationHandler
from config.settings import TELEGRAM_BOT_TOKEN
from bot.handlers.start_handler import start
from bot.handlers.settings_handler import settings
from bot.handlers.report_handler import report
from bot.handlers.subscriptions_handler import handle_subscriptions
from bot.handlers.check_preferences_handler import handle_check_preferences
from bot.handlers.search_new_vehicle_handler import handle_search_new_vehicle
from telegram import Update
from telegram.ext import ContextTypes
from config.logging_config import setup_logging
from database.db import init_db, SessionLocal
from database.models import User, ContactedSeller
from telegram import BotCommand
from telegram.ext import CallbackQueryHandler
from bot.handlers.button_handler import button_handler

import nest_asyncio
nest_asyncio.apply()

# Define states for the conversation handler
MAIN_MENU = range(1)  # Use a single state

# Logging setup
logger = logging.getLogger(__name__)

async def set_bot_commands(application):
    commands = [
        BotCommand("start", "🚀 Start the bot"),
        BotCommand("search", "🔍 New search"),
        BotCommand("preferences", "My preferences"),
        BotCommand("update", "🔄 Update"),
        BotCommand("settings", "⚙️ Settings"),
        BotCommand("support", "💬 Support"),
        BotCommand("report", "Report")

    ]
    await application.bot.set_my_commands(commands)

async def fallback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Just log whatever text user sent that didn't match
    logger.info(f"Fallback triggered. User message text: {update.message.text}")
    await update.message.reply_text("I didn't understand that, sorry!")
    return MAIN_MENU  # or stay in the same state


async def main():
    # Initialize logging
    setup_logging()

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
    application.add_handler(CommandHandler("settings", settings))
    application.add_handler(CommandHandler("report", report))
    application.add_handler(CallbackQueryHandler(button_handler))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAIN_MENU: [
                MessageHandler(
                    filters.TEXT & filters.Regex("^Search new vehicle$"),
                    handle_search_new_vehicle
                ),
                MessageHandler(
                    filters.TEXT & filters.Regex("^Check preferences$"),
                    handle_check_preferences
                ),
                MessageHandler(
                    filters.TEXT & filters.Regex("^Subscriptions$"),
                    handle_subscriptions
                ),
                # Add a fallback to catch everything else
                MessageHandler(filters.TEXT, fallback_handler),
            ]
        },
        fallbacks=[MessageHandler(filters.ALL, fallback_handler)],
    )

    
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, settings))


    application.add_handler(conv_handler)

    # Set bot commands
    await set_bot_commands(application)
    
    # Start polling
    logger.info("Starting bot polling...")
    await application.run_polling()
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())


