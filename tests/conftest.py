import pytest
import tempfile
import os
import asyncio
from fastapi.testclient import TestClient
import aiosqlite
import app.database as database   # ← импортируем модуль, а не атрибут app


@pytest.fixture(scope="function")
def client():
    # 1. Создаём временный файл БД
    fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)

    # 2. Подменяем путь к БД в модуле database
    original_url = database.DATABASE_URL
    database.DATABASE_URL = db_path

    # 3. Создаём таблицу в этом временном файле
    async def init_test_db():
        async with aiosqlite.connect(db_path) as db:
            await db.execute('''
                CREATE TABLE rate_requests (
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

    asyncio.run(init_test_db())

    # 4. Импортируем приложение (оно теперь использует подменённый DATABASE_URL)
    from app.main import app

    # 5. Создаём тестового клиента
    yield TestClient(app)

    # 6. Восстанавливаем исходный путь и удаляем временный файл
    database.DATABASE_URL = original_url
    os.unlink(db_path)
