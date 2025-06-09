import pytest
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)
from asyncio import current_task

pytest.fixture
#def db_fixture():
#    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:test_shop@localhost:5432/f1.db"

class DatabaseHelperTest:
    def __init__(self):
        # создаем движок подключения
        self.engine = create_async_engine(
            url="postgresql+asyncpg://postgres:postgres@localhost:5432/test_shop",
            echo=True,
        )
        # создаетсяфабрика сессии
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )
    
    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def session_dependency(self) -> AsyncSession:
        # Открываем сессию
        async with self.session_factory() as session:
            yield session
            await session.close()

    async def scoped_session_dependency(self) -> AsyncSession:
        session = self.get_scoped_session()
        yield session
        await session.close()

db_helper = DatabaseHelperTest()   