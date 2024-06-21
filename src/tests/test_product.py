from typing import List
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

import tests.utils as utils


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "product_payloads, supplier_payloads", ([2, 2], [2, 1]), indirect=True
)
async def test_post_product(
    client: AsyncClient,
    product_payloads: List[dict],
    supplier_payloads: List[dict],
    db_session: AsyncSession,
) -> None:
    await utils.create_products(client, supplier_payloads, product_payloads)
    for product_payload in product_payloads:
        await utils.compare_db_product_to_payload(product_payload, db_session)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "product_payloads, supplier_payloads", ([2, 2], [2, 1]), indirect=True
)
async def test_get_product(
    client: AsyncClient, product_payloads: List[dict], supplier_payloads: List[dict]
) -> None:
    await utils.create_products(client, supplier_payloads, product_payloads)
    for product_payload in product_payloads:
        response_get = await client.get(f"product/{product_payload['id']}")
        assert response_get.status_code == 200
        assert response_get.json() == product_payload


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "product_payloads, supplier_payloads", ([10, 7],), indirect=True
)
@pytest.mark.parametrize(
    "params", [{"limit": 3}, {"limit": 3, "offset": 4}, {"offset": 8}, {}]
)
async def test_get_all_products_pagination(
    client: AsyncClient,
    product_payloads: List[dict],
    supplier_payloads: List[dict],
    params: dict,
) -> None:
    await utils.create_products(client, supplier_payloads, product_payloads)
    offset = params.get("offset", 0)
    limit = params.get("limit", len(product_payloads) - offset)
    response_get = await client.get("product/all", params=params)
    assert response_get.status_code == 200
    response_get_json = response_get.json()
    assert len(response_get_json) == limit
    for i, product_payload in enumerate(product_payloads[offset : offset + limit]):
        assert product_payload == response_get_json[i]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "product_payloads, supplier_payloads", ([2, 2],), indirect=True
)
@pytest.mark.parametrize("params_template", [{"name": "name"}])
async def test_get_all_by_fields(
    client: AsyncClient,
    product_payloads: List[dict],
    supplier_payloads: List[dict],
    params_template: dict,
) -> None:
    await utils.create_products(client, supplier_payloads, product_payloads)
    for product_payload in product_payloads:
        params = {key: product_payload[value] for key, value in params_template.items()}
        response_get = await client.get("product/all", params=params)
        assert response_get.status_code == 200
        response_get_json = response_get.json()
        assert len(response_get_json) == 1
        assert response_get_json[0] == product_payload


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "product_payloads, supplier_payloads", ([2, 2],), indirect=True
)
@pytest.mark.parametrize("params_template", [{"name": "name"}])
async def test_get_all_by_fields_double(
    client: AsyncClient,
    product_payloads: List[dict],
    supplier_payloads: List[dict],
    params_template: dict,
) -> None:
    for value in params_template.values():
        product_payloads[1][value] = product_payloads[0][value]
    await utils.create_products(client, supplier_payloads, product_payloads)

    params = {key: product_payloads[0][value] for key, value in params_template.items()}
    response_get = await client.get("product/all", params=params)
    assert response_get.status_code == 200
    response_get_json = response_get.json()
    assert len(response_get_json) == 2
    for i, product_payload in enumerate(product_payloads):
        assert product_payload == response_get_json[i]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "product_payloads, supplier_payloads", ([2, 2],), indirect=True
)
async def test_patch_product_stock(
    client: AsyncClient,
    product_payloads: List[dict],
    supplier_payloads: List[dict],
    db_session: AsyncSession,
) -> None:
    await utils.create_products(client, supplier_payloads, product_payloads)
    created_product = product_payloads[0]
    created_product["available_stock"] -= 1
    response_patch = await client.patch(
        f"product/{created_product['id']}", json={"amount_to_reduce": 1}
    )
    assert response_patch.status_code == 200
    assert response_patch.json() == created_product
    for product_payload in product_payloads:
        await utils.compare_db_product_to_payload(product_payload, db_session)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "product_payloads, supplier_payloads", ([2, 2],), indirect=True
)
async def test_delete_product(
    client: AsyncClient,
    product_payloads: List[dict],
    supplier_payloads: List[dict],
    db_session: AsyncSession,
) -> None:
    await utils.create_products(client, supplier_payloads, product_payloads)
    for product_payload in product_payloads:
        response_delete = await client.delete(f"product/{product_payload['id']}")
        assert response_delete.status_code == 200
        assert response_delete.json() is True
        assert (
            await utils.get_product_from_db(product_payload["id"], db_session) is None
        )
