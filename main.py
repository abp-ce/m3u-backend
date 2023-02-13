from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, telebot, web

app = FastAPI()

app.include_router(web.router)
app.include_router(auth.router)
app.include_router(telebot.router)

origins = [
    'http://localhost:8080',
    'https://abp-m3u.ml',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
