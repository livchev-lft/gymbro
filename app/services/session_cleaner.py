# services/session_cleaner.py

import asyncio
import datetime
from app.models.user import SessionToken
from app.core.redis_client import redis_client
from app.core.db import AsyncSessionLocal

CHECK_INTERVAL = 60 * 5  # Проверяем каждые 5 минут

async def clean_expired_sessions():
    while True:
        async with AsyncSessionLocal() as db:
            now = datetime.datetime.now(datetime.timezone.utc)
            expired_sessions = db.query(SessionToken).filter(
                SessionToken.expires_at < now,
                SessionToken.is_active == True
            ).all()

            for session in expired_sessions:
                # Удаляем ключ refresh token из Redis
                await redis_client.delete(f"refresh:{session.session_id}:*")

                # Деактивируем сессию в БД
                session.is_active = False
                print(f"🗑️ Expired session removed: {session.session_id} for user {session.user_id}")

            db.commit()
        await asyncio.sleep(CHECK_INTERVAL)
