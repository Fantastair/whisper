import aiosqlite

from windows.config import settings


async def get_db() -> aiosqlite.Connection:
    """获取数据库连接，自动初始化表结构。"""
    db = await aiosqlite.connect(settings.db_path)
    db.row_factory = aiosqlite.Row
    await _init_tables(db)
    return db


async def _init_tables(db: aiosqlite.Connection) -> None:
    """初始化数据库表结构。"""
    await db.executescript("""
        CREATE TABLE IF NOT EXISTS tasks (
            id              TEXT PRIMARY KEY,
            filename        TEXT NOT NULL,
            original_name   TEXT NOT NULL,
            file_type       TEXT NOT NULL DEFAULT 'audio',
            status          TEXT NOT NULL DEFAULT 'pending',
            transcript      TEXT,
            corrected_text  TEXT,
            summary         TEXT,
            report          TEXT,
            email_sent      INTEGER DEFAULT 0,
            created_at      TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
            updated_at      TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
            file_size       INTEGER,
            audio_duration  REAL,
            error_message   TEXT
        )
    """)
    await db.commit()
