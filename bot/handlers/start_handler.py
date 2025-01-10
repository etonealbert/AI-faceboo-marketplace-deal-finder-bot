import logging
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"Received /start command from user {user.id} ({user.username})")
    await update.message.reply_text("Deal bot started okay good good")

    # Creating a new user
# with SessionLocal() as session:
#     new_user = User(username="JohnDoe", preferences='{"vehicleType":"SUV","priceRange":"10k-15k"}')
#     session.add(new_user)
#     session.commit()

# # Querying
# with SessionLocal() as session:
#     user = session.query(User).filter_by(username="JohnDoe").first()
#     if user:
#         print(user.preferences)