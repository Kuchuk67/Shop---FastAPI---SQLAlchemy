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
        self.engine = create_async_engine(
            url=setting.db_url,
            echo=setting.DEBAG,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

db_helper = DatabaseHelper()      