from fastapi import APIRouter, Request, Depends, HTTPException, status
# from app.users.schemas import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.models import User
from sqlalchemy import select
from sqlalchemy.engine import Result
from fastapi.responses import JSONResponse
from app.users.security import get_password_hash, get_current_user
from app.core.models import db_helper, User as UserDB
from app.users.schemas import LoginUser, UserGet
from config import setting

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


async def get_user_current(session: AsyncSession,
                           current_user: UserGet 
                           ):
    """
    Выводит текущего пользователя
    """
    #stmt=select(User)
    #result: Result = await session.execute(stmt)
    #users = result.scalars().all()
    if UserGet is not None:
        return UserGet
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND
    )


async def get_user(user_id, session: AsyncSession) -> UserDB:
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
    statement = select(UserDB).where(
        (UserDB.email == user_in.email) | (UserDB.phone == user_in.phone)
        )
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


'''async def disable_user(user_in, disable, session: AsyncSession):
    """
    Отключает пользователя
    """
    # получаем пользователя по id
    user = await session.get(UserDB, user_in)
    # если не найден, отправляем статусный код и сообщение об ошибке
    if not user: 
        return JSONResponse(status_code=404, content={ "message": "Пользователь не найден"})

    # если пользователь найден, изменяем его данные и отправляем обратно клиенту
    if disable:
        user.disabled = True
    else:
        user.disabled = False
    await session.commit() # сохраняем изменения 
    await session.refresh(user)
    return user

async def user_roles(user_in, role,  session: AsyncSession):
    """
    Изменяет роль пользователя
    """
    # получаем пользователя по id
    user = await session.get(UserDB, user_in)
    # если не найден, отправляем статусный код и сообщение об ошибке
    if not user: 
        return JSONResponse(status_code=404, content={ "message": "Пользователь не найден"})

    # если пользователь найден, изменяем его данные и отправляем обратно клиенту
    if role in setting.role:
        user.roles = role
    else:
        return JSONResponse(status_code=422, content={ "message": "Такая роль не существует"})
    await session.commit() # сохраняем изменения 
    await session.refresh(user)
    return user'''


async def patch_user(user_in, user_patch_data, session: AsyncSession):
    """
    Patch пользователя
    """
    # получаем пользователя по id
    user = await session.get(UserDB, user_in)
    # если не найден, отправляем статусный код и сообщение об ошибке
    if not user:
        return JSONResponse(status_code=404, content={"detail": "Пользователь не найден"})
    # если пользователь найден, изменяем его данные и отправляем обратно клиенту
    # меняем роль
    if user_patch_data.roles in setting.role:
        user.roles = user_patch_data.roles
    elif not user_patch_data.roles:
        pass
    else:
        return JSONResponse(status_code=422, content={ "detail": "Такая роль не существует"})
    # меняем активность пользователя
    if user_patch_data.disabled:
        user.disabled = user_patch_data.disabled

    # Сохраняем
    await session.commit()
    await session.refresh(user)
    return user

async def user_delete(user_in, session: AsyncSession):
    """
    Удаляет пользователя
    """
    # получаем пользователя по id
    user = await session.get(UserDB, user_in)
    # если не найден, отправляем статусный код и сообщение об ошибке
    if not user:
        return JSONResponse(status_code=404, content={"detail": "Пользователь не найден"})
    # Удаляем
    await session.delete(user)
    await session.commit()
    return JSONResponse(status_code=200, content={"detail": "Пользователь удален"})