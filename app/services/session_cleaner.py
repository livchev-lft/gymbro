import asyncio
import datetime
from sqlalchemy import select, update
from app.models.user import SessionToken
from app.core.redis_client import redis_client
from app.core.db import AsyncSessionLocal

CHECK_INTERVAL = 60 * 5

async def clean_expired_sessions():
    while True:
        async with AsyncSessionLocal() as db:
            now = datetime.datetime.now(datetime.timezone.utc)
            result = await db.execute(select(SessionToken).where(
                SessionToken.expires_at < now,
                SessionToken.is_active == True
            ))
            expired_sessions = result.scalars().all()

            for session in expired_sessions:
                # Удаляем ключ refresh token из Redis
                keys = await redis_client.keys(f"refresh:{session.session_id}:*")
                if keys:
                    await redis_client.delete(*keys)

                # Деактивируем сессию в БД
                stmt = update(SessionToken).where(SessionToken.id == session.id).values(is_active=False)
                await db.execute(stmt)
                print(f"🗑️ Expired session removed: {session.session_id} for user {session.user_id}")

            await db.commit()
        await asyncio.sleep(CHECK_INTERVAL)
