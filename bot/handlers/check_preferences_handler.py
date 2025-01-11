from telegram.ext import ContextTypes, ConversationHandler
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup


async def handle_check_preferences(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Handle the "Check preferences" button press
    await update.message.reply_text("You pressed 'Check preferences'. Here are your preferences...")
    # Add logic to show preferences
    return ConversationHandler.END