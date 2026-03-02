import asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from main import app
from config import settings
from app.db.database import get_async_session
from app.db.base import Base

# --- 1. Движок базы (Используем NullPool) ---
test_engine = create_async_engine(settings.TEST_DATABASE_URL, poolclass=NullPool)


# --- 2. Создание таблиц без Alembic (самый надежный путь для тестов) ---
@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    # Создаем таблицы перед началом всех тестов
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield  # Здесь бегут тесты

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# --- 3. Сессия с автоматическим откатом (Isolating tests) ---
@pytest.fixture(scope="function")
async def session():
    async with test_engine.connect() as connection:
        # Начинаем транзакцию
        transaction = await connection.begin()

        # Создаем сессию, привязанную к этому конкретному соединению
        async_session = AsyncSession(
            bind=connection,
            expire_on_commit=False,
        )

        yield async_session

        # Откатываем всё, что сделал тест, чтобы база осталась чистой
        await transaction.rollback()
        await connection.close()


# --- 4. Асинхронный клиент с правильным переопределением ---
@pytest.fixture(scope="function")
async def client(session):
    # FastAPI ожидает генератор, поэтому используем async def
    async def override_get_async_session():
        yield session

    app.dependency_overrides[get_async_session] = override_get_async_session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()
