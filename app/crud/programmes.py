from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models


async def get_categories(session: AsyncSession):
    result = await session.execute(select(models.Programme.cat).distinct())
    return result.all()


async def get_by_cat(session: AsyncSession, cat: str, tm: datetime):
    tcat = None if cat == 'Пусто' else cat
    result = await session.execute(select(
        models.Channel.ch_id,
        models.Channel.disp_name
    ).join(models.Programme).where(
        models.Programme.pstart <= tm,
        models.Programme.pstop > tm,
        models.Programme.cat == tcat
    ))
    return result.all()


async def get_programme(session: AsyncSession, ch_id: str, tm: datetime):
    result = await session.execute(select(
        models.Programme,
        models.Channel.disp_name
    ).join(models.Channel).where(
        models.Programme.pstart <= tm,
        models.Programme.pstop > tm,
        models.Channel.ch_id == ch_id
    ))
    return result.first()


async def get_programme_by_name(session: AsyncSession, p_name: str,
                                tm: datetime):
    result = await session.scalars(select(
        models.Programme
    ).join(models.Channel).where(
        models.Programme.pstart <= tm,
        models.Programme.pstop > tm,
        models.Channel.disp_name == p_name
    ))
    return result.first()


async def get_by_letters(session: AsyncSession, pat: str):
    pat_l = pat.lower()
    result = await session.execute(select(
        models.Channel.ch_id,
        models.Channel.disp_name
    ).where(
        models.Channel.disp_name.ilike(f'%{pat_l}%')
    ))
    return result.all()
