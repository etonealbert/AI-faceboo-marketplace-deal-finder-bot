from telegram import Update
from telegram.ext import ContextTypes

REPORT_STATE, ADMIN_STATE, SUPPORT_STATE, UPDATE_STATE = range(20, 24)

async def handle_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Report is not ready.")
    
    return REPORT_STATE
 