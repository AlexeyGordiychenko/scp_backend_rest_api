from datetime import datetime
import random
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, List
import pytest
from httpx import AsyncClient, ASGITransport
from shopAPI.server import app

import shopAPI.database as database


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
def random_date() -> str:
    start = datetime(1950, 1, 1)
    end = datetime(2000, 1, 1)
    random_date = start + (end - start) * random.random()
    return random_date.strftime("%Y-%m-%d")


@pytest.fixture(scope="function")
def client_payloads(request, random_date) -> List[dict]:
    return [
        {
            "client_name": f"test_name_{i}",
            "client_surname": f"test_surname_{i}",
            "birthday": random_date,
            "gender": random.choice(["M", "F"]),
            "address": {
                "country": f"test_country_{i}",
                "city": f"test_city_{i}",
                "street": f"test_street_{i}",
            },
        }
        for i in range(request.param)
    ]


@pytest.fixture
async def create_clients(client: AsyncClient):
    async def _create_clients(client_payloads: List[dict]) -> List[dict]:
        for client_payload in client_payloads:
            response_create = await client.post(
                "client",
                json=client_payload,
            )
            assert response_create.status_code == 201
            response_create_json = response_create.json()
            assert "id" in response_create_json
            client_payload["id"] = response_create_json["id"]

    return _create_clients
