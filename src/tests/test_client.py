import pytest
from httpx import AsyncClient
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from shopAPI.models import Client, ClientResponseWithAddress


@pytest.mark.asyncio
async def test_post_client(client: AsyncClient, db_session: AsyncSession) -> None:
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

    response_json = response.json()
    id = response_json["id"]
    payload["id"] = id
    assert response_json == payload

    client_in_db = (
        await db_session.scalars(
            select(Client).where(Client.id == id).options(joinedload(Client.address))
        )
    ).one_or_none()
    assert client_in_db is not None
    assert (
        ClientResponseWithAddress.model_validate(client_in_db).model_dump(mode="json")
        == payload
    )
