from app.core.redis_client import redis_client
import redis

REFRESH_TOKEN_EXPIRE = 30 * 24 * 60 * 60  # 30 дней


async def store_refresh_token(redis: redis.Redis, token: str, session_id: str):
    key = f"refresh:{session_id}:{token}"
    await redis.set(key, "1", ex=REFRESH_TOKEN_EXPIRE)


async def is_refresh_token_valid(token: str, session_id: str) -> bool:
    key = f"refresh:{session_id}:{token}"
    return await redis_client.exists(key) == 1

async def delete_refresh_token(token: str, session_id: str):
    key = f"refresh:{session_id}:{token}"
    await redis_client.delete(key)
