from fastapi import FastAPI
from app.endpoints import users, tests, auth
from app.core.redis_client import init_redis, redis_client
from contextlib import asynccontextmanager
import asyncio
from app.services.session_cleaner import clean_expired_sessions


@asynccontextmanager
async def lifespan(_app: FastAPI):
    _app.state.redis = await init_redis()
    print("🚀 App started")
    _app.state.session_cleaner_task = asyncio.create_task(clean_expired_sessions())
    yield
    _app.state.session_cleaner_task.cancel()
    try:
        await _app.state.session_cleaner_task
    except asyncio.CancelledError:
        pass
    await _app.state.redis.close()
    await _app.state.redis.connection_pool.disconnect()
    print("🛑 App stopped")


app = FastAPI(lifespan=lifespan)

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(tests.router, prefix="/tests", tags=["tests"])
app.include_router(auth.router, prefix="/auth", tags=["tests"])
