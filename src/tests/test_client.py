from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_post_client(client: AsyncClient) -> None:
    payload = {
        "client_name": "test_name",
        "client_surname": "test_username",
        "birthday": "2000-01-01",
        "gender": "M",
        "address": {
            "country": "test_country",
            "city": "test_city",
            "street": "test_street",
        },
    }
    response = await client.post(
        "client",
        json=payload,
    )
    assert response.status_code == 201
