import pytest
from main import app
from httpx import AsyncClient
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"
@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(base_url="http://localhost:8000") as client:
        print("Client is ready")
        yield client


'''from fastapi.testclient import TestClient
from httpx import AsyncClient
from main import app  # Предполагается, что объект app объявлен в my_app/main.py
import pytest
from app.core.models.base import Base
from app.core.models.db_helper import db_helper
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture
async def from_db():
    print("************")
    engine = create_async_engine("postgresql+asyncpg://postgres:54321@localhost:5432/test_shop", echo=True)
    Session = async_sessionmaker(bind=engine, expire_on_commit=False)

    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

@pytest.fixture
def client():
    return TestClient(app)'''


