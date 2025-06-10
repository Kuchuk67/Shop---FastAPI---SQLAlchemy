
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
from ast import literal_eval 
import pytest
from httpx import ASGITransport, AsyncClient
from main import app
import pytest_asyncio  
import pytest 


async def test_user_1():

    async with AsyncClient(
                        transport=ASGITransport(app=app),
                        base_url="http://localhost:8000"
                        ) as ac:
        print(type(ac))
        response = await ac.get("/api/v1/users/id-1/")
        assert response.status_code == 401






@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
                        transport=ASGITransport(app=app),
                        base_url="http://localhost:8000"
                        ) as ac:
        yield ac

@pytest.mark.asyncio
async def test_user_2(client):
        print(type(client))
        
        response = await client.get("/api/v1/users/id-1/")
        assert response.status_code == 401
        client.close()
            

