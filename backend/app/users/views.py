from fastapi import APIRouter, Depends, Request
from app.users import crud, authorization
from app.users.schemas import LoginUser, UserGet, UserCreate, UserPatch
from app.users.security import get_password_hash, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from config import setting
from app.core.models import db_helper, User as UserDB
from app.users.rbac import PermissionRole
from fastapi.responses import JSONResponse

# Добавляем префикс
router = APIRouter(prefix=f"{setting.api_prefix}/users", tags=["Users"])
router_authentication = APIRouter(prefix=f"{setting.api_prefix}", tags=["Users_Authen"])


@router.get("/list/", response_model=list[UserGet])
@PermissionRole(["admin"])
async def get_users_list(
    session: AsyncSession = Depends(db_helper.session_dependency),
    current_user: UserGet = Depends(get_current_user)
) -> list[UserDB]:
    """
    Выводит список пользователей
    """
    return await crud.get_users(session=session)


@router.get("/", response_model=list[UserGet])
@PermissionRole(["admin", "user"])
async def get_users(
    current_user: UserGet = Depends(get_current_user)
):
    """
    Выводит данные текущего пользователя
    """
    return JSONResponse(
            content={"id": current_user.id,
                     "full_name": current_user.full_name,
                     "email": current_user.email,
                     "phone": current_user.phone,
                     "roles": current_user.roles,
   
                     },
            status_code=200
        )


@router.get("/id-{user_id}/", response_model=UserGet)
@PermissionRole(["admin"])
async def get_user(
    user_id: int, session: AsyncSession = Depends(db_helper.session_dependency),
    current_user: UserGet = Depends(get_current_user)
) -> UserDB:
    """
    Выводит данные текущего пользователя
    """
    return await crud.get_user(user_id, session=session)


@router.patch("/id-{user_id}/patch/", response_model=UserGet)
@PermissionRole(["admin"])
async def user_disable(
    user_id: int, 
    user_patch_data: UserPatch,
    session: AsyncSession = Depends(db_helper.session_dependency),
    current_user: UserGet = Depends(get_current_user)
):
    """
    Вносит изменения в сущнось пользователя.
    Отключает пользователя.
    Меняет роль.
    """
    return await crud.patch_user(user_id, user_patch_data, session=session)


@router.post("/id-{user_id}/delete/")
@PermissionRole(["admin"])
async def user_delete(
    user_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
    current_user: UserGet = Depends(get_current_user)
):
    """
    Удалит пользователя совсем
    """
    return await crud.user_delete(user_id, session=session)

'''
@router.patch("/id-{user_id}/role/{role}/", response_model=UserGet)
#@PermissionRole(["admin"])
async def user_role(
    user_id: int, 
    role: str,
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    """
    меняет роль  пользователя
    """
    return await crud.user_roles(user_id, role, session=session)'''


@router_authentication.post("/registration/", status_code=201)
async def create_user(
    user_in: UserCreate, session: AsyncSession = Depends(db_helper.session_dependency)
):
    """
    Принимем POST запрос на создание пользователя
    по схеме UserCreate
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


@router_authentication.post("/refresh-token/")
async def refresh_token(session: AsyncSession = Depends(db_helper.session_dependency)
):
    """
    проверяет учетные данные пользователя
    и возвращает JWT токен, если данные правильные.\n
    login: email пользователя или телефон +7..........
    """
    return await authorization.refresh_token()