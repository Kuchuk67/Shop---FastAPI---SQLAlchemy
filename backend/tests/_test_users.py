import asyncio
from ast import literal_eval
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.core.models import Base, db_helper
from main import app


# @pytest.mark.asyncio
async def _test_app_2(create_2):
    x = f"{await create_2}"
    assert x == "1"


# Additional `asyncio` annotation on fixture
@pytest_asyncio.fixture
async def create_2():
    return 1


@pytest.fixture
def unawaited_fixture():
    async def inner_fixture():
        return 1

    return inner_fixture()


def test_foo(unawaited_fixture):
    assert 1 == asyncio.run(unawaited_fixture)
