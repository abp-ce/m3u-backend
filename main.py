from fastapi import BackgroundTasks, Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_session
from app.populate_epg_db import populate_epg_db
from app.routers import telebot

app = FastAPI()

app.include_router(telebot.router)


@app.get('/refresh_epg_db')
def refresh_epg_db(background_tasks: BackgroundTasks,
                   session: AsyncSession = Depends(get_session)):
    background_tasks.add_task(populate_epg_db, session)
    return {"message": "Refreshing EPG db in the background"}
