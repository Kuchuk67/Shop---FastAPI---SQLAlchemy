from fastapi import APIRouter, Depends, Request
from app.shopcase.schemas import ProductShopGet 

from sqlalchemy.ext.asyncio import AsyncSession
from config import setting
from app.core.models import db_helper, User as UserDB
from app.users.rbac import PermissionRole
from fastapi.responses import JSONResponse

# Добавляем префикс
router = APIRouter(prefix=f"{setting.api_prefix}/products", tags=["Product"])


@router.get("/", response_model=list[ProductShopGet])
#@PermissionRole(["user"])
async def products_list(
    session: AsyncSession = Depends(db_helper.session_dependency),
    #current_user: UserGet = Depends(get_current_user)
) -> list[ProductShopGet]:
    """
    Выводит список товаров
    """
    return await crud.products(session=session)

