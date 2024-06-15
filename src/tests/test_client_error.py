from typing import List
import pytest
from httpx import AsyncClient
from uuid_extensions import uuid7

import tests.utils as utils


@pytest.mark.asyncio
@pytest.mark.parametrize("client_payloads", [1], indirect=True)
@pytest.mark.parametrize("invalid_gender", ("test",))
async def test_post_client_gender(
    client: AsyncClient, client_payloads: List[dict], invalid_gender: str
) -> None:
    client_payload = client_payloads[0]
    client_payload["gender"] = invalid_gender
    response_create = await client.post(
        "client",
        json=client_payload,
    )
    await utils.check_422_error(response_create, "gender")


@pytest.mark.asyncio
@pytest.mark.parametrize("client_payloads", [1], indirect=True)
@pytest.mark.parametrize("invalid_birthday", ("1", "1-1-2024 11:11:11"))
async def test_post_client_birthday(
    client: AsyncClient, client_payloads: List[dict], invalid_birthday: str
) -> None:
    client_payload = client_payloads[0]
    client_payload["birthday"] = invalid_birthday
    response_create = await client.post(
        "client",
        json=client_payload,
    )
    await utils.check_422_error(response_create, "birthday")


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
    response_create = await client.post(
        "client",
        json=client_payload,
    )
    await utils.check_422_error(response_create, field)


@pytest.mark.asyncio
async def test_get_client_not_found(
    client: AsyncClient,
) -> None:
    response_get = await client.get(f"client/{uuid7()}")
    assert response_get.status_code == 404


@pytest.mark.asyncio
async def test_get_client_incorrect_uuid(
    client: AsyncClient,
) -> None:
    response_get = await client.get("client/123")
    await utils.check_422_error(response_get, "id")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "params",
    [
        {"limit": "limit"},
        {"offset": "offset"},
    ],
)
async def test_get_all_clients_offset_limit(
    client: AsyncClient,
    params: dict,
) -> None:
    response_get = await client.get("client/all", params=params)
    await utils.check_422_error(response_get, next(iter(params)))
