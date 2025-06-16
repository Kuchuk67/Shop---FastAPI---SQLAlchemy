import pytest
import pytest_asyncio
from typing import Any, AsyncGenerator
from httpx import ASGITransport, AsyncClient
from asgi_lifespan import LifespanManager
from main import app
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from app.core.models import db_helper, User as UserDB
from app.core.models import Base
import asyncio
from contextlib import asynccontextmanager
from ast import literal_eval 
from sqlalchemy.ext.asyncio import AsyncSession

from .fixture import users_all, users_one, users_one_2, users_one_3


async def override_get_async_session():
    async with db_helper.session_factory() as session:
        yield session

pytestmark = pytest.mark.asyncio(loop_scope="session")





async def test_auth():
    """ 
    очистка БД и новое создание таблиц
    Проверка запрета доступа
    """
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


async def test_create_admin(session: AsyncSession = Depends(db_helper.session_dependency)):
    """ Создание пользователя admin"""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost:8000"
    ) as ac:
        response = await ac.post("/api/v1/registration/",
                           json={
                                "full_name": "administrator",
                                "email": "admin@example.com",
                                "phone": "+79012345678",
                                "password": "pSSdsd343#ads"
                                })
        assert response.status_code == 201
        async_session =  db_helper.session_factory
        async with async_session() as session:
                user = await session.get(UserDB, 1)
                user.roles = "admin" # type: ignore
                await session.commit()


@pytest_asyncio.fixture
async def token_auth_user():
    """
    фикстура получает токен доступа 
    для user для создания заголовка
    """
    async with AsyncClient(
                        transport=ASGITransport(app=app),
                        base_url="http://localhost:8000"
                        ) as ac:
        login_data = {
        "login": "user@example.com",
        "password": "pSSdsd343#ads"
    }
        response = await ac.post("/api/v1/login/", json=login_data)
        assert response.status_code == 200
    token = response.json()["access_token"]
    return token


@pytest_asyncio.fixture
async def token_auth_admin():
    """
    фикстура получает токен доступа 
    для user для создания заголовка
    """
    async with AsyncClient(
                        transport=ASGITransport(app=app),
                        base_url="http://localhost:8000"
                        ) as ac:
        login_data = {
        "login": "admin@example.com",
        "password": "pSSdsd343#ads"
    }
        response = await ac.post("/api/v1/login/", json=login_data)
        assert response.status_code == 200
    token = response.json()["access_token"]
    return token


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
                                "password": "pSSdsd343#ads"
                                })
    assert response.status_code == 201



async def test_user_list(token_auth_admin, users_all):
    """
    вывод всех пользователей
    """
    header = {"Authorization": f"Bearer {await token_auth_admin}"}
    async with AsyncClient(
                        transport=ASGITransport(app=app),
                        base_url="http://localhost:8000"
                        ) as ac:
        response = await ac.get("/api/v1/users/list/", headers=header)
        assert response.status_code == 200
        assert response.content == users_all
        
       
async def test_user_profile(token_auth_admin, users_one):
    """
    вывод текущего пользователя
    """
    header = {"Authorization": f"Bearer {await token_auth_admin}"}
    async with AsyncClient(
                        transport=ASGITransport(app=app),
                        base_url="http://localhost:8000"
                        ) as ac:
        response = await ac.get("/api/v1/users/", headers=header)
        assert response.status_code == 200
        assert response.content == users_one


async def test_user_id(token_auth_admin, users_one_2):
    """
    вывод пользователя по ID
    """
    header = {"Authorization": f"Bearer {await token_auth_admin}"}
    async with AsyncClient(
                        transport=ASGITransport(app=app),
                        base_url="http://localhost:8000"
                        ) as ac:
        response = await ac.get("/api/v1/users/id-2/", headers=header)
        assert response.status_code == 200
        assert response.content == users_one_2


async def test_user_patch(token_auth_admin, users_one_3):
    """
    деактивация пользователя
    """
    header = {"Authorization": f"Bearer {await token_auth_admin}"}
    async with AsyncClient(
                        transport=ASGITransport(app=app),
                        base_url="http://localhost:8000"
                        ) as ac:
        data = {
            "disabled": True,
            "roles": "admin"
        }
        response = await ac.patch("/api/v1/users/id-2/patch/", json=data, headers=header)
        assert response.status_code == 200
        assert response.content == users_one_3


async def test_user_del(token_auth_admin):
    """
    деактивация пользователя
    """
    header = {"Authorization": f"Bearer {await token_auth_admin}"}
    async with AsyncClient(
                        transport=ASGITransport(app=app),
                        base_url="http://localhost:8000"
                        ) as ac:
        data = {
            "disabled": True,
            "roles": "admin"
        }
        response = await ac.post("/api/v1/users/id-2/delete/", headers=header)
        assert response.status_code == 200

        data = response.content
        assert data.decode('utf-8') == '{"detail":"Пользователь удален"}'


