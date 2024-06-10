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
    "limit, offset",
    [
        (3, None),
        (3, 4),
        (None, 8),
    ],
)
async def test_get_all_clients_pagination(
    client: AsyncClient,
    client_payloads: List[dict],
    limit: Optional[int],
    offset: Optional[int],
) -> None:
    await create_clients(client, client_payloads)

    query_string = "&".join(
        (
            f"offset={offset}" if offset is not None else "",
            f"limit={limit}" if limit is not None else "",
        )
    )
    offset = 0 if offset is None else offset
    limit = len(client_payloads) - offset if limit is None else limit

    response_get = await client.get(f"client/all?{query_string}")
    assert response_get.status_code == 200
    response_get_json = response_get.json()
    assert len(response_get_json) == limit
    for i, client_payload in enumerate(client_payloads[offset : offset + limit]):
        assert client_payload == response_get_json[i]


@pytest.mark.asyncio
@pytest.mark.parametrize("client_payloads", [1, 2], indirect=True)
async def test_get_all_by_name(
    client: AsyncClient,
    client_payloads: List[dict],
) -> None:
    await create_clients(client, client_payloads)
    for client_payload in client_payloads:
        response_get = await client.get(
            f"client/all?name={client_payload['client_name']}"
        )
        assert response_get.status_code == 200
        response_get_json = response_get.json()
        assert len(response_get_json) == 1
        assert response_get_json[0] == client_payload


@pytest.mark.asyncio
@pytest.mark.parametrize("client_payloads", [2], indirect=True)
async def test_get_all_by_name_double(
    client: AsyncClient,
    client_payloads: List[dict],
) -> None:
    client_name = client_payloads[0]["client_name"]
    client_payloads[1]["client_name"] = client_name
    await create_clients(client, client_payloads)

    response_get = await client.get(f"client/all?name={client_name}")
    assert response_get.status_code == 200
    response_get_json = response_get.json()
    assert len(response_get_json) == 2
    for i, client_payload in enumerate(client_payloads):
        assert client_payload == response_get_json[i]


@pytest.mark.asyncio
@pytest.mark.parametrize("client_payloads", [1, 2], indirect=True)
async def test_get_all_by_surname(
    client: AsyncClient,
    client_payloads: List[dict],
) -> None:
    await create_clients(client, client_payloads)
    for client_payload in client_payloads:
        response_get = await client.get(
            f"client/all?surname={client_payload['client_surname']}"
        )
        assert response_get.status_code == 200
        response_get_json = response_get.json()
        assert len(response_get_json) == 1
        assert response_get_json[0] == client_payload


@pytest.mark.asyncio
@pytest.mark.parametrize("client_payloads", [2], indirect=True)
async def test_get_all_by_surname_double(
    client: AsyncClient,
    client_payloads: List[dict],
) -> None:
    client_surname = client_payloads[0]["client_surname"]
    client_payloads[1]["client_surname"] = client_surname
    await create_clients(client, client_payloads)

    response_get = await client.get(f"client/all?surname={client_surname}")
    assert response_get.status_code == 200
    response_get_json = response_get.json()
    assert len(response_get_json) == 2
    for i, client_payload in enumerate(client_payloads):
        assert client_payload == response_get_json[i]


@pytest.mark.asyncio
@pytest.mark.parametrize("client_payloads", [1, 2], indirect=True)
async def test_get_all_by_name_and_surname(
    client: AsyncClient,
    client_payloads: List[dict],
) -> None:
    await create_clients(client, client_payloads)
    for client_payload in client_payloads:
        response_get = await client.get(
            f"client/all?name={client_payload['client_name']}&surname={client_payload['client_surname']}"
        )
        assert response_get.status_code == 200
        response_get_json = response_get.json()
        assert len(response_get_json) == 1
        assert response_get_json[0] == client_payload


@pytest.mark.asyncio
@pytest.mark.parametrize("client_payloads", [2], indirect=True)
async def test_get_all_by_name_and_surname_double(
    client: AsyncClient,
    client_payloads: List[dict],
) -> None:
    client_name = client_payloads[0]["client_name"]
    client_surname = client_payloads[0]["client_surname"]
    client_payloads[1]["client_name"] = client_name
    client_payloads[1]["client_surname"] = client_surname
    await create_clients(client, client_payloads)

    response_get = await client.get(
        f"client/all?name={client_name}&surname={client_surname}"
    )
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
async def test_update_client_name(
    client: AsyncClient,
    client_payloads: List[dict],
) -> None:
    await create_clients(client, client_payloads)
    created_client = client_payloads[0]
    updated_client = {"client_name": "new_name"}
    response_get = await client.patch(
        f"client/{created_client['id']}", json=updated_client
    )
    created_client.update(updated_client)
    assert response_get.status_code == 200
    assert response_get.json() == created_client


@pytest.mark.asyncio
@pytest.mark.parametrize("client_payloads", [1], indirect=True)
async def test_update_client_surname(
    client: AsyncClient,
    client_payloads: List[dict],
) -> None:
    await create_clients(client, client_payloads)
    created_client = client_payloads[0]
    updated_client = {"client_surname": "new_surname"}
    response_get = await client.patch(
        f"client/{created_client['id']}", json=updated_client
    )
    created_client.update(updated_client)
    assert response_get.status_code == 200
    assert response_get.json() == created_client


@pytest.mark.asyncio
@pytest.mark.parametrize("client_payloads", [1], indirect=True)
async def test_update_client_birthday(
    client: AsyncClient, client_payloads: List[dict]
) -> None:
    await create_clients(client, client_payloads)
    created_client = client_payloads[0]
    updated_client = {"birthday": random_date()}
    response_get = await client.patch(
        f"client/{created_client['id']}", json=updated_client
    )

    created_client.update(updated_client)
    assert response_get.status_code == 200
    assert response_get.json() == created_client


@pytest.mark.asyncio
@pytest.mark.parametrize("client_payloads", [1], indirect=True)
async def test_update_client_gender(
    client: AsyncClient,
    client_payloads: List[dict],
) -> None:
    await create_clients(client, client_payloads)
    created_client = client_payloads[0]
    updated_client = {"gender": "M" if created_client["gender"] == "F" else "F"}
    response_get = await client.patch(
        f"client/{created_client['id']}", json=updated_client
    )

    created_client.update(updated_client)
    assert response_get.status_code == 200
    assert response_get.json() == created_client


@pytest.mark.asyncio
@pytest.mark.parametrize("client_payloads", [1], indirect=True)
async def test_update_client_address(
    client: AsyncClient,
    client_payloads: List[dict],
) -> None:
    await create_clients(client, client_payloads)
    created_client = client_payloads[0]
    updated_client = {
        "address": {
            "country": "new_country",
            "city": "new_city",
            "street": "new_street",
        }
    }
    response_get = await client.patch(
        f"client/{created_client['id']}", json=updated_client
    )

    created_client.update(updated_client)
    assert response_get.status_code == 200
    assert response_get.json() == created_client


@pytest.mark.asyncio
@pytest.mark.parametrize("client_payloads", [1], indirect=True)
async def test_update_client_address_country(
    client: AsyncClient,
    client_payloads: List[dict],
) -> None:
    await create_clients(client, client_payloads)
    created_client = client_payloads[0]
    updated_client = {"address": {"country": "new_country"}}
    response_get = await client.patch(
        f"client/{created_client['id']}", json=updated_client
    )

    created_client["address"].update(updated_client["address"])
    assert response_get.status_code == 200
    assert response_get.json() == created_client


@pytest.mark.asyncio
@pytest.mark.parametrize("client_payloads", [1], indirect=True)
async def test_update_client_address_city(
    client: AsyncClient,
    client_payloads: List[dict],
) -> None:
    await create_clients(client, client_payloads)
    created_client = client_payloads[0]
    updated_client = {"address": {"city": "new_city"}}
    response_get = await client.patch(
        f"client/{created_client['id']}", json=updated_client
    )

    created_client["address"].update(updated_client["address"])
    assert response_get.status_code == 200
    assert response_get.json() == created_client


@pytest.mark.asyncio
@pytest.mark.parametrize("client_payloads", [1], indirect=True)
async def test_update_client_address_street(
    client: AsyncClient,
    client_payloads: List[dict],
) -> None:
    await create_clients(client, client_payloads)
    created_client = client_payloads[0]
    updated_client = {"address": {"street": "new_street"}}
    response_get = await client.patch(
        f"client/{created_client['id']}", json=updated_client
    )

    created_client["address"].update(updated_client["address"])
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
