from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User, UserHint


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user_id):
        result = await self.db.execute(select(User).where(User.user_id == user_id))
        existing = result.scalars().first()
        if existing:
            return None

        new_user = User(
            user_id=user_id
        )

        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)

        user_hint = UserHint(user_id=new_user.user_id)
        self.db.add_all([new_user, user_hint])
        await self.db.commit()
        await self.db.refresh(user_hint)

        return new_user
