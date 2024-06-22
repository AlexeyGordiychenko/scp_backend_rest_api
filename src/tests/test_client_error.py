from typing import List
import pytest
from httpx import AsyncClient
from uuid_extensions import uuid7

import tests.utils as utils


@pytest.mark.asyncio
@pytest.mark.parametrize("client_payloads", [1], indirect=True)
@pytest.mark.parametrize(
    "invalid_field",
    [
        {"gender": "incorrect_gender"},
        {"birthday": "1"},
        {"birthday": "1-1-2024 11:11:11"},
    ],
)
async def test_post_client_invalid_field(
    client: AsyncClient, client_payloads: List[dict], invalid_field: dict
) -> None:
    client_payload = client_payloads[0]
    client_payload.update(invalid_field)
    response_create = await client.post("client", json=client_payload)
    await utils.check_422_error(response_create, next(iter(invalid_field)))


@pytest.mark.asyncio
@pytest.mark.parametrize("client_payloads", [1], indirect=True)
@pytest.mark.parametrize(
    "field",
    (
        "client_name",
        "client_surname",
        "birthday",
        "gender",
        "address",
        "address.country",
        "address.city",
        "address.street",
    ),
)
async def test_post_client_fields_absence(
    client: AsyncClient, client_payloads: List[dict], field: str
) -> None:
    client_payload = client_payloads[0]
    if "." in field:
        field, subfield = field.split(".")
        client_payload[field].pop(subfield)
        field = subfield
    else:
        client_payload.pop(field)
    response_create = await client.post("client", json=client_payload)
    await utils.check_422_error(response_create, field)


@pytest.mark.asyncio
async def test_get_client_not_found(client: AsyncClient) -> None:
    response_get = await client.get(f"client/{uuid7()}")
    assert response_get.status_code == 404


@pytest.mark.asyncio
async def test_get_client_incorrect_uuid(client: AsyncClient) -> None:
    response_get = await client.get("client/123")
    await utils.check_422_error(response_get, "id")


@pytest.mark.asyncio
@pytest.mark.parametrize("params", [{"limit": "limit"}, {"offset": "offset"}])
async def test_get_all_clients_offset_limit(client: AsyncClient, params: dict) -> None:
    response_get = await client.get("client/all", params=params)
    await utils.check_422_error(response_get, next(iter(params)))


@pytest.mark.asyncio
async def test_patch_client_incorrect_uuid(client: AsyncClient) -> None:
    response_patch = await client.patch("client/123", json={"client_name": "test"})
    await utils.check_422_error(response_patch, "id")


@pytest.mark.asyncio
@pytest.mark.parametrize("client_payloads", [1], indirect=True)
@pytest.mark.parametrize(
    "invalid_field",
    [
        {"gender": "incorrect_gender"},
        {"birthday": "1"},
        {"birthday": "1-1-2024 11:11:11"},
    ],
)
async def test_patch_client_invalid_field(
    client: AsyncClient, client_payloads: List[dict], invalid_field: dict
) -> None:
    await utils.create_entities(client, "client", client_payloads)
    created_client = client_payloads[0]
    response_patch = await client.patch(
        f"client/{created_client['id']}", json=invalid_field
    )
    await utils.check_422_error(response_patch, next(iter(invalid_field)))


@pytest.mark.asyncio
async def test_delete_client_incorrect_uuid(client: AsyncClient) -> None:
    response_delete = await client.delete("client/123")
    await utils.check_422_error(response_delete, "id")
