# Ish Berish / Ish Olish Telegram Bot

Mijoz (ish beruvchi) va ijrochi (ish izlovchi)ni bog'lovchi Telegram bot.

## Qanday ishlaydi

- **💼 Ish berish** — bosgan foydalanuvchiga admin nickname'i ko'rsatiladi. U admin bilan
  bog'lanib, o'z ishini joylashtirish uchun ma'lumot beradi.
- **🔍 Ish olish** / **📋 Ishlar** — mavjud ishlar ro'yxati va har birining ish beruvchi
  nickname'i ko'rsatiladi.
- **📰 Yangiliklar** — admin qo'shgan yangiliklar ro'yxati.
- **🎨 Slayd buyurtma** — bosgan foydalanuvchidan "Slayd mavzusini yozing" deb so'raladi,
  u mavzuni yozadi va bu buyurtma (mavzu + kimdan kelgani) bazaga saqlanadi. Admin
  `/slaydlar` orqali barcha buyurtmalarni ko'radi.

Barcha ish e'lonlarini faqat **admin** qo'sha oladi (`/addwork`) — oddiy foydalanuvchilar
to'g'ridan-to'g'ri e'lon joylay olmaydi, bu adminni "moderator" rolida ushlab turadi.

## O'rnatish

1. Python 3.10+ o'rnatilgan bo'lishi kerak.
2. Kutubxonalarni o'rnating:
   ```bash
   pip install -r requirements.txt
   ```
3. `.env.example` faylini `.env` nomiga ko'chiring va to'ldiring:
   ```bash
   cp .env.example .env
   ```
   - `BOT_TOKEN` — @BotFather orqali yaratilgan bot tokeni
   - `ADMIN_IDS` — sizning Telegram user ID'ingiz (bir nechta bo'lsa vergul bilan ajrating).
     ID'ni bilish uchun @userinfobot ga `/start` yozing.
4. Botni ishga tushiring:
   ```bash
   python main.py
   ```

## Admin buyruqlari

| Buyruq | Tavsif |
|---|---|
| `/addwork Tavsif \| @nickname` | Yangi ish e'loni qo'shish |
| `/addnickname @nickname` | "Ish berish" bosilganda chiqadigan admin nickname'ini o'rnatish |
| `/addnews Matn` | Yangilik qo'shish |
| `/listwork` | Barcha ishlar ro'yxati (ID bilan) |
| `/delwork ID` | ID bo'yicha ishni o'chirish |
| `/slaydlar` | Slayd buyurtmalari ro'yxati (mavzu + kimdan kelgani) |
| `/help_admin` | Buyruqlar ro'yxatini ko'rish |

### Misol

```
/addnickname @admin_kontakt
/addwork Frontend dasturchi kerak, remote, 3 oy | @acme_company
```

Bunda "Ish olish" bosgan foydalanuvchi quyidagini ko'radi:

```
📋 Mavjud ishlar:

🔹 Frontend dasturchi kerak, remote, 3 oy
👤 Bog'lanish: @acme_company
```

## Ma'lumotlar bazasi

Ishlar, yangiliklar va sozlamalar `ish_bot.db` (SQLite) faylida saqlanadi — u avtomatik
yaratiladi, alohida sozlash shart emas.

## Kengaytirish g'oyalari

- Inline tugmalar bilan har bir ishga alohida "Bog'lanish" tugmasi qo'shish
- Ish kategoriyalari (masalan: IT, qurilish, dizayn) bo'yicha filtrlash
- Ish izlovchilar ham anketa to'ldirib, adminga yuborishi (ikki tomonlama)
- Bir nechta admin uchun har birining o'z nickname'i
