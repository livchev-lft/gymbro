from app.core.db import AsyncSessionLocal
from app.services.hint_service import check_and_show_hint

def with_hint(section: str):
    def decorator(handler):
        async def wrapper(*args, **kwargs):
            message = kwargs.get("message") or args[0]  # достаём message
            user_id = message.from_user.id
            async with AsyncSessionLocal() as session:
                hint_value = await check_and_show_hint(user_id, section, session)

            if not hint_value:
                # Первый раз — показываем подсказку
                await message.answer("💡 Подсказка: как пользоваться этим разделом...")
            else:
                # Уже видел — ничего не показываем, либо другое поведение
                await message.answer("👌 Ты уже знаешь, что делать!")
            return await handler(*args, **kwargs)

        return wrapper

    return decorator