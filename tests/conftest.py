import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, init_db
import aiosqlite
import asyncio


@pytest.fixture(scope="function")
async def db_cleanup():
    """Создаёт временную БД в памяти и переопределяет get_db для тестов."""
    # Создаём in-memory БД
    conn = await aiosqlite.connect(":memory:")
    await conn.execute('''
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
    await conn.commit()

    # Функция-заглушка для get_db, возвращающая наше соединение
    async def override_get_db():
        yield conn

    # Переопределяем зависимость в приложении
    app.dependency_overrides[get_db] = override_get_db

    yield conn

    # Чистим после теста
    await conn.close()
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def client(db_cleanup):
    """Клиент FastAPI с чистой БД для каждого теста."""
    return TestClient(app)
