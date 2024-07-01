from typing import List
import pytest
from httpx import AsyncClient
from uuid_extensions import uuid7

import tests.utils as utils


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "product_payloads, supplier_payloads", ([1, 1],), indirect=True
)
@pytest.mark.parametrize(
    "invalid_field",
    [
        {"price": "text_price"},
        {"available_stock": "text_available_stock"},
        {"last_update_date": "text_date"},
        {"supplier_id": "123"},
    ],
)
async def test_post_product_invalid_field(
    client: AsyncClient,
    product_payloads: List[dict],
    supplier_payloads: List[dict],
    invalid_field: dict,
) -> None:
    await utils.create_entities(client, "supplier", supplier_payloads)
    product_payload = product_payloads[0]
    supplier_payload = supplier_payloads[0]
    product_payload["supplier_id"] = supplier_payload["id"]
    product_payload.update(invalid_field)
    response_create = await client.post("product", json=product_payload)
    await utils.check_422_error(response_create, next(iter(invalid_field)))


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "product_payloads, supplier_payloads", ([1, 1],), indirect=True
)
@pytest.mark.parametrize(
    "field",
    (
        "name",
        "category",
        "price",
        "available_stock",
        "last_update_date",
        "supplier_id",
    ),
)
async def test_post_product_fields_absence(
    client: AsyncClient,
    product_payloads: List[dict],
    supplier_payloads: List[dict],
    field: str,
) -> None:
    await utils.create_entities(client, "supplier", supplier_payloads)
    product_payload = product_payloads[0]
    supplier_payload = supplier_payloads[0]
    product_payload["supplier_id"] = supplier_payload["id"]
    if "." in field:
        field, subfield = field.split(".")
        product_payload[field].pop(subfield)
        field = subfield
    else:
        product_payload.pop(field)
    response_create = await client.post("product", json=product_payload)
    await utils.check_422_error(response_create, field)


@pytest.mark.asyncio
@pytest.mark.parametrize("product_payloads", [1], indirect=True)
async def test_post_product_supplier_not_found(
    client: AsyncClient, product_payloads: List[dict]
) -> None:
    product_payload = product_payloads[0]
    product_payload["supplier_id"] = str(uuid7())
    response_create = await client.post("product", json=product_payload)
    assert response_create.status_code == 404


@pytest.mark.asyncio
async def test_get_product_not_found(client: AsyncClient) -> None:
    response_get = await client.get(f"product/{uuid7()}")
    assert response_get.status_code == 404


@pytest.mark.asyncio
async def test_get_product_incorrect_uuid(client: AsyncClient) -> None:
    response_get = await client.get("product/123")
    await utils.check_422_error(response_get, "id")


@pytest.mark.asyncio
@pytest.mark.parametrize("params", [{"limit": "limit"}, {"offset": "offset"}])
async def test_get_all_clients_offset_limit(client: AsyncClient, params: dict) -> None:
    response_get = await client.get("product/all", params=params)
    await utils.check_422_error(response_get, next(iter(params)))


@pytest.mark.asyncio
async def test_patch_product_incorrect_uuid(client: AsyncClient) -> None:
    response_patch = await client.patch("product/123", json={"amount_to_reduce": "1"})
    await utils.check_422_error(response_patch, "id")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "product_payloads, supplier_payloads", ([1, 1],), indirect=True
)
@pytest.mark.parametrize("invalid_stock", ("test",))
async def test_patch_product_invalid_stock(
    client: AsyncClient,
    product_payloads: List[dict],
    supplier_payloads: List[dict],
    invalid_stock: str,
) -> None:
    await utils.create_products(client, supplier_payloads, product_payloads)
    created_product = product_payloads[0]
    response_patch = await client.patch(
        f"product/{created_product['id']}", json={"amount_to_reduce": invalid_stock}
    )
    await utils.check_422_error(response_patch, "amount_to_reduce")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "product_payloads, supplier_payloads", ([1, 1],), indirect=True
)
async def test_patch_product_not_enough_stock(
    client: AsyncClient, product_payloads: List[dict], supplier_payloads: List[dict]
) -> None:
    await utils.create_products(client, supplier_payloads, product_payloads)
    created_product = product_payloads[0]
    response_patch = await client.patch(
        f"product/{created_product['id']}",
        json={"amount_to_reduce": created_product["available_stock"] + 1},
    )
    assert response_patch.status_code == 400
    response_patch_json = response_patch.json()
    assert "detail" in response_patch_json
    assert response_patch_json["detail"] == "Not enough stock"


@pytest.mark.asyncio
async def test_delete_product_incorrect_uuid(client: AsyncClient) -> None:
    response_delete = await client.delete("product/123")
    await utils.check_422_error(response_delete, "id")
