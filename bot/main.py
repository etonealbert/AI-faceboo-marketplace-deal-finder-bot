# bot/main.py
import logging
from telegram.ext import ApplicationBuilder, CommandHandler
from config.settings import TELEGRAM_BOT_TOKEN
from bot.handlers.start_handler import start
from bot.handlers.settings_handler import settings
from bot.handlers.report_handler import report
from config.logging_config import setup_logging
from database.db import init_db, SessionLocal
from database.models import User, ContactedSeller


def main():
    # Инициализация логирования
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Проверяем наличие токена
    if not TELEGRAM_BOT_TOKEN:
        logger.error("The TELEGRAM_BOT_TOKEN is missing. Please check your .env file.")
        raise ValueError("The TELEGRAM_BOT_TOKEN is missing. Please check your .env file.")
    
    # Инициализация базы данных
    init_db()  # Call this at the start of your application
    logger.info("Database initialized successfully.")
    
    # Создание приложения Telegram Bot
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("settings", settings))
    application.add_handler(CommandHandler("report", report))
    
    # Запуск polling
    logger.info("Starting bot polling...")
    application.run_polling()

if __name__ == "__main__":
    main()