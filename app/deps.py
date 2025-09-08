from typing import AsyncGenerator
from app.core.db import AsyncSessionLocal

async def get_db() -> AsyncGenerator[AsyncSessionLocal, None]:
    async with AsyncSessionLocal() as session:
        yield session
