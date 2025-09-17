import redis.asyncio

REFRESH_TOKEN_EXPIRE = 30 * 24 * 60 * 60  # 30 дней

class RedisService:
    def __init__(self, client: redis.Redis):
        self.client = client

    async def store_refresh_token(self, token: str, session_id: str):
        key = f"refresh:{session_id}:{token}"
        await self.client.set(key, "1", ex=REFRESH_TOKEN_EXPIRE)

    async def is_refresh_token_valid(self, token: str, session_id: str) -> bool:
        key = f"refresh:{session_id}:{token}"
        return await self.client.exists(key) == 1

    async def delete_refresh_token(self, token: str, session_id: str):
        key = f"refresh:{session_id}:{token}"
        await self.client.delete(key)
