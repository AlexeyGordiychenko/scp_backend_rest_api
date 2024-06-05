from typing import List
import pytest
from httpx import AsyncClient
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from shopAPI.models import Client, ClientResponseWithAddress


@pytest.mark.asyncio
@pytest.mark.parametrize("client_payloads", [1], indirect=True)
async def test_post_client(
    client: AsyncClient, client_payloads: List[dict], db_session: AsyncSession
) -> None:
    client_payload = client_payloads[0]
    print(client_payload)
    response = await client.post(
        "client",
        json=client_payload,
    )
    assert response.status_code == 201

    response_json = response.json()
    assert "id" in response_json
    id = response_json["id"]
    client_payload["id"] = id
    assert response_json == client_payload

    client_in_db = (
        await db_session.scalars(
            select(Client).where(Client.id == id).options(joinedload(Client.address))
        )
    ).one_or_none()
    assert client_in_db is not None
    assert (
        ClientResponseWithAddress.model_validate(client_in_db).model_dump(mode="json")
        == client_payload
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("client_payloads", [1], indirect=True)
async def test_get_client(client: AsyncClient, client_payloads: List[dict]) -> None:
    client_payload = client_payloads[0]
    print(client_payload)
    response_create = await client.post(
        "client",
        json=client_payload,
    )
    assert response_create.status_code == 201
    response_create_json = response_create.json()
    assert "id" in response_create_json

    response_get = await client.get(f"client/{response_create_json['id']}")
    assert response_get.status_code == 200
    assert response_get.json() == response_create_json
