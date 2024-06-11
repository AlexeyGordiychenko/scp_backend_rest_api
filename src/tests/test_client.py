from typing import List, Optional
import pytest
from httpx import AsyncClient
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from shopAPI.models import Client, ClientResponseWithAddress
from tests.utils import create_clients, random_date


@pytest.mark.asyncio
@pytest.mark.parametrize("client_payloads", [1, 2], indirect=True)
async def test_post_client(
    client: AsyncClient,
    client_payloads: List[dict],
    db_session: AsyncSession,
) -> None:
    await create_clients(client, client_payloads)
    for client_payload in client_payloads:
        client_in_db = (
            await db_session.scalars(
                select(Client)
                .where(Client.id == client_payload["id"])
                .options(joinedload(Client.address))
            )
        ).one_or_none()
        assert client_in_db is not None
        assert (
            ClientResponseWithAddress.model_validate(client_in_db).model_dump(
                mode="json"
            )
            == client_payload
        )


@pytest.mark.asyncio
@pytest.mark.parametrize("client_payloads", [1, 2], indirect=True)
async def test_get_client(
    client: AsyncClient,
    client_payloads: List[dict],
) -> None:
    await create_clients(client, client_payloads)
    for client_payload in client_payloads:
        response_get = await client.get(f"client/{client_payload['id']}")
        assert response_get.status_code == 200
        assert response_get.json() == client_payload


@pytest.mark.asyncio
@pytest.mark.parametrize("client_payloads", [10, 15], indirect=True)
@pytest.mark.parametrize(
    "params",
    [
        {"limit": 3},
        {"limit": 3, "offset": 4},
        {"offset": 8},
    ],
)
async def test_get_all_clients_pagination(
    client: AsyncClient,
    client_payloads: List[dict],
    params: dict,
) -> None:
    await create_clients(client, client_payloads)
    offset = params.get("offset", 0)
    limit = params.get("limit", len(client_payloads) - offset)
    response_get = await client.get("client/all", params=params)
    assert response_get.status_code == 200
    response_get_json = response_get.json()
    assert len(response_get_json) == limit
    for i, client_payload in enumerate(client_payloads[offset : offset + limit]):
        assert client_payload == response_get_json[i]


@pytest.mark.asyncio
@pytest.mark.parametrize("client_payloads", [1, 2], indirect=True)
@pytest.mark.parametrize(
    "params_template",
    [
        {"name": "client_name"},
        {"surname": "client_surname"},
        {"name": "client_name", "surname": "client_surname"},
    ],
)
async def test_get_all_by_fields(
    client: AsyncClient,
    client_payloads: List[dict],
    params_template: dict,
) -> None:
    await create_clients(client, client_payloads)
    for client_payload in client_payloads:
        params = {key: client_payload[value] for key, value in params_template.items()}
        response_get = await client.get("client/all", params=params)
        assert response_get.status_code == 200
        response_get_json = response_get.json()
        assert len(response_get_json) == 1
        assert response_get_json[0] == client_payload


@pytest.mark.asyncio
@pytest.mark.parametrize("client_payloads", [2], indirect=True)
@pytest.mark.parametrize(
    "params_template",
    [
        {"name": "client_name"},
        {"surname": "client_surname"},
        {"name": "client_name", "surname": "client_surname"},
    ],
)
async def test_get_all_by_fields_double(
    client: AsyncClient,
    client_payloads: List[dict],
    params_template: dict,
) -> None:
    for value in params_template.values():
        client_payloads[1][value] = client_payloads[0][value]
    await create_clients(client, client_payloads)

    params = {key: client_payloads[0][value] for key, value in params_template.items()}
    response_get = await client.get("client/all", params=params)
    assert response_get.status_code == 200
    response_get_json = response_get.json()
    assert len(response_get_json) == 2
    for i, client_payload in enumerate(client_payloads):
        assert client_payload == response_get_json[i]


@pytest.mark.asyncio
@pytest.mark.parametrize("client_payloads", [2], indirect=True)
async def test_update_client(
    client: AsyncClient,
    client_payloads: List[dict],
) -> None:
    updated_client = dict(client_payloads[1])
    await create_clients(client, client_payloads)
    created_client = client_payloads[0]
    response_get = await client.patch(
        f"client/{created_client['id']}", json=updated_client
    )
    updated_client["id"] = created_client["id"]
    assert response_get.status_code == 200
    assert response_get.json() == updated_client


@pytest.mark.asyncio
@pytest.mark.parametrize("client_payloads", [1], indirect=True)
@pytest.mark.parametrize(
    "update",
    [
        {"client_name": "new_name"},
        {"client_surname": "new_surname"},
        {"birthday": random_date()},
        {"gender": None},
        {
            "address": {
                "country": "new_country",
                "city": "new_city",
                "street": "new_street",
            }
        },
        {"address": {"country": "new_country"}},
        {"address": {"city": "new_city"}},
        {"address": {"street": "new_street"}},
    ],
)
async def test_update_client_field(
    client: AsyncClient,
    client_payloads: List[dict],
    update: dict,
) -> None:
    await create_clients(client, client_payloads)
    created_client = client_payloads[0]
    if "gender" in update:
        update["gender"] = "M" if created_client["gender"] == "F" else "F"
    response_get = await client.patch(f"client/{created_client['id']}", json=update)
    if "address" in update:
        created_client["address"].update(update["address"])
    else:
        created_client.update(update)
    assert response_get.status_code == 200
    assert response_get.json() == created_client


@pytest.mark.asyncio
@pytest.mark.parametrize("client_payloads", [1, 2], indirect=True)
async def test_delete_client(
    client: AsyncClient,
    client_payloads: List[dict],
) -> None:
    await create_clients(client, client_payloads)
    for client_payload in client_payloads:
        response_get = await client.delete(f"client/{client_payload['id']}")
        assert response_get.status_code == 200
        assert response_get.json() is True
