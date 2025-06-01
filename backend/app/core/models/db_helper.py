from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)

from config import setting


class DatabaseHelper:
    def __init__(self):
        # создаем движок подключения
        self.engine = create_async_engine(
            url=setting.db_url,
            echo=setting.DEBAG,
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

db_helper = DatabaseHelper()      