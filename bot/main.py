import logging
from telegram.ext import ApplicationBuilder, CommandHandler
from telegram import ReplyKeyboardRemove
from telegram.ext import  CommandHandler, MessageHandler, filters, ConversationHandler
from config.settings import TELEGRAM_BOT_TOKEN
from bot.handlers.start_handler import start
from bot.handlers.settings_handler import settings
from bot.handlers.report_handler import report
from bot.handlers.subscriptions_handler import handle_subscriptions
from bot.handlers.check_preferences_handler import handle_check_preferences, handle_remove_preference_selection, remove_preference_callback
from bot.handlers.search_new_vehicle_handler import  (
    handle_search_new_vehicle,
    ask_vehicle_type,
    ask_brand,
    ask_model,
    ask_condition,
    ask_price_range,
    ask_year_range,
    ask_mileage_range,
    ask_car_color,
    ask_car_condition,
    ask_location,
    ask_transmission,
    ask_fuel_type,
    ask_drive_type,
    ask_doors,
    ask_listing_condition,
    ask_keywords,
    ask_has_images,
    confirm_preferences
)
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

# Conversation states
(
    SELECT_VEHICLE_TYPE,
    SELECT_BRAND,
    SELECT_MODEL,
    SELECT_CONDITION,
    SELECT_PRICE_RANGE,
    SELECT_YEAR_RANGE,
    SELECT_MILEAGE_RANGE,
    SELECT_CAR_COLOR,
    SELECT_CAR_CONDITION,
    SELECT_OPTIONAL_LOCATION,
    SELECT_OPTIONAL_TRANSMISSION,
    SELECT_OPTIONAL_FUEL_TYPE,
    SELECT_OPTIONAL_DRIVE_TYPE,
    SELECT_OPTIONAL_DOORS,
    SELECT_OPTIONAL_LISTING_CONDITION,
    SELECT_OPTIONAL_KEYWORDS,
    SELECT_OPTIONAL_IMAGES,
    CONFIRM,
) = range(18)

REMOVE_PREFERENCE = 19

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
        BotCommand("report", "Report"),
        BotCommand("cancel", "Cancel"),
        BotCommand("admin", "Admin Pannel"),

    ]
    await application.bot.set_my_commands(commands)

async def fallback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Interrupts the current conversation and ends the ConversationHandler."""
    await update.message.reply_text(
        text="The transport search dialogue has been interrupted. To start over, enter /search.",
        reply_markup=ReplyKeyboardRemove()  # Removes the keyboard
    )
    return ConversationHandler.END



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
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAIN_MENU: [
                MessageHandler(
                    filters.TEXT & filters.Regex("^Setup vehicle preferences$"),
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
                # MessageHandler(filters.TEXT, fallback_handler),
            ],
            SELECT_VEHICLE_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_vehicle_type)],
            SELECT_BRAND: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_brand)],
            SELECT_MODEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_model)],
            SELECT_CONDITION: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_condition)],
            SELECT_PRICE_RANGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_price_range)],
            SELECT_YEAR_RANGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_year_range)],
            SELECT_MILEAGE_RANGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_mileage_range)],
            SELECT_CAR_COLOR: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_car_color)],
            SELECT_CAR_CONDITION: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_car_condition)],
            SELECT_OPTIONAL_LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_location)],
            SELECT_OPTIONAL_TRANSMISSION: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_transmission)],
            SELECT_OPTIONAL_FUEL_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_fuel_type)],
            SELECT_OPTIONAL_DRIVE_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_drive_type)],
            SELECT_OPTIONAL_DOORS: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_doors)],
            SELECT_OPTIONAL_LISTING_CONDITION: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_listing_condition)],
            SELECT_OPTIONAL_KEYWORDS: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_keywords)],
            SELECT_OPTIONAL_IMAGES: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_has_images)],
            CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_preferences)],
            REMOVE_PREFERENCE : [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_remove_preference_selection)],
        },
        fallbacks = [
            MessageHandler(filters.COMMAND, fallback_handler)
        ],
    )
    
    search_vehicle_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("search", handle_search_new_vehicle)],
        states = {
            SELECT_VEHICLE_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_vehicle_type)],
            SELECT_BRAND: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_brand)],
            SELECT_MODEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_model)],
            SELECT_CONDITION: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_condition)],
            SELECT_PRICE_RANGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_price_range)],
            SELECT_YEAR_RANGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_year_range)],
            SELECT_MILEAGE_RANGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_mileage_range)],
            SELECT_CAR_COLOR: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_car_color)],
            SELECT_CAR_CONDITION: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_car_condition)],
            SELECT_OPTIONAL_LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_location)],
            SELECT_OPTIONAL_TRANSMISSION: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_transmission)],
            SELECT_OPTIONAL_FUEL_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_fuel_type)],
            SELECT_OPTIONAL_DRIVE_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_drive_type)],
            SELECT_OPTIONAL_DOORS: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_doors)],
            SELECT_OPTIONAL_LISTING_CONDITION: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_listing_condition)],
            SELECT_OPTIONAL_KEYWORDS: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_keywords)],
            SELECT_OPTIONAL_IMAGES: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_has_images)],
            CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_preferences)],
        },
        fallbacks = [
            MessageHandler(filters.COMMAND, fallback_handler)
        ],
    )
    
    preferences_vehicle_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("preferences", handle_check_preferences)],
        states = {
            REMOVE_PREFERENCE : [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_remove_preference_selection)]
        },
        fallbacks = [
            MessageHandler(filters.COMMAND, fallback_handler)
        ],
    )
    
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, settings))


    application.add_handler(conv_handler)
    application.add_handler(search_vehicle_conv_handler)
    application.add_handler(preferences_vehicle_conv_handler)
    application.add_handler(
        CallbackQueryHandler(button_handler, pattern=r"^some_prefix:.+")
    )
    # Теперь remove_pref:\d+$ не «зацепится» за этот pattern
    application.add_handler(
        CallbackQueryHandler(remove_preference_callback, pattern=r"^remove_pref:\d+$")
    )
    # Set bot commands
    await set_bot_commands(application)
    
    # Start polling
    logger.info("Starting bot polling...")
    await application.run_polling()
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())




