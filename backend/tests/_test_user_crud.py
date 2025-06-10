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
from ast import literal_eval 

async def override_get_async_session():
    async with db_helper.session_factory() as session:
        yield session

pytestmark = pytest.mark.asyncio(loop_scope="module")



async def test_auth():
    """ Проверка наличия аутентификации"""
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        async with db_helper.engine.begin() as conn:
            app.dependency_overrides[db_helper.scoped_session_dependency] = override_get_async_session
            
            try:
                await conn.run_sync(Base.metadata.drop_all)
            except:
                ...
            await conn.run_sync(Base.metadata.create_all)
            yield


    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost:8000"
    ) as ac, lifespan(app):
        response = await ac.get("/api/v1/users/id-1/")
        assert response.status_code == 401
        response = await ac.patch("/api/v1/users/id-1/patch/")
        assert response.status_code == 401
        response = await ac.post("/api/v1/users/id-1/delete/")
        assert response.status_code == 401


async def test_create_user_1():
    """ Создание пользователя admin"""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost:8000"
    ) as ac:
        response = await ac.post("/api/v1/registration/",
                           json={
                                "full_name": "administrator",
                                "email": "admin@example.com",
                                "phone": "+79012345678",
                                "password": "pass"
                                })
    assert response.status_code == 201


async def test_create_user():
    """ Создание пользователя"""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost:8000"
    ) as ac:
        response = await ac.post("/api/v1/registration/",
                           json={
                                "full_name": "string",
                                "email": "user@example.com",
                                "phone": "+79012345679",
                                "password": "pass"
                                })
    assert response.status_code == 201


async def test_login():
    """ Логинемся админом пользователя"""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost:8000"
    ) as ac:
        response = await ac.post("/api/v1/login/",
                           json={
                                "login": "+79012345678",
                                "password": "pass"
                                })
    print("*************************")
    print(literal_eval(response.content.decode('utf-8'))["token_type"])
    print(literal_eval(response.content.decode('utf-8'))["access_token"])
    print(literal_eval(response.content.decode('utf-8'))["refresh_token"])
    #token.access_token = literal_eval(response.content.decode('utf-8'))["access_token"]
    assert response.status_code == 200



