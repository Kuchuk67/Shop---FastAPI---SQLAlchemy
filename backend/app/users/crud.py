from fastapi import APIRouter, Request, Depends, HTTPException, status
from app.users.schemas import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.models import User
from sqlalchemy import select
from sqlalchemy.engine import Result

from app.core.models import db_helper, User as UserDB


async def get_users() -> list[UserDB]:
    """
    Выводит всех пользователей
    """
    session: AsyncSession = Depends(db_helper.session_dependency)
    stmt=select(User)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    if users is not None:
        return list(users)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND
    )


async def get_user(user_id) -> [UserDB]:
    """
    Выводит пользователя по ID
    """
    session: AsyncSession = Depends(db_helper.session_dependency)
    user = await session.get(UserDB, user_id)
    if user is not None:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND
    )


async def create_user():
    """
    Создает нового пользователя
    """
    session: AsyncSession = Depends(db_helper.session_dependency)

