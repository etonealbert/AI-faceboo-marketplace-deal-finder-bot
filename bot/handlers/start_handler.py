import logging
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"Received /start command from user {user.id} ({user.username})")
    await update.message.reply_text("Deal bot started okay good good")