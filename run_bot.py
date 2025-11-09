import asyncio
import logging
from aiogram import Bot, Dispatcher

from services.config import BOT_TOKEN
from bot.handlers.start import start_router

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start_router)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
