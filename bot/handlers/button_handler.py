from telegram.ext import ContextTypes
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Acknowledge the callback query

    # Handle button actions based on callback_data
    if query.data == 'payment_settings':
        await query.edit_message_text(text="💰 Payments is not setup")
    elif query.data == 'gpt_model':
        await query.edit_message_text(text="🤖 No GPT Available")
    elif query.data == 'facebook_login':
        await query.edit_message_text(text="Facebook Login Failed")
    elif query.data == 'other_settings':
        await query.edit_message_text(text="⚙️ No other setting")




