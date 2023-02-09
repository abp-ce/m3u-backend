from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..crud import programmes as crud
from ..dependencies.session import get_session

router = APIRouter(
    prefix="/telebot",
    tags=["telebot"]
)


@router.get("/categories/")
async def get_categories(session: AsyncSession = Depends(get_session)):
    return await crud.get_categories(session)


@router.get("/category/{cat}")
async def get_category(cat: str, dt: datetime | None = None,
                       session: AsyncSession = Depends(get_session)):
    if dt is None:
        dt = datetime.now(tz=timezone.utc)
    return await crud.get_by_cat(session, cat, dt)


@router.get("/programme/{ch_id}")
async def get_programme(ch_id: str, dt: datetime | None = None,
                        session: AsyncSession = Depends(get_session)):
    if dt is None:
        dt = datetime.now(tz=timezone.utc)
    return await crud.get_programme(session, ch_id, dt)


@router.get("/letters/{pat}")
async def get_letters(pat: str, session: AsyncSession = Depends(get_session)):
    return await crud.get_by_letters(session, pat)
