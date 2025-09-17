from sqlalchemy import select
from app.models.user import SessionToken, RefreshToken
from app.repositories.base import BaseRepository

class SessionRepository(BaseRepository):
    async def create_session(self, user_id: int):
        import uuid, datetime
        session_id = str(uuid.uuid4())
        session = SessionToken(
            user_id=user_id,
            session_id=session_id,
            expires_at=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=30),
            is_active=True
        )
        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)
        return session

    async def get_active_session(self, session_id: str):
        query = select(SessionToken).where(
            SessionToken.session_id == session_id,
            SessionToken.is_active == True
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_refresh_token(self, token: str, session_id: str):
        query = select(RefreshToken).where(
            RefreshToken.token == token,
            RefreshToken.session_id == session_id,
            RefreshToken.is_active == True
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
