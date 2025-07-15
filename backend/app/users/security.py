import re
from datetime import UTC, datetime, timedelta
from typing import Dict

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import db_helper
from app.core.models.users import User as UserDB
from config import setting

"""
Здесь функции хеширования паролей,
создания и расшифровки токенов,
функция получения текущего пользователя.
"""

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def validate_pass(password: str) -> bool:
    """
    Проверка уровня сложности пароля
    """
    if re.fullmatch(
        r"(?=^.{8,}$)((?=.*\d)(?=.*\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$",
        password
    ):
        return True
    return False


def get_password_hash(password: str) -> str:
    """
    Функция для создания хэша пароля:
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Функция для проверки пароля
    """
    return pwd_context.verify(plain_password, hashed_password)


# OAuth2PasswordBearer извлекает токен
# из заголовка "Authorization: Bearer <token>"
# Параметр tokenUrl указывает маршрут,
# по которому клиенты смогут получить токен

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"api/v1/login")


# Функция для создания JWT токена с заданным временем жизни
def create_jwt_token(data: Dict, expires_delta: int):
    """
    Функция для создания JWT токена. Мы копируем входные данные,
    добавляем время истечения и кодируем токен.
    """
    to_encode = data.copy()

    # expire time of the token
    expire = datetime.now(UTC) + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,
                             setting.SECRET_KEY,
                             algorithm=setting.ALGORITHM
                             )

    # return the generated token
    return encoded_jwt


# Функция для получения пользователя из токена
def get_user_from_token(
    token: str = Depends(oauth2_scheme), refresh: bool = False
) -> int | None:
    """
    Функция для извлечения информации о пользователе из токена.
    Проверяем токен и извлекаем утверждение о пользователе.
    """
    try:
        payload = jwt.decode(token,
                             setting.SECRET_KEY,
                             algorithms=[setting.ALGORITHM]
                             )
        # Декодируем токен с помощью секретного ключа

    # Возвращаем утверждение о пользователе (subject) из полезной нагрузки
    except jwt.ExpiredSignatureError:
        pass  # Обработка ошибки истечения срока действия токена
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token is invalid"
            )
    else:
        try:
            user_id: int = int(payload.get("sub"))
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User not found"
                )
        else:
            return user_id


async def get_user(user_id: int,
                   session: AsyncSession
                   ) -> UserDB:
    """
    Получаем пользователя по ID
    """
    user = await session.get(UserDB, user_id)


    if user is not None:
        if not user.disabled:
            return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail="User not found"
                        )


async def get_current_user(
    current_userid: int = Depends(get_user_from_token),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> UserDB:
    """
    Получаем текущего пользователя (из токена) по ID из бд
    """

    user = await get_user(current_userid, session=session)
    if user is not None:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User not found"
        )


def get_user_from_refresh_token(
        token: str = Depends(oauth2_scheme)
        ) -> int | None:
    """
    Функция для извлечения информации о пользователе из refresh-токена.
    """
    try:
        payload = jwt.decode(token, setting.SECRET_KEY,
                             algorithms=[setting.ALGORITHM]
                             )
        # Декодируем токен с помощью секретного ключа

    # Возвращаем утверждение о пользователе (subject) из полезной нагрузки
    except jwt.ExpiredSignatureError:
        pass  # Обработка ошибки истечения срока действия токена
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Token is invalid"
        )
    else:
        try:
            user_id: int = int(payload.get("iss"))
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="User not found"
            )
        else:
            return user_id
