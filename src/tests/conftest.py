from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
import pytest
from httpx import AsyncClient, ASGITransport
from shopAPI.server import app
from shopAPI.database import get_session, engine, async_session_factory


@pytest.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        base_url="http://testserver/api/v1/",
        transport=ASGITransport(app),
        follow_redirects=True,
    ) as ac:
        yield ac


@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with engine.begin() as conn:
        session = async_session_factory()
        app.dependency_overrides[get_session] = lambda: session
        yield session
        await session.close()
        await conn.rollback()
    await engine.dispose()


@pytest.fixture(scope="function")
async def client_payload() -> dict:
    return {
        "client_name": "test_name",
        "client_surname": "test_surname",
        "birthday": "2000-01-01",
        "gender": "M",
        "address": {
            "country": "test_country",
            "city": "test_city",
            "street": "test_street",
        },
    }
