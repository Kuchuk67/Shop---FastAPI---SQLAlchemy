import json
from contextlib import asynccontextmanager
from datetime import datetime

import pytest
import pytest_asyncio
from fastapi import Depends, FastAPI, HTTPException, status
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from app.core.models import Base
from app.core.models import User as UserDB
from app.core.models import db_helper
from app.core.models.shop import ProductShop as ProductShopDB
from app.shopcase.schemas import ProductShop, ProductShopGet, ProductShopPut
from main import app


async def data_test(session: AsyncSession, product):

    # for x in range(1, 15):

    session.add(product)

    await session.commit()


async def data_test1(session: AsyncSession = Depends(db_helper.session_dependency)):
    product = ProductShop(
        name=f"Товар {x}",
        description=f"Описание: {x}, подробное описание товара и его свойств",
        price=x * 1000,
        quantity=x,
        is_active=True,
    )
    await data_test(session, product)
