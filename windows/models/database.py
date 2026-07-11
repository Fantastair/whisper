import aiosqlite

from windows.config import settings


async def get_db() -> aiosqlite.Connection:
    """获取数据库连接，自动初始化表结构。"""
    db = await aiosqlite.connect(settings.db_path)
    db.row_factory = aiosqlite.Row
    await _init_tables(db)
    return db


async def _init_tables(db: aiosqlite.Connection) -> None:
    """初始化数据库表结构、索引和触发器。"""
    await db.executescript("""
        CREATE TABLE IF NOT EXISTS tasks (
            id              TEXT PRIMARY KEY,
            filename        TEXT NOT NULL,
            original_name   TEXT NOT NULL,
            file_type       TEXT NOT NULL DEFAULT 'audio'
                            CHECK(file_type IN ('audio', 'video')),
            status          TEXT NOT NULL DEFAULT 'pending'
                            CHECK(status IN (
                                'pending', 'syncing', 'extracting',
                                'transcribing', 'correcting', 'summarizing',
                                'completed', 'emailed', 'failed'
                            )),
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
        );

        CREATE INDEX IF NOT EXISTS idx_tasks_status
            ON tasks(status);
        CREATE INDEX IF NOT EXISTS idx_tasks_created
            ON tasks(created_at);

        DROP TRIGGER IF EXISTS trg_tasks_updated;
        CREATE TRIGGER trg_tasks_updated
            AFTER UPDATE ON tasks
        BEGIN
            UPDATE tasks
            SET updated_at = datetime('now', 'localtime')
            WHERE id = NEW.id;
        END;
    """)
    await db.commit()
