from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from sqlalchemy.orm import Session
from database.models import User
from database.db import SessionLocal
import logging

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"Received /start command from user {user.id} ({user.username})")
    
    # Use a default username if it's None
    username = user.username or f"user_{user.id}"  # Assign a fallback username if `user.username` is None
    
    # Start a database session
    with SessionLocal() as session:
        # Check if the user already exists
        existing_user = session.query(User).filter((User.id == user.id) | (User.username == username)).first()
        
        if existing_user:
            logger.info(f"User {username} already exists with ID {user.id}")
            
            # Check if the preferences field is not empty
            if existing_user.preferences:
                # Preferences exist, show all three buttons
                keyboard = [
                    [KeyboardButton("Check preferences")],
                    [KeyboardButton("Subscriptions")],
                    [KeyboardButton("Search new vehicle")]
                ]
            else:
                # Preferences do not exist, show only one button
                keyboard = [
                    [KeyboardButton("Search new vehicle")]
                ]
        else:
            # Create a new user if it doesn't exist
            new_user = User(id=user.id, username=username)
            session.add(new_user)
            session.commit()
            logger.info(f"Created new user {username} with ID {user.id}")
            
            # New user, show only one button
            keyboard = [
                [KeyboardButton("Search new vehicle")]
            ]
    
    # Send a message with the appropriate buttons
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Choose an option:", reply_markup=reply_markup)


# # Querying
# with SessionLocal() as session:
#     user = session.query(User).filter_by(username="JohnDoe").first()
#     if user:
#         print(user.preferences)