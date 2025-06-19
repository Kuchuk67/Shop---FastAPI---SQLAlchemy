import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from main import app
from fastapi import FastAPI
from app.core.models import db_helper
from contextlib import asynccontextmanager

pytest_plugins = 'pytest_asyncio'
pytestmark = pytest.mark.asyncio


@pytest.fixture
def users_all():
    return b'[{"full_name":"administrator","email":"admin@example.com","phone":"+79012345678","disabled":false,"roles":"admin","id":1},{"full_name":"string","email":"user@example.com","phone":"+79012345679","disabled":false,"roles":"user","id":2}]'


@pytest.fixture
def users_one():
    return b'{"id":1,"full_name":"administrator","email":"admin@example.com","phone":"+79012345678","roles":"admin"}'


@pytest.fixture
def users_one_2():
    return b'{"full_name":"string","email":"user@example.com","phone":"+79012345679","disabled":false,"roles":"user","id":2}'


@pytest.fixture
def users_one_3():
    return b'{"full_name":"string","email":"user@example.com","phone":"+79012345679","disabled":true,"roles":"admin","id":2}'


pytestmark = pytest.mark.asyncio(loop_scope="session")


async def override_get_async_session():
    async with db_helper.session_factory() as session:
        yield session


@pytest.fixture
async def users_products():
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        async with db_helper.engine.begin() as conn:
            app.dependency_overrides[db_helper.scoped_session_dependency] = override_get_async_session
            yield

    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://localhost:8000"
    ) as ac, lifespan(app):
        login_data = {
            "login": "admin@example.com",
            "password": "pSSdsd343#ads"
        }
        response = await ac.post("/api/v1/login/", json=login_data)
        assert response.status_code == 200
        token = response.json()["access_token"]
        header = {"Authorization": f"Bearer {token}"}

        prod_data = {
            "name": "string",
            "description": "string",
            "price": 0,
            "quantity": 0,
            "is_active": True
        }

        response = await ac.post("/api/v1/products/add/", json=prod_data, headers=header)
        assert response.status_code == 200
        return prod_data


@pytest_asyncio.fixture
async def ttt():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://localhost:8000"
    ) as ac:
        login_data = {
            "login": "user@example.com",
            "password": "pass"
        }

        response = await ac.post("/api/v1/login/", json=login_data)
        assert response.status_code == 200
    token = response.json()["access_token"]
    return token
