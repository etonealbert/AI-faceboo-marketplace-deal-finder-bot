from telegram import Update
from telegram.ext import ContextTypes

async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Here setups")