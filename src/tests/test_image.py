from io import BytesIO
from typing import List
import zipfile
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

import tests.utils as utils


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "product_payloads, supplier_payloads, image_payloads",
    ([1, 1, ["image1.jpg", "image2.png"]],),
    indirect=True,
)
async def test_post_image(
    client: AsyncClient,
    product_payloads: List[dict],
    supplier_payloads: List[dict],
    image_payloads: List[dict],
    db_session: AsyncSession,
) -> None:
    created_images = await utils.create_images(
        client, supplier_payloads, product_payloads, image_payloads
    )
    for created_image in created_images:
        await utils.compare_db_image_to_payload(created_image, db_session)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "product_payloads, supplier_payloads, image_payloads",
    ([1, 1, ["image1.jpg", "image2.png"]],),
    indirect=True,
)
async def test_get_image(
    client: AsyncClient,
    product_payloads: List[dict],
    supplier_payloads: List[dict],
    image_payloads: List[dict],
) -> None:
    created_images = await utils.create_images(
        client, supplier_payloads, product_payloads, image_payloads
    )
    for created_image in created_images:
        response_get = await client.get(f"image/{created_image.id}")
        assert response_get.status_code == 200
        assert response_get.headers["content-type"] == "application/octet-stream"
        assert response_get.content == created_image.image


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "product_payloads, supplier_payloads, image_payloads",
    ([1, 1, ["image1.jpg", "image2.png"]],),
    indirect=True,
)
@pytest.mark.parametrize(
    "params", [{"limit": 1}, {"limit": 1, "offset": 1}, {"offset": 1}, {}]
)
async def test_get_products_images(
    client: AsyncClient,
    product_payloads: List[dict],
    supplier_payloads: List[dict],
    image_payloads: List[dict],
    params: dict,
) -> None:
    created_images = await utils.create_images(
        client, supplier_payloads, product_payloads, image_payloads
    )
    offset = params.get("offset", 0)
    limit = params.get("limit", len(image_payloads) - offset)
    response_get = await client.get(
        f"product/{product_payloads[0]['id']}/images", params=params
    )
    assert response_get.status_code == 200
    assert response_get.headers["content-type"] == "application/octet-stream"
    zip_buffer = BytesIO(response_get.content)
    with zipfile.ZipFile(zip_buffer, "r") as zf:
        file_list = zf.namelist()
        assert len(file_list) == limit
        for i, created_image in enumerate(created_images[offset : offset + limit]):
            with zf.open(file_list[i]) as image_file:
                assert image_file.read() == created_image.image


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "product_payloads, supplier_payloads, image_payloads",
    ([1, 1, ["image1.jpg", "image2.png"]],),
    indirect=True,
)
async def test_patch_image(
    client: AsyncClient,
    product_payloads: List[dict],
    supplier_payloads: List[dict],
    image_payloads: List[dict],
    db_session: AsyncSession,
) -> None:
    created_images = await utils.create_images(
        client, supplier_payloads, product_payloads, [image_payloads[0]]
    )
    response_patch = await client.patch(
        f"image/{created_images[0].id}/",
        files={"image": image_payloads[1]["buffer"]},
    )
    assert response_patch.status_code == 200
    image_payloads[1]["buffer"].seek(0)
    created_images[0].image = image_payloads[1]["buffer"].read()
    created_images[0].extension = image_payloads[1]["extension"]
    await utils.compare_db_image_to_payload(created_images[0], db_session)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "product_payloads, supplier_payloads, image_payloads",
    ([1, 1, ["image1.jpg", "image2.png"]],),
    indirect=True,
)
async def test_delete_image(
    client: AsyncClient,
    product_payloads: List[dict],
    supplier_payloads: List[dict],
    image_payloads: List[dict],
    db_session: AsyncSession,
) -> None:
    created_images = await utils.create_images(
        client, supplier_payloads, product_payloads, [image_payloads[0]]
    )
    for created_image in created_images:
        response_delete = await client.delete(f"image/{created_image.id}")
        assert response_delete.status_code == 200
        assert response_delete.json() is True
        assert await utils.get_image_from_db(created_image.id, db_session) is None
