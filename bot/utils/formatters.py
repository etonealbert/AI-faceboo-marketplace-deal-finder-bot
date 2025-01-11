from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
import logging

logger = logging.getLogger(__name__)

def format_report(data):
    # Форматирование отчёта для пользователя
    return "\n".join([str(item) for item in data])

async def log_all_updates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Received update: {update}")