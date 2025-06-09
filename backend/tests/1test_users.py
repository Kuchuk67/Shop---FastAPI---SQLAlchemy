from tests.conftest import TestClient, from_db
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


#pytestmark = pytest.mark.asyncio(loop_scope="module")

def dtest_check_auth(client: TestClient):
    response = client.get("/api/v1/users")
    assert response.status_code == 401

    response = client.get("/api/v1/users/list")
    assert response.status_code == 401

    response = client.get("/api/v1/users/id-1")
    assert response.status_code == 401


async def stest_get_db(client: TestClient):

    engine = create_async_engine("postgresql+asyncpg://postgres:54321@localhost:5432/test_shop", echo=True)
    Session = async_sessionmaker(bind=engine, expire_on_commit=False)
    async with engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.drop_all)
        except:
            ...
        await conn.run_sync(Base.metadata.create_all)
    
    #Session.close_all
    
        #return
        #yield


def test_user_registration(client: TestClient):

    response = client.post("/api/v1/registration",
                           json={
                                "full_name": "string",
                                "email": "user@example.com",
                                "phone": "+70349184258",
                                "password": "string"
                                }
                            )
    print("***********************",response.json)
    assert response.status_code == 201



def test_user_login(client: TestClient):
    response = client.post("/api/v1/login",
                           json={
                                "login": "user@example.com",
                                 "password": "string"
                                }
                           )
 
    assert literal_eval(response.content.decode('utf-8'))["token_type"] == "bearer"



async def ltest_drop_db(client: TestClient):

    engine = create_async_engine("postgresql+asyncpg://postgres:54321@localhost:5432/test_shop", echo=True)
    Session = async_sessionmaker(bind=engine, expire_on_commit=False)

    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


