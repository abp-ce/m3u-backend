from datetime import timedelta

from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import ACCESS_TOKEN_EXPIRE_MINUTES
from ..crud import auth as crud
from ..dependencies.session import get_session
from ..models import M3UUser
from ..schemas.auth import Token
from ..utils.auth import (authenticate_user, create_access_token,
                          get_password_hash)

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.post("/register", response_model=Token)
async def register_for_access_token(
    username=Form(),
    email=Form(default=None),
    password=Form(),
    session: AsyncSession = Depends(get_session)
):
    result = await crud.get_user_by_name(session=session, username=username)
    if result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Username {result.username} already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = {'username': username, 'password': get_password_hash(password)}
    if email:
        user['email'] = email
    # user.password = get_password_hash(user.password)
    await crud.create_user(session=session, user=M3UUser(**user))
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token)


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_dt: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session)
):
    user = await authenticate_user(form_dt.username, form_dt.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token)
