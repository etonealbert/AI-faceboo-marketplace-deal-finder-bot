import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_ADMIN_API_KEY = os.getenv('OPENAI_ADMIN_API_KEY')

DB_PATH = "marketplace.db"