from fastapi import HTTPException, status
from app.shopcase.schemas import ProductShop, ProductShopGet, ProductShopPut
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.models.shop import ProductShop as ProductShopDB
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.sql import text
from datetime import datetime
import json
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from main import app
from fastapi import FastAPI, Depends
from app.core.models import db_helper, User as UserDB
from app.core.models import Base
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession


async def data_test(session: AsyncSession, product):

    #for x in range(1, 15):
        
    session.add(product)

    await session.commit()



async def data_test1(session: AsyncSession = Depends(db_helper.session_dependency)):
    product = ProductShop(
            name = f"Товар {x}",   
            description = 
            f"Описание: {x}, подробное описание товара и его свойств",
            price = x * 1000,
            quantity = x,
            is_active = True )
    await data_test(session, product)
