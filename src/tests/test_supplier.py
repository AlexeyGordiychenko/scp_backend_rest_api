from typing import List
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from uuid_extensions import uuid7

import tests.utils as utils


@pytest.mark.asyncio
@pytest.mark.parametrize("supplier_payloads", [1, 2], indirect=True)
async def test_post_supplier(
    client: AsyncClient,
    supplier_payloads: List[dict],
    db_session: AsyncSession,
) -> None:
    await utils.create_entities(client, "supplier", supplier_payloads)
    for supplier_payload in supplier_payloads:
        await utils.compare_db_supplier_to_payload(supplier_payload, db_session)


@pytest.mark.asyncio
@pytest.mark.parametrize("supplier_payloads", [1, 2], indirect=True)
async def test_get_supplier(
    client: AsyncClient,
    supplier_payloads: List[dict],
) -> None:
    await utils.create_entities(client, "supplier", supplier_payloads)
    for supplier_payload in supplier_payloads:
        response_get = await client.get(f"supplier/{supplier_payload['id']}")
        assert response_get.status_code == 200
        assert response_get.json() == supplier_payload


@pytest.mark.asyncio
async def test_get_supplier_not_found(
    client: AsyncClient,
) -> None:
    response_get = await client.get(f"supplier/{uuid7()}")
    assert response_get.status_code == 404


@pytest.mark.asyncio
@pytest.mark.parametrize("supplier_payloads", [10, 15], indirect=True)
@pytest.mark.parametrize(
    "params",
    [
        {"limit": 3},
        {"limit": 3, "offset": 4},
        {"offset": 8},
        {},
    ],
)
async def test_get_all_suppliers_pagination(
    client: AsyncClient,
    supplier_payloads: List[dict],
    params: dict,
) -> None:
    await utils.create_entities(client, "supplier", supplier_payloads)
    offset = params.get("offset", 0)
    limit = params.get("limit", len(supplier_payloads) - offset)
    response_get = await client.get("supplier/all", params=params)
    assert response_get.status_code == 200
    response_get_json = response_get.json()
    assert len(response_get_json) == limit
    for i, supplier_payload in enumerate(supplier_payloads[offset : offset + limit]):
        assert supplier_payload == response_get_json[i]


@pytest.mark.asyncio
@pytest.mark.parametrize("supplier_payloads", [1, 2], indirect=True)
@pytest.mark.parametrize(
    "params_template",
    [
        {"name": "name"},
    ],
)
async def test_get_all_by_fields(
    client: AsyncClient,
    supplier_payloads: List[dict],
    params_template: dict,
) -> None:
    await utils.create_entities(client, "supplier", supplier_payloads)
    for supplier_payload in supplier_payloads:
        params = {
            key: supplier_payload[value] for key, value in params_template.items()
        }
        response_get = await client.get("supplier/all", params=params)
        assert response_get.status_code == 200
        response_get_json = response_get.json()
        assert len(response_get_json) == 1
        assert response_get_json[0] == supplier_payload


@pytest.mark.asyncio
@pytest.mark.parametrize("supplier_payloads", [2], indirect=True)
@pytest.mark.parametrize(
    "params_template",
    [
        {"name": "name"},
    ],
)
async def test_get_all_by_fields_double(
    client: AsyncClient,
    supplier_payloads: List[dict],
    params_template: dict,
) -> None:
    for value in params_template.values():
        supplier_payloads[1][value] = supplier_payloads[0][value]
    await utils.create_entities(client, "supplier", supplier_payloads)

    params = {
        key: supplier_payloads[0][value] for key, value in params_template.items()
    }
    response_get = await client.get("supplier/all", params=params)
    assert response_get.status_code == 200
    response_get_json = response_get.json()
    assert len(response_get_json) == 2
    for i, supplier_payload in enumerate(supplier_payloads):
        assert supplier_payload == response_get_json[i]


@pytest.mark.asyncio
@pytest.mark.parametrize("supplier_payloads", [2], indirect=True)
async def test_update_supplier(
    client: AsyncClient,
    supplier_payloads: List[dict],
    db_session: AsyncSession,
) -> None:
    updated_supplier = supplier_payloads.pop()
    await utils.create_entities(client, "supplier", supplier_payloads)
    created_supplier = supplier_payloads[0]
    response_get = await client.patch(
        f"supplier/{created_supplier['id']}", json=updated_supplier
    )
    updated_supplier["id"] = created_supplier["id"]
    assert response_get.status_code == 200
    assert response_get.json() == updated_supplier
    await utils.compare_db_supplier_to_payload(updated_supplier, db_session)


@pytest.mark.asyncio
@pytest.mark.parametrize("supplier_payloads", [1], indirect=True)
@pytest.mark.parametrize(
    "update",
    [
        {"name": "new_name"},
        {"phone_number": "+79999999999"},
    ],
)
async def test_update_supplier_field(
    client: AsyncClient,
    supplier_payloads: List[dict],
    update: dict,
    db_session: AsyncSession,
) -> None:
    await utils.create_entities(client, "supplier", supplier_payloads)
    created_supplier = supplier_payloads[0]
    response_get = await client.patch(f"supplier/{created_supplier['id']}", json=update)
    created_supplier.update(update)
    assert response_get.status_code == 200
    assert response_get.json() == created_supplier
    await utils.compare_db_supplier_to_payload(created_supplier, db_session)


@pytest.mark.asyncio
@pytest.mark.parametrize("supplier_payloads", [1, 2], indirect=True)
async def test_delete_supplier(
    client: AsyncClient,
    supplier_payloads: List[dict],
    db_session: AsyncSession,
) -> None:
    await utils.create_entities(client, "supplier", supplier_payloads)
    for supplier_payload in supplier_payloads:
        response_get = await client.delete(f"supplier/{supplier_payload['id']}")
        assert response_get.status_code == 200
        assert response_get.json() is True
        assert (
            await utils.get_supplier_from_db(supplier_payload["id"], db_session) is None
        )
