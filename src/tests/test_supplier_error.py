from typing import List
import pytest
from httpx import AsyncClient
from uuid_extensions import uuid7

import tests.utils as utils


@pytest.mark.asyncio
@pytest.mark.parametrize("supplier_payloads", [1], indirect=True)
@pytest.mark.parametrize(
    "invalid_field",
    [
        {"phone_number": "invalid_phone_number"},
    ],
)
async def test_post_supplier_invalid_field(
    client: AsyncClient, supplier_payloads: List[dict], invalid_field: dict
) -> None:
    supplier_payload = supplier_payloads[0]
    supplier_payload.update(invalid_field)
    response_create = await client.post("supplier", json=supplier_payload)
    await utils.check_422_error(response_create, next(iter(invalid_field)))


@pytest.mark.asyncio
@pytest.mark.parametrize("supplier_payloads", [1], indirect=True)
@pytest.mark.parametrize(
    "field",
    (
        "name",
        "phone_number",
        "address",
        "address.country",
        "address.city",
        "address.street",
    ),
)
async def test_post_supplier_fields_absence(
    client: AsyncClient, supplier_payloads: List[dict], field: str
) -> None:
    supplier_payload = supplier_payloads[0]
    if "." in field:
        field, subfield = field.split(".")
        supplier_payload[field].pop(subfield)
        field = subfield
    else:
        supplier_payload.pop(field)
    response_create = await client.post("supplier", json=supplier_payload)
    await utils.check_422_error(response_create, field)


@pytest.mark.asyncio
async def test_get_supplier_not_found(client: AsyncClient) -> None:
    response_get = await client.get(f"supplier/{uuid7()}")
    assert response_get.status_code == 404


@pytest.mark.asyncio
async def test_get_supplier_incorrect_uuid(client: AsyncClient) -> None:
    response_get = await client.get("supplier/123")
    await utils.check_422_error(response_get, "id")


@pytest.mark.asyncio
@pytest.mark.parametrize("params", [{"limit": "limit"}, {"offset": "offset"}])
async def test_get_all_clients_offset_limit(client: AsyncClient, params: dict) -> None:
    response_get = await client.get("supplier/all", params=params)
    await utils.check_422_error(response_get, next(iter(params)))


@pytest.mark.asyncio
async def test_patch_supplier_incorrect_uuid(client: AsyncClient) -> None:
    response_patch = await client.patch("supplier/123", json={"name": "test"})
    await utils.check_422_error(response_patch, "id")


@pytest.mark.asyncio
@pytest.mark.parametrize("supplier_payloads", [1], indirect=True)
@pytest.mark.parametrize(
    "invalid_field",
    [
        {"phone_number": "invalid_phone_number"},
    ],
)
async def test_patch_supplier_invalid_phone_number(
    client: AsyncClient, supplier_payloads: List[dict], invalid_field: dict
) -> None:
    await utils.create_entities(client, "supplier", supplier_payloads)
    created_supplier = supplier_payloads[0]
    response_patch = await client.patch(
        f"supplier/{created_supplier['id']}",
        json=invalid_field,
    )
    await utils.check_422_error(response_patch, next(iter(invalid_field)))


@pytest.mark.asyncio
async def test_delete_supplier_incorrect_uuid(client: AsyncClient) -> None:
    response_delete = await client.delete("supplier/123")
    await utils.check_422_error(response_delete, "id")
