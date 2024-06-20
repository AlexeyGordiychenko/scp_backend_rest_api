import random
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, List
import pytest
from httpx import AsyncClient, ASGITransport

from shopAPI.models import Gender
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
            "gender": random.choice(list(Gender)),
            "address": {
                "country": f"test_country_{i}",
                "city": f"test_city_{i}",
                "street": f"test_street_{i}",
            },
        }
        for i in range(request.param)
    ]


@pytest.fixture(scope="function")
def supplier_payloads(request) -> List[dict]:
    return [
        {
            "name": f"test_name_{i}",
            "phone_number": f"+791222{format(random.randint(1, 99998), '05d')}",
            "address": {
                "country": f"test_country_{i}",
                "city": f"test_city_{i}",
                "street": f"test_street_{i}",
            },
        }
        for i in range(request.param)
    ]


@pytest.fixture(scope="function")
def product_payloads(request) -> List[dict]:
    return [
        {
            "name": f"test_name_{i}",
            "category": f"test_category_{i}",
            "price": round(random.uniform(10, 100), 2),
            "available_stock": random.randint(1, 1000),
            "last_update_date": random_date(),
        }
        for i in range(request.param)
    ]
