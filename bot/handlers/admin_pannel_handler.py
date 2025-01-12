from telegram.ext import ContextTypes, ConversationHandler
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove


REPORT_STATE, ADMIN_STATE, SUPPORT_STATE, UPDATE_STATE = range(20, 24)

async def handle_admin_pannel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Handle the "Subscriptions" button press
    await update.message.reply_text(
        "If you want to fix smth commit here https://github.com/etonealbert/AI-faceboo-marketplace-deal-finder-bot ",
        reply_markup=ReplyKeyboardRemove()  # Удаляет клавиатуру
    )
    
    # Add logic for subscriptions
    return ADMIN_STATE