import pytest
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)
from asyncio import current_task

#pytest.fixture
#def db_fixture():
#    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:test_shop@localhost:5432/f1.db"
