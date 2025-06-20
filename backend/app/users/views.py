from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import User as UserDB
from app.core.models import db_helper
from app.users import authorization, crud
from app.users.authorization import refresh_token_create
from app.users.rbac import PermissionRole
from app.users.schemas import (LoginUser,
                               UserCreate,
                               UserGet,
                               UserPatch)
from app.users.security import (
    get_current_user,
    get_password_hash,
    get_user_from_refresh_token,
    validate_pass
)
from config import setting
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login")

# Добавляем префикс
router = APIRouter(prefix=f"{setting.api_prefix}/users",
                   tags=["Users"]
                   )
router_authentication = APIRouter(prefix=f"{setting.api_prefix}",
                                  tags=["Users_Authen"]
                                  )


@router.get("/list/", response_model=list[UserGet])
@PermissionRole(["admin"])
async def get_users_list(
        session: AsyncSession = Depends(db_helper.session_dependency),
        current_user: UserGet = Depends(get_current_user),
) -> list[UserDB]:
    """
    Выводит список пользователей
    """
    return await crud.get_users(session=session)


@router.get("/", response_model=list[UserGet])
@PermissionRole(["admin", "user"])
async def get_users(current_user: UserGet = Depends(get_current_user)):
    """
    Выводит данные текущего пользователя
    """
    return JSONResponse(
        content={
            "id": current_user.id,
            "full_name": current_user.full_name,
            "email": current_user.email,
            "phone": current_user.phone,
            "roles": current_user.roles,
        },
        status_code=200,
    )


@router.get("/id-{user_id}/", response_model=UserGet)
@PermissionRole(["admin"])
async def get_user(
        user_id: int,
        session: AsyncSession = Depends(db_helper.session_dependency),
        current_user: UserGet = Depends(get_current_user),
) -> UserDB:
    """
    Выводит данные текущего пользователя
    """
    return await crud.get_user(user_id, session=session)


@router.patch("/id-{user_id}/patch/",
              response_model=UserGet
              )
@PermissionRole(["admin"])
async def user_disable(
        user_id: int,
        user_patch_data: UserPatch,
        session: AsyncSession = Depends(db_helper.session_dependency
                                        ),
        current_user: UserGet = Depends(get_current_user),
):
    """
    Вносит изменения в сущнось пользователя.
    Отключает пользователя.
    Меняет роль.
    """
    return await crud.patch_user(user_id,
                                 user_patch_data,
                                 session=session
                                 )


@router.delete("/id-{user_id}/delete/")
@PermissionRole(["admin"])
async def user_delete(
        user_id: int,
        session: AsyncSession = Depends(db_helper.session_dependency),
        current_user: UserGet = Depends(get_current_user),
):
    """
    Удалит пользователя совсем
    """
    return await crud.user_delete(user_id, session=session)


@router_authentication.post("/registration/",
                            status_code=201
                            )
async def create_user(
        user_in: UserCreate,
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    """
    Принимем POST запрос на создание пользователя
    по схеме UserCreate
    """
    # Валидация пароля
    if not validate_pass(user_in.password):
        return JSONResponse(
            content={"detail": "The password is too simple"},
            status_code=422
        )
    if user_in.password != user_in.password2:
        return JSONResponse(
            content={"detail": "The passwords do not match"},
            status_code=422
        )

    user_in.password = get_password_hash(user_in.password)
    # Передаем запрос в круд на создание пользователя
    return await crud.create_user(user_in=user_in, session=session)


@router_authentication.post("/login/")
async def login_user(
        # user_in: LoginUser,
        user_in: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    """
    проверяет учетные данные пользователя
    и возвращает JWT токен, если данные правильные.\n
    login: email пользователя или телефон +7..........
    """
    return await authorization.login_user(user_in=user_in, session=session)


@router_authentication.post("/refresh-token/")
async def refresh_token(
        current_user: UserGet = Depends(get_user_from_refresh_token)
):
    """
    возвращает JWT токен..........
    """
    return await refresh_token_create(current_user)
