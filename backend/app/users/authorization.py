from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.responses import JSONResponse
from .security import verify_password, create_jwt_token, get_user_from_token_refresh,get_user_from_token
from app.core.models import User as UserDB
from config import setting
from fastapi import Depends, HTTPException, status
import jwt

async def login_user(user_in, session: AsyncSession):
    """
    Авторизация пользователя
    """
    if "@" in user_in.login:
        statement = select(UserDB).where(UserDB.email == user_in.login)
    else:
        # user_in.login = user_in.login[2:]
        statement = select(UserDB).where(UserDB.phone == user_in.login)
    result = await session.execute(statement)
    users = result.scalars().first()
    if users:
        # Если нашли пользователя с таким логином
        # сравниваем пароли
        # print(user_in.password, users.password)
        if verify_password(user_in.password, users.password):
            ...
            # Если проверка прошла успешно, генерируем токен для пользователя
            token = create_jwt_token(
                {"sub": str(users.id)}, setting.ACCESS_TOKEN_EXPIRE_MINUTES
            )  # "sub" — это subject, в нашем случае имя пользователя
            token_refresh = create_jwt_token(
                {"iss": str(users.id)}, setting.FRESH_TOKEN_EXPIRE_MINUTES
            )
            return {
                "access_token": token,
                "token_type": "bearer",
                "refresh_token": token_refresh,
            }
        return users
    # Ошибка пары логин-пароль
    return JSONResponse(
        content={"detail": "Error in login-password pair"}, status_code=401
    )

from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def refresh_token(current_userid: int):

    # Проверяем токен и извлекаем утверждение о пользователе.
    # Создаем новую пару токенов
    token = create_jwt_token(
                {"sub": str(current_userid)}, setting.ACCESS_TOKEN_EXPIRE_MINUTES
            )  # "sub" — это subject, в нашем случае имя пользователя
    token_refresh = create_jwt_token(
                {"iss": str(current_userid)}, setting.FRESH_TOKEN_EXPIRE_MINUTES
            )
    return {
                "access_token": token,
                "token_type": "bearer",
                "refresh_token": token_refresh,
            } 
