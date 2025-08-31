from fastapi import FastAPI
from app.endpoints import users, tests

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(tests.router, prefix="/tests", tags=["tests"])
