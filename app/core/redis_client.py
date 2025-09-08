import redis.asyncio as redis
from app.core.config import get_settings

settings = get_settings()
redis_client: redis.Redis | None = None

async def init_redis() -> redis.Redis:
    global redis_client
    if not redis_client:
        redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
        try:
            await redis_client.ping()
            print("✅ Redis connected")
        except Exception as e:
            print("❌ Redis connection failed:", e)
            raise e
    return redis_client