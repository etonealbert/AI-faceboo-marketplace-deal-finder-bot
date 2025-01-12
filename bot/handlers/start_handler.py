from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
)
from database.models import User
from database.db import SessionLocal

import logging

# Logging setup
logger = logging.getLogger(__name__)

# Define states for the conversation handler

MAIN_MENU = range(1) 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"Received /start command from user {user.id} ({user.username})")

    # Use a default username if it's None
    username = user.username or f"user_{user.id}"

    # Start a database session
    with SessionLocal() as session:
        # Check if the user already exists
        existing_user = (
            session.query(User)
            .filter((User.telegram_id == user.id))
            .first()
        )

        if existing_user:
            logger.info(f"User {username} already exists with ID {user.id}")

            # Check if the preferences field is not empty
            if existing_user.preferences:
                # Preferences exist, show all three buttons
                keyboard = [
                    [KeyboardButton("Check preferences")],
                    [KeyboardButton("Subscriptions")],
                    [KeyboardButton("Subscribe on vehicle")],
                ]
            else:
                # Preferences do not exist, show only one button
                keyboard = [[KeyboardButton("Search new vehicle")]]
        else:
            # Create a new user if it doesn't exist
            new_user = User(telegram_id=user.id, username=username)
            session.add(new_user)
            session.commit()
            logger.info(f"Created new user {username} with ID {user.id}")

            # New user, show only one button
            keyboard = [[KeyboardButton("Search new vehicle")]]

    # Send a message with the appropriate buttons
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    logger.info(f"User message: {update.message.text}")

    await update.message.reply_text(
        "Choose an option:", 
        reply_markup=reply_markup
    )
    return MAIN_MENU  # Single main state
