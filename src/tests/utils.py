from datetime import datetime
import random
from typing import List
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlmodel import select

from shopAPI.models import Client, ClientResponseWithAddress


def random_date() -> str:
    start = datetime(1950, 1, 1)
    end = datetime(2000, 1, 1)
    random_date = start + (end - start) * random.random()
    return random_date.strftime("%Y-%m-%d")


async def create_entities(
    client: AsyncClient, path: str, payloads: List[dict]
) -> List[dict]:
    for client_payload in payloads:
        response_create = await client.post(
            path,
            json=client_payload,
        )
        assert response_create.status_code == 201
        response_create_json = response_create.json()
        assert "id" in response_create_json
        client_payload["id"] = response_create_json["id"]
        assert client_payload == response_create_json


async def get_client_from_db(id: str, db_session: AsyncSession):
    return (
        await db_session.scalars(
            select(Client).where(Client.id == id).options(joinedload(Client.address))
        )
    ).one_or_none()


async def compare_db_client_to_payload(client_payload: dict, db_session: AsyncSession):
    db_client = await get_client_from_db(client_payload["id"], db_session)
    assert db_client is not None
    assert (
        ClientResponseWithAddress.model_validate(db_client).model_dump(mode="json")
        == client_payload
    )
