import uuid
from datetime import datetime, timezone, timedelta

from app.core.security import create_access_token
from app.models import RefreshToken
from app.repositories.session_repo import SessionRepository
from app.services.redis_service import RedisService


class TokenService:
    def __init__(self, db, redis_client):
        self.session_repo = SessionRepository(db)
        self.redis = RedisService(redis_client)

    async def login_user(self, user_id: int):
        now = datetime.now(timezone.utc)
        access_token = create_access_token(user_id)
        refresh_token = str(uuid.uuid4())

        session = await self.session_repo.create_session(user_id)

        await self.redis.store_refresh_token(refresh_token, session.session_id)

        expires_at = now + timedelta(days=30)

        db_refresh = RefreshToken(
            token=refresh_token,
            user_id=user_id,
            session_id=session.session_id,
            created_at=datetime.now(timezone.utc),
            expires_at=expires_at,
            is_active=True
        )

        self.session_repo.db.add(db_refresh)
        await self.session_repo.db.commit()
        await self.session_repo.db.refresh(db_refresh)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "session_id": session.session_id,
            "token_type": "bearer"
        }

    async def refresh_token(self, session_id: str, refresh_token: str):
        if not await self.redis.is_refresh_token_valid(refresh_token, session_id):
            return None

        db_token = await self.session_repo.get_refresh_token(refresh_token, session_id)
        now = datetime.now(timezone.utc)
        if not db_token or not db_token.is_active or db_token.expires_at < now:
            return None

        session = await self.session_repo.get_active_session(session_id)
        if not session:
            return None

        return create_access_token(session.user_id)
