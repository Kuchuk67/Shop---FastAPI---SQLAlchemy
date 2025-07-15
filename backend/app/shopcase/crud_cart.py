# CRUD - Корзина
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import select, func
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.models.shop import Cart as CartDB
from app.core.models.shop import ProductShop as ProductShopDB
from app.shopcase.schemas import CartBase
from app.users.schemas import UserGet


async def cart_get_list(session: AsyncSession,
                        current_user: UserGet) -> list[CartDB]:
    """
    Выводит товары в корзине
    """
    stmt = (select(CartDB).filter(CartDB.user_id == current_user.id)
            .options(selectinload(CartDB.products)))
    result: Result = await session.execute(stmt)
    products_in_cart = result.scalars().all()
    # if products_in_cart is not None:
    return list(products_in_cart)
    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


async def cart_add(
    session: AsyncSession,
    current_user: UserGet,
    product_in: CartBase,
):
    """
    Добавляет товар в корзину
    """
    product = await session.get(
        ProductShopDB,
        product_in.product_id,
    )

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        if product.is_active | product.price == 0 | product.quantity == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # Проверяем на наличие в корзине похожего товара

    stmt = (
        select(CartDB)
        .filter(CartDB.user_id == current_user.id)
        .filter(CartDB.product_id == product_in.product_id)
    )
    result: Result = await session.execute(stmt)
    cart = result.scalars().all()

    if not cart:
        # Столько товара нет в наличии
        if product_in.quantity > product.quantity:
            return JSONResponse(
                content={"detail": "So many items are out of stock"},
                status_code=422
            )
        product_in_cart = CartDB(
            user_id=current_user.id,
            product_id=product_in.product_id,
            price=product.price,
            quantity=product_in.quantity,
        )
        session.add(product_in_cart)
        await session.commit()
        return product_in_cart
    else:
        # Товар уже в корзине
        return JSONResponse(
            content={"detail": "The product is already in the cart"},
            status_code=422
        )


async def cart_gelete(session: AsyncSession,
                      current_user: UserGet,
                      cart_id: int):
    """
    Удаляет товар из корзины
    """
    product_in_cart = await session.get(
        CartDB,
        cart_id,
    )
    if product_in_cart:
        if product_in_cart.user_id == current_user.id:
            # удаляем
            await session.delete(product_in_cart)
            await session.commit()
            return JSONResponse(
                content={"detail": "Product removed from cart"},
                status_code=200
            )
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


async def cart_patch_quantity(
    session: AsyncSession, current_user: UserGet, product_in: CartBase
) -> CartDB | None:
    """
    Изменяет количество товара в корзине
    """
    # грузим товар из корзины
    stmt = (
        select(CartDB)
        .filter(CartDB.user_id == current_user.id)
        .filter(CartDB.product_id == product_in.product_id)
    )
    result: Result = await session.execute(stmt)
    product_in_cart = result.scalars().first()
    if product_in_cart:
        # print(product_in_cart.quantity)
        product_in_cart.quantity = product_in.quantity
        await session.commit()
        await session.refresh(product_in_cart)
        return product_in_cart

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


async def cart_remove_all(session: AsyncSession, current_user: UserGet):
    """
    Очищает корзину
    """
    # грузим товар из корзины
    result = await session.execute(
        select(CartDB).where(CartDB.user_id == current_user.id)
    )
    product_in_cart = result.scalars().all()

    if product_in_cart:
        for item in product_in_cart:
            await session.delete(item)
        await session.commit()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content={"detail": "Cart removed"}, status_code=200)


async def cart_sum(session: AsyncSession,
                        current_user: UserGet) -> int:
    """
    Возвращает общую стоимость товаров в корзине пользователя.
    """
    stmt = select(
        func.sum(CartDB.quantity * CartDB.price)
    ).where(CartDB.user_id == current_user.id)

    result: Result = await session.execute(stmt)
    summa = result.scalar()
    if not summa:
        summa = 0
    return summa

    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)