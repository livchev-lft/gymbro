import asyncio
import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import get_settings
import redis
from fastapi.testclient import TestClient
from main import app

# Асинхронная проверка PostgreSQL
async def check_postgres_connection():
    settings = get_settings()
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    try:
        async with engine.connect() as conn:
            result = await conn.execute(sqlalchemy.text("SELECT 1"))
            assert result.scalar() == 1
    finally:
        await engine.dispose()

# Синхронная обёртка для Pytest
def test_postgres_connection():
    asyncio.run(check_postgres_connection())

def test_redis_connection():
    settings = get_settings()
    client = redis.Redis.from_url(settings.REDIS_URL)
    pong = client.ping()
    assert pong is True

def test_fastapi_healthcheck():
    client = TestClient(app)
    response = client.get("tests/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}