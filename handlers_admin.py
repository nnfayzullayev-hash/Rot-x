from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

import database as db
from config import ADMIN_IDS

router = Router()


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


@router.message(Command("help_admin"))
async def help_admin(message: Message):
    if not is_admin(message.from_user.id):
        return
    await message.answer(
        "🛠 <b>Admin buyruqlari:</b>\n\n"
        "<code>/addwork Tavsif | @nickname</code>\n"
        "— Yangi ish e'loni qo'shish (tavsif va ish beruvchi nicknamesi | bilan ajratiladi)\n\n"
        "<code>/addnickname @nickname</code>\n"
        "— \"Ish berish\" bosilganda ko'rsatiladigan admin nickname'ini o'rnatish\n\n"
        "<code>/addnews Matn</code>\n"
        "— Yangilik qo'shish\n\n"
        "<code>/listwork</code>\n"
        "— Barcha ishlar ro'yxati (ID bilan)\n\n"
        "<code>/delwork ID</code>\n"
        "— ID bo'yicha ishni o'chirish\n\n"
        "<code>/slaydlar</code>\n"
        "— Slayd buyurtmalari ro'yxati (mavzu va kimdan kelgani)"
    )


@router.message(Command("addwork"))
async def add_work(message: Message):
    if not is_admin(message.from_user.id):
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2 or "|" not in args[1]:
        await message.answer(
            "❗ Foydalanish: <code>/addwork Ish tavsifi | @ish_beruvchi_nickname</code>\n\n"
            "Masalan:\n<code>/addwork Dizayner kerak, remote | @employer_nick</code>"
        )
        return

    description, nickname = args[1].split("|", maxsplit=1)
    description = description.strip()
    nickname = nickname.strip()

    if not description or not nickname:
        await message.answer("❗ Tavsif va nickname bo'sh bo'lmasligi kerak.")
        return

    job_id = await db.add_job(description, nickname)
    await message.answer(f"✅ Ish qo'shildi (ID: {job_id})")


@router.message(Command("addnickname"))
async def add_nickname(message: Message):
    if not is_admin(message.from_user.id):
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2 or not args[1].strip():
        await message.answer("❗ Foydalanish: <code>/addnickname @nickname</code>")
        return

    nickname = args[1].strip()
    await db.set_setting("admin_nickname", nickname)
    await message.answer(f"✅ Admin nickname o'rnatildi: {nickname}")


@router.message(Command("addnews"))
async def add_news(message: Message):
    if not is_admin(message.from_user.id):
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2 or not args[1].strip():
        await message.answer("❗ Foydalanish: <code>/addnews Yangilik matni</code>")
        return

    await db.add_news(args[1].strip())
    await message.answer("✅ Yangilik qo'shildi")


@router.message(Command("listwork"))
async def list_work(message: Message):
    if not is_admin(message.from_user.id):
        return

    jobs = await db.get_all_jobs()
    if not jobs:
        await message.answer("Hozircha ishlar yo'q.")
        return

    parts = []
    for job in jobs:
        parts.append(f"ID {job['id']}: {job['description']} | {job['employer_nickname']}")
    await message.answer("\n".join(parts))


@router.message(Command("delwork"))
async def del_work(message: Message):
    if not is_admin(message.from_user.id):
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2 or not args[1].strip().isdigit():
        await message.answer("❗ Foydalanish: <code>/delwork ID</code>")
        return

    job_id = int(args[1].strip())
    deleted = await db.delete_job(job_id)
    if deleted:
        await message.answer(f"✅ ID {job_id} o'chirildi")
    else:
        await message.answer(f"❗ ID {job_id} topilmadi")


@router.message(Command("slaydlar"))
async def list_slide_orders(message: Message):
    if not is_admin(message.from_user.id):
        return

    orders = await db.get_all_slide_orders()
    if not orders:
        await message.answer("Hozircha slayd buyurtmalari yo'q.")
        return

    parts = ["🎨 <b>Slayd buyurtmalari:</b>\n"]
    for order in orders:
        sender = order["username"] or f"ID: {order['user_id']}"
        parts.append(
            f"ID {order['id']}\n"
            f"📌 Mavzu: {order['topic']}\n"
            f"👤 Kimdan: {order['full_name']} ({sender})\n"
        )
    await message.answer("\n".join(parts))
