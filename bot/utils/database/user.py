from typing import Optional, List

from sqlalchemy import insert, select

from database import get_async_session, User


async def get_all_users() -> List[User]:
    async with get_async_session() as session:
        return await session.scalars(select(User))


async def get_user_by_id(user_id: int) -> Optional[User]:
    async with get_async_session() as session:
        return await session.scalar(select(User).where(
            User.id == user_id
        ))


async def create_user(user_id: int,
                      first_name: str,
                      last_name: Optional[str] = None,
                      username: Optional[str] = None) -> None:
    async with get_async_session() as session:
        await session.execute(insert(User).values(
            id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
        ))
        await session.commit()
