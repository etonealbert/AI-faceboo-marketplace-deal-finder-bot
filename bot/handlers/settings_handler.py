from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Define the InlineKeyboardButtons for the settings
    keyboard = [
        [
            InlineKeyboardButton("Payment Settings", callback_data='payment_settings'),
            InlineKeyboardButton("GPT Model to Use", callback_data='gpt_model'),
        ],
        [
            InlineKeyboardButton("Facebook Login", callback_data='facebook_login'),
            InlineKeyboardButton("Other Settings", callback_data='other_settings'),
        ],
    ]

    # Create InlineKeyboardMarkup
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send a message with the keyboard
    await update.message.reply_text("Choose a setting to configure:", reply_markup=reply_markup)
