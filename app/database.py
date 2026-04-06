import aiosqlite
from contextlib import asynccontextmanager

DATABASE_URL = "currency_stats.db"


async def init_db():
    async with aiosqlite.connect(DATABASE_URL) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS rate_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                usd REAL,
                eur REAL,
                gbp REAL,
                jpy REAL,
                chf REAL
            )
        ''')
        await db.commit()


@asynccontextmanager
async def get_db():
    async with aiosqlite.connect(DATABASE_URL) as db:
        db.row_factory = aiosqlite.Row
        yield db
