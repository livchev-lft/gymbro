import pytest
import sqlalchemy
from config import get_settings
import redis
from fastapi.testclient import TestClient
from app.main import app

def test_postgres_connection():
    settings = get_settings()
    engine = sqlalchemy.create_engine(settings.DATABASE_URL)
    try:
        with engine.connect() as conn:
            result = conn.execute(sqlalchemy.text("SELECT 1"))
            assert result.scalar() == 1
    finally:
        engine.dispose()

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