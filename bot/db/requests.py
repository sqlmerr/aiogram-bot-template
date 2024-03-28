from typing import Optional

from sqlalchemy import select, insert
from .models import User
from .core import session_maker


async def get_user(user_id: int) -> Optional[User]:
    statement = select(User).where(User.user_id == user_id)
    async with session_maker() as session:
        result = await session.execute(statement)

    return result.scalar_one_or_none()


async def create_user(user_id: int) -> None:
    statement = insert(User).values(user_id=user_id)
    async with session_maker() as session:
        await session.execute(statement)
        await session.commit()
