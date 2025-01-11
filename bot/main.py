from telegram import BotCommand

def main():
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
    
    # Set bot commands for the menu
    commands = [
    BotCommand("start", "🚀 Start the bot and show the welcome message"),
    BotCommand("search", "🔍 New vehicle search"),
    BotCommand("preferences", "My preferencess"),
    BotCommand("update_subscriptions", "🔄 Update your subscriptions"),
    BotCommand("settings", "⚙️ Settings"),
    BotCommand("support", "💬 Support")
    ]
    application.bot.set_my_commands(commands)
    
    # Start polling
    logger.info("Starting bot polling...")
    application.run_polling()

if __name__ == "__main__":
    main()
