from fastapi import APIRouter, Request, Depends, HTTPException, status
from app.users.schemas import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.models import User
from sqlalchemy import select
from sqlalchemy.engine import Result
from fastapi.responses import JSONResponse

from app.core.models import db_helper, User as UserDB


async def get_users(session: AsyncSession) -> list[UserDB]:
    """
    Выводит всех пользователей
    """

    stmt=select(User)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    if users is not None:
        return list(users)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND
    )


async def get_user(user_id, session: AsyncSession) -> [UserDB]:
    """
    Выводит пользователя по ID
    """

    user = await session.get(User, user_id)
    if user is not None:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND
    )


async def create_user(user_in, session: AsyncSession):
    """
    Создает нового пользователя
    """
    # Нужна проверка на наличие похожих email и телефона в БД
    user_in.phone = user_in.phone[2:]
    statement = select(UserDB).where((UserDB.email == user_in.email) | (UserDB.phone == user_in.phone))
    result = await session.execute(statement)
    users = result.scalars().first()

    # Создаем нового пользователя
    if not users:
        user = UserDB(**user_in.model_dump())
        session.add(user)
        await session.commit()
        return user

    # Если дублирование, то статус 202
    if users.email == user_in.email:
        return JSONResponse(
            content={"detail": "Such user exists", "email": user_in.email},
            status_code=202
        )
    if users.phone == user_in.phone:
        return JSONResponse(
            content={"detail": "Such user exists", "phone": user_in.phone},
            status_code=202
        )
    return JSONResponse(
        content={"detail": "Such user exists"},
        status_code=202
    )


