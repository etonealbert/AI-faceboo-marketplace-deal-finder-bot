from telegram.ext import ContextTypes, ConversationHandler
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove


async def handle_subscriptions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Handle the "Subscriptions" button press
    await update.message.reply_text(
        "You pressed 'Subscriptions'. Here are your subscriptions...",
        reply_markup=ReplyKeyboardRemove()  # Удаляет клавиатуру
    )
    
    # Add logic for subscriptions
    return ConversationHandler.END