from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

import database as db
from config import ADMIN_IDS
from keyboards import (
    main_menu,
    BTN_ISH_BERISH,
    BTN_ISH_OLISH,
    BTN_ISHLAR,
    BTN_YANGILIKLAR,
    BTN_SLAYD_BUYURTMA,
)

router = Router()


class SlideOrderStates(StatesGroup):
    waiting_for_topic = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Assalomu alaykum! 👋\n\n"
        "Bu bot orqali siz:\n"
        "💼 <b>Ish berish</b> — ishchi/ijrochi qidirayotgan bo'lsangiz\n"
        "🔍 <b>Ish olish</b> — ish qidirayotgan bo'lsangiz\n\n"
        "kerakli bo'limni tanlang 👇",
        reply_markup=main_menu(),
    )


@router.message(F.text == BTN_ISH_BERISH)
async def ish_berish(message: Message):
    nickname = await db.get_setting("admin_nickname")
    if not nickname:
        await message.answer(
            "Hozircha admin bilan bog'lanish uchun nickname o'rnatilmagan. "
            "Birozdan so'ng qayta urinib ko'ring."
        )
        return
    await message.answer(
        "Ish beruvchi sifatida ishingizni joylashtirish uchun quyidagi admin bilan "
        f"bog'laning:\n\n👤 {nickname}\n\n"
        "Unga ish tavsifini yuboring, u sizning e'loningizni ro'yxatga qo'shadi."
    )


async def _send_jobs_list(message: Message):
    jobs = await db.get_all_jobs()
    if not jobs:
        await message.answer("Hozircha hech qanday ish e'loni yo'q. Keyinroq qayta tekshiring 🙂")
        return

    text_parts = ["📋 <b>Mavjud ishlar:</b>\n"]
    for job in jobs:
        text_parts.append(
            f"🔹 {job['description']}\n👤 Bog'lanish: {job['employer_nickname']}\n"
        )
    await message.answer("\n".join(text_parts))


@router.message(F.text == BTN_ISH_OLISH)
async def ish_olish(message: Message):
    await _send_jobs_list(message)


@router.message(F.text == BTN_ISHLAR)
async def ishlar(message: Message):
    await _send_jobs_list(message)


@router.message(F.text == BTN_YANGILIKLAR)
async def yangiliklar(message: Message):
    news_items = await db.get_all_news()
    if not news_items:
        await message.answer("Hozircha yangiliklar yo'q.")
        return

    text_parts = ["📰 <b>Yangiliklar:</b>\n"]
    for item in news_items:
        text_parts.append(f"• {item['text']}")
    await message.answer("\n\n".join(text_parts))


@router.message(F.text == BTN_SLAYD_BUYURTMA)
async def slayd_buyurtma(message: Message, state: FSMContext):
    await state.set_state(SlideOrderStates.waiting_for_topic)
    await message.answer("✍️ Slayd mavzusini yozing:")


@router.message(StateFilter(SlideOrderStates.waiting_for_topic))
async def slayd_mavzu_qabul(message: Message, state: FSMContext):
    topic = message.text.strip() if message.text else ""
    if not topic:
        await message.answer("❗ Iltimos, matn ko'rinishida mavzu yozing.")
        return

    user = message.from_user
    await db.add_slide_order(
        topic=topic,
        user_id=user.id,
        username=f"@{user.username}" if user.username else None,
        full_name=user.full_name,
    )
    await state.clear()
    await message.answer(
        "✅ Buyurtmangiz qabul qilindi! Tez orada siz bilan bog'lanishadi.",
        reply_markup=main_menu(),
    )
