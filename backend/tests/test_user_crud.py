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


async def test_create_user_1():
    """ Создание пользователя admin"""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost:8000"
    ) as ac:
        response = await ac.get("/api/v1/users/")
    assert response.status_code == 200


async def test_create_user():
    """ Создание пользователя"""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost:8000"
    ) as ac:
        response = await ac.get("/api/v1/users/")
    assert response.status_code == 200


async def test_auth():
    """ Проверка наличия аутентификации"""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost:8000"
    ) as ac:
        response = await ac.get("/api/v1/users/id-1/")
        assert response.status_code == 401
        response = await ac.patch("/api/v1/users/id-1/patch/")
        assert response.status_code == 401
        response = await ac.post("/api/v1/users/id-1/delete/")
        assert response.status_code == 401



async def test_login():
    """ Логинемся админом пользователя"""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost:8000"
    ) as ac:
        response = await ac.get("/api/v1/users/")
    assert response.status_code == 200


