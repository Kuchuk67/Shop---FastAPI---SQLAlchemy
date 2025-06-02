
from fastapi import APIRouter, Request, Depends, HTTPException, status
from app.users import crud
from app.core.models.db_helper import db_helper
from config import setting
from app.users.schemas import User, LoginUser, UserGet
from app.core.security import get_password_hash, verify_password
from sqlalchemy.ext.asyncio import AsyncSession
from config import setting
from app.core.models import db_helper, User as UserDB

# Добавляем префикс и тег для DOCS
router = APIRouter(prefix=f"{setting.api_prefix}/user", tags=["Users"])
router_authen = APIRouter(prefix=f"{setting.api_prefix}", tags=["Users_Authen"])


@router.get("",response_model=list[UserGet])
async def get_users() -> list[UserDB]:
    return  await crud.get_users()


@router.get("/{user_id}/", response_model=UserGet)
async def get_user(user_id: int) -> [UserDB]:
    return crud.get_user(user_id)


@router.post("")
async def create_user(user: User):
    """ Принимем POST запрос JOSN
    по модели CreateUser
    """
    # Передаем запрос в круд на создание пользователя
    return crud.create_user()

# # Пути аутентификации пользователя
# @router_authen.get("/registration")
# async def registration_form(): 
#     """
#     Этот маршрут выводит форму регистрации пользователя.
#     """
#     return {"message": "выводит форму регистрации пользователя"}

# @router_authen.post("/registration")
# async def registration(user: User): 
#     """
#     Регистрация пользователя.
#     """
#     # хэшируем пароль
#     password = get_password_hash(user.password)
#     # Передаем запрос в круд на создание пользователя
#     return crud.create_user(user_in=user)

    # Сохраняетм данные по пользователю в БД
    # USERS_DATA.append({"username": user.full_name,
    #                    "email": user.email,  
    #                    "password": password,
    #                    "disabled": True,
    #                    "roles": 'user'}
    #                    )
     # В реальной базе данных пароли должны храниться в виде хэшей
    #return {"message": f"регистрация пользователя {password}"}



