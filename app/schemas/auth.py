from datetime import datetime

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = 'Bearer'


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: EmailStr | None = None
    password: str
    creation_date: datetime
    disabled: str

    class Config:
        orm_mode = True
