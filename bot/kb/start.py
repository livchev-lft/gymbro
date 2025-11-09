from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, KeyboardButton

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Начать тренировку"),
        KeyboardButton(text="Статистика")],
        [KeyboardButton(text="Мои тренировки"),
        KeyboardButton(text="Вес")],
        [KeyboardButton(text="Достижения"),
        KeyboardButton(text="Настройки")],
    ],
    resize_keyboard=True
)