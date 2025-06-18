from fastapi import APIRouter, Depends
from app.shopcase.schemas import ProductShopGet, ProductShop, CartBase, CartGet, ProductShopPut
from app.users.schemas import UserGet
from app.shopcase import crud_shop, crud_cart
from app.users.security import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from config import setting
from app.core.models import db_helper
from app.core.models.shop import ProductShop as ProductShopDB, Cart as CartDB
from app.users.rbac import PermissionRole

# Добавляем префикс
router_shop = APIRouter(prefix=f"{setting.api_prefix}/products", tags=["Product"])
router_cart = APIRouter(prefix=f"{setting.api_prefix}/cart", tags=["Cart"])


@router_shop.get("/", response_model=list[ProductShopGet])
async def products_get_list(
        page: int = 1, limit: int = 10,
        session: AsyncSession = Depends(db_helper.session_dependency),
) -> list[ProductShopDB]:
    """
    Выводит список товаров
    """
    return await crud_shop.products_get_list(session=session, page=page, limit=limit)


@router_shop.get("/id-{product_id}/", response_model=ProductShopGet)
@PermissionRole(["user"])
async def products_list(
        product_id: int,
        session: AsyncSession = Depends(db_helper.session_dependency),
        current_user: UserGet = Depends(get_current_user)
) -> ProductShopDB:
    """
    Выводит один продукт по ID
    """
    return await crud_shop.products_get(session=session,
                                        id=product_id)


@router_shop.post("/add/", status_code=201)
@PermissionRole(["admin"])
async def products_add(
        product_in: ProductShop,
        session: AsyncSession = Depends(db_helper.session_dependency),
        current_user: UserGet = Depends(get_current_user)
) -> ProductShopGet:
    """
    Добавляет продукт
    """
    return await crud_shop.products_add(session=session,
                                        product_in=product_in
                                        )


@router_shop.patch("/id-{product_id}/", response_model=ProductShopGet)
@PermissionRole(["user"])
async def products_edit(
        product_id: int,
        product_in: ProductShopPut,
        session: AsyncSession = Depends(db_helper.session_dependency),
        current_user: UserGet = Depends(get_current_user)
) -> ProductShopDB | None:
    """
    Редактирует продукт
    """
    return await crud_shop.products_edit(session=session,
                                         product_id=product_id,
                                         product_in=product_in)


@router_shop.patch("/id-{product_id}/delete/", response_model=ProductShopGet)
@PermissionRole(["admin"])
async def products_delete(
        product_id: int,
        session: AsyncSession = Depends(db_helper.session_dependency),
        current_user: UserGet = Depends(get_current_user)
) -> ProductShopDB:
    """
    Удаляет продукт (обнуляет количество)
    """
    return await crud_shop.products_delete(session=session,
                                           product_id=product_id)


# Корзина router_cart /cart

@router_cart.get("/", response_model=list[CartGet])
@PermissionRole(["user"])
async def cart_get_list(
        session: AsyncSession = Depends(db_helper.session_dependency),
        current_user: UserGet = Depends(get_current_user)
) -> list[CartDB]:
    """
    Выводит товары в корзине
    """
    return await crud_cart.cart_get_list(session=session,
                                         current_user=current_user)


@router_cart.post("/add/", response_model=CartGet, status_code=201)
@PermissionRole(["user"])
async def cart_add(
        product_in: CartBase,
        session: AsyncSession = Depends(db_helper.session_dependency),
        current_user: UserGet = Depends(get_current_user)
):
    """
    Добавляет товар в корзину
    """
    return await crud_cart.cart_add(session=session,
                                    current_user=current_user,
                                    product_in=product_in,
                                    )


@router_cart.patch("/", response_model=CartGet)
@PermissionRole(["user"])
async def cart_patch_quantity(
        product_in: CartBase,
        session: AsyncSession = Depends(db_helper.session_dependency),
        current_user: UserGet = Depends(get_current_user)
) -> CartDB | None:
    """
    Изменяет количество товара в корзине
    """

    return await crud_cart.cart_patch_quantity(session=session,
                                               current_user=current_user,
                                               product_in=product_in,
                                               )


@router_cart.delete("/remove_all/", response_model=list[CartGet])
@PermissionRole(["user"])
async def cart_remove_all(
        session: AsyncSession = Depends(db_helper.session_dependency),
        current_user: UserGet = Depends(get_current_user)
):
    """
    Очищает корзину
    """
    return await crud_cart.cart_remove_all(session=session,
                                           current_user=current_user,
                                           )
