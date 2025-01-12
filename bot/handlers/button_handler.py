from telegram.ext import ContextTypes
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Acknowledge the callback query

    data = query.data
    # Handle button actions based on callback_data
    if data.startswith("some_prefix:"):
        action = data.split(":")[1]  # Извлекаем действие после префикса
    if action == "payment_settings":
        await query.edit_message_text(text="You selected Payment Settings.")
    elif action == "gpt_model":
        await query.edit_message_text(text="You selected GPT Model.")
    elif action == "facebook_login":
        await query.edit_message_text(text="You selected Facebook Login.")
    elif action == "other_settings":
        await query.edit_message_text(text="You selected Other Settings.")
    else:
        await query.edit_message_text(text="Unknown action.")




