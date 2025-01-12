from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
import json
import logging
from telegram.helpers import escape_markdown

logger = logging.getLogger(__name__)

def format_report(data):
    # Форматирование отчёта для пользователя
    return "\n".join([str(item) for item in data])

async def log_all_updates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Received update: {update}")
    

def format_preference(preference):
    emoji_map = {
        "vehicle_type": "🚗",
        "make": "🏷️",
        "model": "📦",
        "year_range": "📅",
        "mileage_range": "🚦",
        "color": "🎨",
        "car_condition": "🔧",
        "location": "📍",
        "transmission": "⚙️",
        "fuel_type": "⛽",
        "drive_type": "🛞",
        "doors": "🚪",
        "listing_condition": "🔖",
        "keywords": "🔑",
        "has_images": "🖼️"
    }

    formatted = []
    for key, value in preference.items():
        if value is not None:  # Skip empty fields
            key_emoji = emoji_map.get(key, "")
            key_safe = key.capitalize()  # No escaping here
            value_safe = escape_markdown(str(value), version=2)  # Escape values only
            if key_emoji:
                formatted.append(f"{key_emoji} *{key_safe}*: {value_safe}")
            else:
                formatted.append(f"*{key_safe}*: {value_safe}")

    return "\n".join(formatted)
