import os
from dotenv import load_dotenv

load_dotenv()

# BotFather'dan olingan tokenni shu yerga yoki .env fayliga yozing
BOT_TOKEN = os.getenv("BOT_TOKEN", "SIZNING_BOT_TOKENINGIZ")

# Admin(lar)ning Telegram user ID raqamlari (bir nechta bo'lishi mumkin)
# ID ni bilish uchun @userinfobot ga /start yozing
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "123456789").split(",") if x.strip()]

DB_PATH = os.getenv("DB_PATH", "ish_bot.db")
