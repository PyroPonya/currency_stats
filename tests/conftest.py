import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
import aiosqlite
from contextlib import asynccontextmanager


@pytest.fixture(scope="function")
async def db_cleanup():
    """Создаёт временную БД в памяти с таблицей и подменяет get_db."""
    # Создаём in-memory БД
    conn = await aiosqlite.connect(":memory:")
    # Создаём таблицу
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

    # Функция для переопределения зависимости get_db
    @asynccontextmanager
    async def override_get_db():
        yield conn

    # Переопределяем
    app.dependency_overrides[get_db] = override_get_db

    yield conn

    # Чистим
    await conn.close()
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def client(db_cleanup):
    """Клиент FastAPI с чистой БД для каждого теста."""
    return TestClient(app)
