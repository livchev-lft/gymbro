from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, data):
        # Проверяем, есть ли уже юзер
        result = await self.db.execute(select(User).where(User.user_id == data.user_id))
        existing = result.scalars().first()
        if existing:
            return None

        new_user = User(
            user_id=data.user_id,
            username=data.username,
            gender=data.gender,
            birthdate=data.birthdate,
            height=data.height,
            goal=data.goal,
            experience=data.experience,
        )

        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user
