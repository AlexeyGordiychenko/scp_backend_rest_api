import pytest
from httpx import AsyncClient, ASGITransport
from shopAPI.server import app
from shopAPI.database import get_session


@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(
        base_url="http://testserver/api/v1/",
        transport=ASGITransport(app),
        follow_redirects=True,
    ) as ac:
        yield ac


@pytest.fixture(scope="function")
async def db_session():
    async for session in get_session():
        yield session
