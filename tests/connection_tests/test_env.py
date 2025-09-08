from app.core.config import get_settings


def test_env_loaded():
    s = get_settings()
    assert s.DATABASE_URL is not None
    assert s.REDIS_URL is not None
    assert s.SECRET_KEY is not None