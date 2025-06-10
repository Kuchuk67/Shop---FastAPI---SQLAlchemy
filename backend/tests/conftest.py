'''import pytest_asyncio
from httpx import AsyncGenerator


@pytest_asyncio.fixture(scope='session', autouse=True)
async def test_app() -> AsyncGenerator[LifespanManager, Any]:
    app.dependency_overrides[db_connection.session_geter] = override_get_async_session

    async with LifespanManager(app) as manager:
        yield manager.app'''