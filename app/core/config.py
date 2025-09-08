import os
from functools import lru_cache
from pydantic_settings import BaseSettings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print("Looking for .env at:", os.path.join(BASE_DIR, ".env"))
print("Does .env exist?", os.path.exists(os.path.join(BASE_DIR, ".env")))
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    SECRET_KEY: str
    DEBUG: bool = False

    class Config:
        env_file = os.path.join(BASE_DIR, ".env")
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings():
    return Settings()
