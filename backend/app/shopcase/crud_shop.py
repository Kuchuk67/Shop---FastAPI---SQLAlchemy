# CRUD - витрина продуктов
from fastapi import APIRouter, Request, Depends, HTTPException, status
from app.shopcase.schemas import ProductShop, ProductShopGet, ProductShopPut
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.models.shop import ProductShop as ProductShopDB
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.sql import text
from datetime import datetime, timezone, timedelta
from fastapi.responses import JSONResponse

async def products_get_list(session: AsyncSession, page, limit) -> list[ProductShopDB]:
    """
    Выводит список продуктов
    """
    count = await session.execute(text("SELECT COUNT(*) FROM productshops"))
    count = count.scalars().one()

    offset = (page-1) * limit

    if count % limit == 0:
        total_pages = count / limit
    else:
        total_pages = count // limit + 1


    stmt=select(ProductShopDB).offset(offset).limit(limit)
    result: Result = await session.execute(stmt)
    products = result.scalars().all()
    if products is not None:
        return list(products)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND
    )


async def products_get(session: AsyncSession, 
                       id: int) -> ProductShopDB:
    """
    Выводит один продукт по ID
    """
    product = await session.get(ProductShopDB, id)
    if product is not None:
        return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND
    )


async def products_add(session: AsyncSession, 
                       product_in: ProductShop
                       ) -> ProductShopGet:
    """
    Добавляет продукт
    """
    product = ProductShopDB(**product_in.model_dump())
    session.add(product)
    await session.commit()
    return product # type: ignore


async def products_edit(session: AsyncSession, 
                        product_id: int, 
                        product_in: ProductShopPut
                        ) -> ProductShopDB | None:
    """
    Редактирует продукт
    """
    product = await session.get(ProductShopDB, product_id)
    if product is not None:
        product.updated_at = datetime.now()
        product.quantity = product_in.quantity
        product.is_active = product_in.is_active
        product.price = product_in.price
        await session.commit()
        await session.refresh(product)
        return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND
    )


async def products_delete(session: AsyncSession, product_id: int) -> ProductShopDB:
    """
    Удаляет продукт (обнуляет количество)
    """
    product = await session.get(ProductShopDB, product_id)
    if product is not None:
        product.updated_at = datetime.now()
        product.quantity = 0
        await session.commit()
        await session.refresh(product)
        return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND
    )

    
