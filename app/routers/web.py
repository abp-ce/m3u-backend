import os
import urllib
from datetime import datetime
from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ..crud.populate_epg_db import populate_epg_db
from ..crud.programmes import get_programme_by_name
from ..dependencies.auth import get_current_active_user
from ..dependencies.session import get_session
from ..schemas.auth import User
from ..schemas.web import PersonalList, ProgrammeResponse
from ..utils.M3U import M3U

router = APIRouter()


@router.get("/{p_name}/{dt}", response_model=ProgrammeResponse | None)
async def details(p_name: str, dt: datetime,
                  session: AsyncSession = Depends(get_session)):
    prog = await get_programme_by_name(session, p_name, dt)
    if prog:
        ret = ProgrammeResponse.from_orm(prog)
        ret.disp_name = p_name
        return ret
    return prog


@router.get("/load/")
def load(url: str | None = None):
    if url:
        with urllib.request.urlopen(url) as f:
            lines = f.readlines()
        m3u = M3U(lines)
        return m3u.get_dict_arr()
    return {'message': 'Empty URL'}


@router.post("/save", response_class=FileResponse)
async def save(
    pers_list: List[PersonalList],
    current_user: User = Depends(get_current_active_user)
):
    with open(f'../files/{current_user.username}.txt', 'w') as f:
        f.write("#EXTM3U\n")
        for ch in pers_list:
            f.write(f'#EXTINF:-1 ,{ch.title}\n')
            f.write(f'{ch.value}\n')
    return f'../files/{current_user.username}.txt'


@router.get('/load_personal')
async def load_personal(current_user: User = Depends(get_current_active_user)):
    if not os.path.exists(f'../files/{current_user.username}.txt'):
        return []
    with open(f'../files/{current_user.username}.txt', 'r') as f:
        lines = f.readlines()
    m3u = M3U(lines)
    return m3u.get_dict_arr()


@router.get('/refresh_epg_db')
def refresh_epg_db(background_tasks: BackgroundTasks,
                   session: AsyncSession = Depends(get_session)):
    background_tasks.add_task(populate_epg_db, session)
    return {"message": "Refreshing EPG db in the background"}
