import pytest
import pytest_asyncio
from typing import Any, AsyncGenerator
from httpx import ASGITransport, AsyncClient
from asgi_lifespan import LifespanManager
from main import app
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.models import db_helper
from app.core.models import Base
import asyncio
from contextlib import asynccontextmanager

async def override_get_async_session():
    async with db_helper.session_factory() as session:
        yield session


pytestmark = pytest.mark.asyncio(loop_scope="module")

#@pytest.mark.anyncio
async def test_root():
    """ Простой тест без обращений к БД"""
    '''@asynccontextmanager
    async def lifespan(app: FastAPI):
        async with db_helper.engine.begin() as conn:
            app.dependency_overrides[db_helper.scoped_session_dependency] = override_get_async_session
            yield'''


    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost:8000"
    ) as ac:
        response = await ac.get("/api/v1/users")
    assert response.status_code == 200



#@pytest.mark.anyncio
async def test_root2():
    """ Простой тест без обращений к БД"""
    
    '''@asynccontextmanager
    async def lifespan(app: FastAPI):
        async with db_helper.engine.begin() as conn:
            app.dependency_overrides[db_helper.scoped_session_dependency] = override_get_async_session
            yield'''


    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost:8000"
    ) as ac:
        response = await ac.get("/api/v1/users")
    assert response.status_code == 200