from typing import List
import pytest
from httpx import AsyncClient
from uuid_extensions import uuid7

import tests.utils as utils


@pytest.mark.asyncio
@pytest.mark.parametrize("image_payloads", (["image1.jpg"],), indirect=True)
@pytest.mark.parametrize("invalid_params", [{"product_id": "123"}, {}])
async def test_post_image_invalid_params(
    client: AsyncClient, image_payloads: List[dict], invalid_params: dict
) -> None:
    response_create = await client.post(
        "image", files={"image": image_payloads[0]["buffer"]}, params=invalid_params
    )
    await utils.check_422_error(response_create, "product_id")


@pytest.mark.asyncio
@pytest.mark.parametrize("image_payloads", (["image1.jpg"],), indirect=True)
async def test_post_image_product_not_found(
    client: AsyncClient, image_payloads: List[dict]
) -> None:
    response_create = await client.post(
        "image",
        files={"image": image_payloads[0]["buffer"]},
        params={"product_id": uuid7()},
    )
    assert response_create.status_code == 404


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "product_payloads, supplier_payloads, image_payloads",
    ([1, 1, ["not_image.txt"]],),
    indirect=True,
)
async def test_post_image_invalid_file(
    client: AsyncClient,
    product_payloads: List[dict],
    supplier_payloads: List[dict],
    image_payloads: List[dict],
) -> None:
    await utils.create_products(client, supplier_payloads, product_payloads)
    response_create = await client.post(
        "image",
        files={"image": image_payloads[0]["buffer"]},
        params={"product_id": product_payloads[0]["id"]},
    )
    assert response_create.status_code == 400
    response_create_json = response_create.json()
    assert "detail" in response_create_json
    assert response_create_json["detail"] == "Invalid image"


@pytest.mark.asyncio
async def test_get_image_not_found(client: AsyncClient) -> None:
    response_get = await client.get(f"image/{uuid7()}")
    assert response_get.status_code == 404


@pytest.mark.asyncio
async def test_get_image_incorrect_uuid(client: AsyncClient) -> None:
    response_get = await client.get("image/123")
    await utils.check_422_error(response_get, "id")


@pytest.mark.asyncio
async def test_get_product_images_not_found(client: AsyncClient) -> None:
    response_get = await client.get(f"product/{uuid7()}/images")
    assert response_get.status_code == 404


@pytest.mark.asyncio
async def test_get_product_images_incorrect_uuid(client: AsyncClient) -> None:
    response_get = await client.get("product/123/images")
    await utils.check_422_error(response_get, "id")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "product_payloads, supplier_payloads", ([1, 1],), indirect=True
)
@pytest.mark.parametrize("params", [{"limit": "limit"}, {"offset": "offset"}])
async def test_get_product_images_offset_limit(
    client: AsyncClient,
    product_payloads: List[dict],
    supplier_payloads: List[dict],
    params: dict,
) -> None:
    await utils.create_products(client, supplier_payloads, product_payloads)
    response_get = await client.get(
        f"product/{product_payloads[0]['id']}/images", params=params
    )
    await utils.check_422_error(response_get, next(iter(params)))


@pytest.mark.asyncio
@pytest.mark.parametrize("image_payloads", (["image1.jpg"],), indirect=True)
async def test_patch_image_not_found(
    client: AsyncClient, image_payloads: List[dict]
) -> None:
    response_patch = await client.patch(
        f"image/{uuid7()}", files={"image": image_payloads[0]["buffer"]}
    )
    assert response_patch.status_code == 404


@pytest.mark.asyncio
@pytest.mark.parametrize("image_payloads", (["image1.jpg"],), indirect=True)
async def test_patch_image_incorrect_uuid(
    client: AsyncClient, image_payloads: List[dict]
) -> None:
    response_patch = await client.patch(
        "image/123", files={"image": image_payloads[0]["buffer"]}
    )
    await utils.check_422_error(response_patch, "id")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "product_payloads, supplier_payloads, image_payloads",
    ([1, 1, ["image1.jpg", "not_image.txt"]],),
    indirect=True,
)
async def test_patch_image_invalid_file(
    client: AsyncClient,
    product_payloads: List[dict],
    supplier_payloads: List[dict],
    image_payloads: List[dict],
) -> None:
    created_images = await utils.create_images(
        client, supplier_payloads, product_payloads, [image_payloads[0]]
    )
    response_patch = await client.patch(
        f"image/{created_images[0].id}/",
        files={"image": image_payloads[1]["buffer"]},
    )
    assert response_patch.status_code == 400
    response_create_json = response_patch.json()
    assert "detail" in response_create_json
    assert response_create_json["detail"] == "Invalid image"


@pytest.mark.asyncio
async def test_delete_image_not_found(client: AsyncClient) -> None:
    response_delete = await client.delete(f"image/{uuid7()}")
    assert response_delete.status_code == 404


@pytest.mark.asyncio
async def test_delete_image_incorrect_uuid(client: AsyncClient) -> None:
    response_delete = await client.delete("image/123")
    await utils.check_422_error(response_delete, "id")
