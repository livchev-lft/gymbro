from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import UserHint, default_hints


async def check_and_show_hint(user_id: int, section: str, session: AsyncSession) -> bool:
    result = await session.execute(
        select(UserHint).where(UserHint.user_id == user_id)  # type: ignore
    )
    user_hint = result.scalar_one_or_none()

    if not user_hint:
        user_hint = UserHint(user_id=user_id, hints=default_hints())
        session.add(user_hint)
        await session.commit()
        await session.refresh(user_hint)

    hint_value = user_hint.hints.get(section, False)

    # Если ещё не показывалось — ставим True
    if not hint_value:
        user_hint.hints[section] = True
        await session.commit()

    return hint_value