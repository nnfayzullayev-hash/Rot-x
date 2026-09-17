import aiosqlite
from config import DB_PATH


async def init_db():
    """Bot ishga tushganda jadvallarni yaratadi (agar mavjud bo'lmasa)."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                employer_nickname TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS slide_orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                username TEXT,
                full_name TEXT,
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)
        await db.commit()


# ---------- JOBS ----------

async def add_job(description: str, employer_nickname: str) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "INSERT INTO jobs (description, employer_nickname) VALUES (?, ?)",
            (description, employer_nickname),
        )
        await db.commit()
        return cursor.lastrowid


async def get_all_jobs():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM jobs ORDER BY id DESC")
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]


async def delete_job(job_id: int) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
        await db.commit()
        return cursor.rowcount > 0


# ---------- NEWS ----------

async def add_news(text: str) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("INSERT INTO news (text) VALUES (?)", (text,))
        await db.commit()
        return cursor.lastrowid


async def get_all_news(limit: int = 10):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM news ORDER BY id DESC LIMIT ?", (limit,)
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]


# ---------- SLIDE ORDERS ----------

async def add_slide_order(topic: str, user_id: int, username: str | None, full_name: str) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "INSERT INTO slide_orders (topic, user_id, username, full_name) VALUES (?, ?, ?, ?)",
            (topic, user_id, username, full_name),
        )
        await db.commit()
        return cursor.lastrowid


async def get_all_slide_orders(limit: int = 50):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM slide_orders ORDER BY id DESC LIMIT ?", (limit,)
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]


# ---------- SETTINGS (admin nickname) ----------

async def set_setting(key: str, value: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO settings (key, value) VALUES (?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (key, value),
        )
        await db.commit()


async def get_setting(key: str):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT value FROM settings WHERE key = ?", (key,))
        row = await cursor.fetchone()
        return row["value"] if row else None
