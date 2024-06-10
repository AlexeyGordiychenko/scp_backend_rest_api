import random
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, List
import pytest
from httpx import AsyncClient, ASGITransport
from shopAPI.server import app

import shopAPI.database as database
from tests.utils import random_date


@pytest.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        base_url="http://testserver/api/v1/",
        transport=ASGITransport(app),
        follow_redirects=True,
    ) as ac:
        yield ac


@pytest.fixture(scope="function", autouse=True)
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with database.engine.connect() as connection:
        await connection.begin()
        session = database.prepare_session(connection)
        app.dependency_overrides[database.get_session] = lambda: session
        database.session = session
        yield session
        await session.close()
        await connection.rollback()

    await database.engine.dispose()


@pytest.fixture(scope="function")
def client_payloads(request) -> List[dict]:
    return [
        {
            "client_name": f"test_name_{i}",
            "client_surname": f"test_surname_{i}",
            "birthday": random_date(),
            "gender": random.choice(["M", "F"]),
            "address": {
                "country": f"test_country_{i}",
                "city": f"test_city_{i}",
                "street": f"test_street_{i}",
            },
        }
        for i in range(request.param)
    ]
