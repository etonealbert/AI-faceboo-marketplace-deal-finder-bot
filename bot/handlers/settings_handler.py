from telegram import Update
from telegram.ext import ContextTypes
from telegram import BotCommand

async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Here setups")


