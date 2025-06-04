from fastapi import APIRouter, Request, Depends, HTTPException, status
from app.users.schemas import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.models import User
from sqlalchemy import select
from sqlalchemy.engine import Result
from fastapi.responses import JSONResponse
from .security import verify_password, create_jwt_token
from app.core.models import db_helper, User as UserDB
from config import setting

async def login_user(user_in, session: AsyncSession):
    """
    Авторизация пользователя
    """

    # В реальной практике пароли необходимо сравнивать с хэшами, а не в открытом виде
    # password_h = get_password_hash(user_login.password)
    '''    for user in USERS_DATA:
        if user.get("username") == user_login.username and verify_password(user_login.password, user.get("password")):
            # Если проверка прошла успешно, генерируем токен для пользователя
            token = create_jwt_token({"sub": user_login.username},
                                     ACCESS_TOKEN_EXPIRE_MINUTES)  # "sub" — это subject, в нашем случае имя пользователя
            token_refresh = create_jwt_token({"iss": user_login.username}, FRESH_TOKEN_EXPIRE_MINUTES)
            return {"access_token": token,
                    "token_type": "bearer",
                    "refresh_token": token_refresh}
    # Если данные неверные, возвращаем ошибку
    return {"error": "Ошибка пары пароль-логин"}'''

    if "@" in user_in.login:
        statement = select(UserDB).where(UserDB.email == user_in.login)
    else:
        user_in.login = user_in.login[2:]
        statement = select(UserDB).where(UserDB.phone == user_in.login)
    result = await session.execute(statement)
    users = result.scalars().first()
    if users:
        # Если нашли пользователя с таким логином
        # сравниваем пароли
        #print(user_in.password, users.password)
        if verify_password(user_in.password, users.password):
            ...
            # Если проверка прошла успешно, генерируем токен для пользователя
            token = create_jwt_token({"sub": users.id},
                                     setting.ACCESS_TOKEN_EXPIRE_MINUTES)  # "sub" — это subject, в нашем случае имя пользователя
            token_refresh = create_jwt_token({"iss": users.id}, setting.FRESH_TOKEN_EXPIRE_MINUTES)
            return {"access_token": token,
                    "token_type": "bearer",
                    "refresh_token": token_refresh}
        return users
    # Ошибка пары логин-пароль
    return JSONResponse(
        content={"detail": "Error in login-password pair"},
        status_code=401
    )
