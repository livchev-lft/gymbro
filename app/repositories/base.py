from sqlalchemy.ext.asyncio import AsyncSession

class BaseRepository:
    def __init__(self, model, db: AsyncSession):
        self.model = model
        self.db = db

    async def add(self, obj):
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj
