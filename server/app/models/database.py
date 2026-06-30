import aiosqlite
from contextlib import asynccontextmanager

DB_PATH = "whisper_tools.db"


async def get_db() -> aiosqlite.Connection:
    db = await aiosqlite.connect(DB_PATH)
    db.row_factory = aiosqlite.Row
    await _init_tables(db)
    return db


async def _init_tables(db: aiosqlite.Connection):
    await db.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            filename TEXT NOT NULL,
            original_name TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            transcript TEXT,
            corrected_text TEXT,
            summary TEXT,
            report TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
        )
    """)
    await db.commit()
