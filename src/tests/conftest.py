import pytest
from httpx import AsyncClient, ASGITransport
from shopAPI.server import app


@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(
        base_url="http://testserver/api/v1/",
        transport=ASGITransport(app),
        follow_redirects=True,
    ) as ac:
        yield ac
