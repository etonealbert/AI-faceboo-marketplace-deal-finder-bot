from telegram.ext import ContextTypes, ConversationHandler
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup

MAIN_MENU = range(1)  # Use a single state

async def handle_search_new_vehicle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Handle the "Search new vehicle" button press
    await update.message.reply_text("You pressed 'Search new vehicle'. Proceeding with search...")
    # You can add more logic here to initiate vehicle search
    return ConversationHandler.END