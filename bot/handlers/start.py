from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.decorators.hint_decorator import with_hint
from bot.kb.start import start_kb

start_router = Router()

@start_router.message(CommandStart())
@with_hint("start")
async def start_handler(message: Message, **kwargs):
    await message.answer(f"Добро пожаловать!\n"
                         f"Я твой личный помощник для тренировок"
                         f"Выбери действие кнопками снизу:\n",
                         reply_markup=start_kb
                         )