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


async def override_get_async_session():
    async with db_helper.session_factory() as session:
        yield session


pytestmark = pytest.mark.asyncio(loop_scope="session")


@pytest.mark.asyncio(loop_scope="session")
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
        response = await ac.get("/api/v1/products/id-1/")
        assert response.status_code == 401
        response = await ac.patch("/api/v1/products/id-1/")
        assert response.status_code == 401
        response = await ac.post("/api/v1/products/add/")
        assert response.status_code == 401


@pytest.mark.asyncio(loop_scope="session")
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
        async_session = db_helper.session_factory
        async with async_session() as session:
            user = await session.get(UserDB, 1)
            user.roles = "admin"  # type: ignore
            await session.commit()


@pytest_asyncio.fixture(loop_scope="session")
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


@pytest.mark.asyncio(loop_scope="session")
async def test_product_add(token_auth_admin):
    """
    Добавление товаров
    """

    header = {"Authorization": f"Bearer {token_auth_admin}"}
    # rex = f"{await users_products}"
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://localhost:8000"
    ) as ac:
        for x in range(1, 15):
            prod_data = {
                "name": f"Товар {x}",
                "description": f"Описание: {x}, подробное описание товара и его свойств",
                "price": x * 1000,
                "quantity": x,
                "is_active": True
            }
            response = await ac.post("/api/v1/products/add/", json=prod_data, headers=header)
            assert response.status_code == 201


@pytest.mark.asyncio(loop_scope="session")
async def test_products(token_auth_admin):
    """
    Вывод списка товаров
    """
    header = {"Authorization": f"Bearer {token_auth_admin}"}
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://localhost:8000"
    ) as ac:
        response = await ac.get("/api/v1/products/?page=0&limit=5", headers=header)
        assert response.status_code == 200
        data = json.loads(response.content)
        assert len(data) == 5


@pytest.mark.asyncio(loop_scope="session")
async def test_products_id(token_auth_admin):
    """
    Вывод товара по ID
    """
    header = {"Authorization": f"Bearer {token_auth_admin}"}
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://localhost:8000"
    ) as ac:
        response = await ac.get("/api/v1/products/id-1/", headers=header)
        assert response.status_code == 200


@pytest.mark.asyncio(loop_scope="session")
async def test_products_patch(token_auth_admin):
    """
    Редактирование товара
    """
    header = {"Authorization": f"Bearer {token_auth_admin}"}
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://localhost:8000"
    ) as ac:
        data = {
            "quantity": 100,
            "is_active": False,
            "price": 100
        }
        response = await ac.patch("/api/v1/products/id-1/", json=data, headers=header)
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["price"] == 100
        assert data["is_active"] == False
        assert data["quantity"] == 100


@pytest.mark.asyncio(loop_scope="session")
async def test_products_delete(token_auth_admin):
    """
    Удаление товара
    """
    header = {"Authorization": f"Bearer {token_auth_admin}"}
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://localhost:8000"
    ) as ac:
        response = await ac.patch("/api/v1/products/id-1/delete/", headers=header)
        assert response.status_code == 200
        response = await ac.get("/api/v1/products/?page=0&limit=100", headers=header)
        assert response.status_code == 200
        data = json.loads(response.content)
        assert len(data) == 14
