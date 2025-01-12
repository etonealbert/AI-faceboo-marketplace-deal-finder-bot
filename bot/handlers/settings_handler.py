from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Define the InlineKeyboardButtons for the settings
    keyboard = [
        [
            InlineKeyboardButton("Payment Settings", callback_data='some_prefix:payment_settings'),
            InlineKeyboardButton("GPT Model to Use", callback_data='some_prefix:gpt_model'),
        ],
        [
            InlineKeyboardButton("Facebook Login", callback_data='some_prefix:facebook_login'),
            InlineKeyboardButton("Other Settings", callback_data='some_prefix:other_settings'),
        ],
    ]

    # Create InlineKeyboardMarkup
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send a message with the keyboard
    await update.message.reply_text("Choose a setting to configure:", reply_markup=reply_markup)
