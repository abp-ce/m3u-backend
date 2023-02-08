from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models


async def get_user_by_name(session: AsyncSession, username: str):
    result = await session.scalars(select(
        models.M3UUser
    ).where(
        models.M3UUser.username == username
    ))
    return result.first()


async def create_user(session: AsyncSession, user: models.M3UUser):
    session.add(user)
    await session.commit()
