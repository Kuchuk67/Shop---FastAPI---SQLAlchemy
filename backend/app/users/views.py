from fastapi import APIRouter, Depends
from app.users import crud, authorization
from app.users.schemas import LoginUser, UserGet, UserCreate
from app.core.security import get_password_hash
from sqlalchemy.ext.asyncio import AsyncSession
from config import setting
from app.core.models import db_helper, User as UserDB
from app.users.rbac import PermissionRole

# Добавляем префикс
router = APIRouter(prefix=f"{setting.api_prefix}/users", tags=["Users"])
router_authentication = APIRouter(prefix=f"{setting.api_prefix}", tags=["Users_Authen"])


@router.get("/list/", response_model=list[UserGet])
@PermissionRole(["admin"])
async def get_users_list(
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> list[UserDB]:
    # session: AsyncSession = Depends(db_helper.session_dependency)
    return await crud.get_users(session=session)


@router.get("", response_model=list[UserGet])
# @PermissionRole(["admin", "user"])
async def get_users(
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> list[UserDB]:
    # session: AsyncSession = Depends(db_helper.session_dependency)
    return await crud.get_user_current(session=session)


@router.get("/{user_id}/", response_model=UserGet)
@PermissionRole(["admin"])
async def get_user(
    user_id: int, session: AsyncSession = Depends(db_helper.session_dependency)
) -> [UserDB]:
    return await crud.get_user(user_id, session=session)


@router_authentication.post("/registration/", status_code=201)
async def create_user(
    user_in: UserCreate, session: AsyncSession = Depends(db_helper.session_dependency)
):
    """
    Принимем POST запрос по схеме UserCreate
    """
    user_in.password = get_password_hash(user_in.password)
    # Передаем запрос в круд на создание пользователя
    return await crud.create_user(user_in=user_in, session=session)


@router_authentication.post("/login/")
async def login_user(
    user_in: LoginUser, session: AsyncSession = Depends(db_helper.session_dependency)
):
    """
    проверяет учетные данные пользователя
    и возвращает JWT токен, если данные правильные.\n
    login: email пользователя или телефон +7..........
    """
    return await authorization.login_user(user_in=user_in, session=session)


# Пути аутентификации пользователя
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
# return {"message": f"регистрация пользователя {password}"}
