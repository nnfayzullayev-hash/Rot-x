from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

BTN_ISH_BERISH = "💼 Ish berish"
BTN_ISH_OLISH = "🔍 Ish olish"
BTN_ISHLAR = "📋 Ishlar"
BTN_YANGILIKLAR = "📰 Yangiliklar"
BTN_SLAYD_BUYURTMA = "🎨 Slayd buyurtma"


def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_ISH_BERISH), KeyboardButton(text=BTN_ISH_OLISH)],
            [KeyboardButton(text=BTN_ISHLAR), KeyboardButton(text=BTN_YANGILIKLAR)],
            [KeyboardButton(text=BTN_SLAYD_BUYURTMA)],
        ],
        resize_keyboard=True,
    )
