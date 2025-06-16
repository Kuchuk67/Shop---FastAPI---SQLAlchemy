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