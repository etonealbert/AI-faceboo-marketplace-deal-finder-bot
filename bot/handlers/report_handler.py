from telegram import Update
from telegram.ext import ContextTypes

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ваш отчёт готов.")