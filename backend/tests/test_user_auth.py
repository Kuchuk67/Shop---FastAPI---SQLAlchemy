import pytest
from httpx import ASGITransport, AsyncClient
from main import app
from fastapi import FastAPI
from app.core.models import db_helper
from app.core.models import Base
from contextlib import asynccontextmanager
from ast import literal_eval


async def override_get_async_session():
    async with db_helper.session_factory() as session:
        yield session


pytestmark = pytest.mark.asyncio(loop_scope="session")


async def test_auth():
    """ проверка не авторизированого доступа"""

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
        response = await ac.get("/api/v1/users/")
        assert response.status_code == 401
        response = await ac.get("/api/v1/users/list/")
        assert response.status_code == 401
        response = await ac.get("/api/v1/users/id-3/")
        assert response.status_code == 401
        response = await ac.get("/api/v1/users/")
        assert response.status_code == 401


async def test_registration():
    """ Тест регистрацияя пользователя"""
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://localhost:8000"
    ) as ac:
        response = await ac.post("/api/v1/registration/",
                                 json={
                                     "full_name": "string",
                                     "email": "user@example.com",
                                     "phone": "+70349184258",
                                     "password": "string"
                                 }
                                 )
        assert response.status_code == 201


async def test_user_login_email():
    """
    Тест авторизации пользователя по логину
    """
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://localhost:8000"
    ) as ac:
        response = await ac.post("/api/v1/login/",
                                 json={
                                     "login": "user@example.com",
                                     "password": "string"
                                 }
                                 )
        assert literal_eval(response.content.decode('utf-8'))["token_type"] == "bearer"


async def test_user_login_phone():
    """
    Тест авторизации пользователя по телефону
    """
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://localhost:8000"
    ) as ac:
        response = await ac.post("/api/v1/login/",
                                 json={
                                     "login": "+70349184258",
                                     "password": "string"
                                 }
                                 )
        assert literal_eval(response.content.decode('utf-8'))["token_type"] == "bearer"


async def test_registration_not_email():
    """ 
    Тест регистрации с невалидным емайлом
    """
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://localhost:8000"
    ) as ac:
        response = await ac.post("/api/v1/registration/",
                                 json={
                                     "full_name": "string",
                                     "email": "user@examplecom",
                                     "phone": "+70349522211",
                                     "password": "string"
                                 }
                                 )
        assert response.status_code == 422


async def test_registration_not_phone1():
    """ 
    Тест регистрации с невалидным телефоном
    """
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://localhost:8000"
    ) as ac:
        response = await ac.post("/api/v1/registration/",
                                 json={
                                     "full_name": "string",
                                     "email": "user@example.com",
                                     "phone": "70349522211",
                                     "password": "string"
                                 }
                                 )
        assert response.status_code == 422
        response = await ac.post("/api/v1/registration/",
                                 json={
                                     "full_name": "string",
                                     "email": "user@example.com",
                                     "phone": "+7900333221",
                                     "password": "string"
                                 }
                                 )
        assert response.status_code == 422
        response = await ac.post("/api/v1/registration/",
                                 json={
                                     "full_name": "string",
                                     "email": "user@example.com",
                                     "phone": "+7 900 333 2121",
                                     "password": "string"
                                 }
                                 )
        assert response.status_code == 422


async def test_duble_email():
    """ 
    Тест на дублирование емайла
    """
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://localhost:8000"
    ) as ac:
        response = await ac.post("/api/v1/registration/",
                                 json={
                                     "full_name": "string",
                                     "email": "user@example.com",
                                     "phone": "+70349184251",
                                     "password": "string"
                                 }
                                 )
        assert response.status_code == 202


async def test_duble_phone():
    """ 
    Тест на дублирование телефона
    """
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://localhost:8000"
    ) as ac:
        response = await ac.post("/api/v1/registration/",
                                 json={
                                     "full_name": "string",
                                     "email": "user1@example.com",
                                     "phone": "+70349184258",
                                     "password": "string"
                                 }
                                 )
        assert response.status_code == 202
