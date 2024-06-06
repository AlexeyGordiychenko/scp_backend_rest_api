from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, List
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


@pytest.fixture(scope="function", autouse=True)
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with engine.begin() as conn:
        session = async_session_factory()
        app.dependency_overrides[get_session] = lambda: session
        yield session
        await session.close()
        await conn.rollback()
    await engine.dispose()


@pytest.fixture(scope="function")
def client_payloads(request):
    return [
        {
            "client_name": f"test_name_{i}",
            "client_surname": f"test_surname_{i}",
            "birthday": "2000-01-01",
            "gender": "M",
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
