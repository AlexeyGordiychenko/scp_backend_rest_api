from datetime import datetime
from itertools import zip_longest
import random
from typing import List
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlmodel import select

from shopAPI.models import (
    Client,
    ClientResponseWithAddress,
    Image,
    ImageResponseFull,
    Product,
    ProductResponseWithSupplierId,
    Supplier,
    SupplierResponseWithAddress,
)


def random_date() -> str:
    start = datetime(1950, 1, 1)
    end = datetime(2000, 1, 1)
    random_date = start + (end - start) * random.random()
    return random_date.strftime("%Y-%m-%d")


async def create_entities(
    client: AsyncClient, path: str, payloads: List[dict]
) -> List[dict]:
    for client_payload in payloads:
        response_create = await client.post(
            path,
            json=client_payload,
        )
        assert response_create.status_code == 201
        response_create_json = response_create.json()
        assert "id" in response_create_json
        client_payload["id"] = response_create_json["id"]
        assert client_payload == response_create_json


async def get_client_from_db(id: str, db_session: AsyncSession):
    return (
        await db_session.scalars(
            select(Client).where(Client.id == id).options(joinedload(Client.address))
        )
    ).one_or_none()


async def compare_db_client_to_payload(client_payload: dict, db_session: AsyncSession):
    db_client = await get_client_from_db(client_payload["id"], db_session)
    assert db_client is not None
    assert (
        ClientResponseWithAddress.model_validate(db_client).model_dump(mode="json")
        == client_payload
    )


async def get_supplier_from_db(id: str, db_session: AsyncSession):
    return (
        await db_session.scalars(
            select(Supplier)
            .where(Supplier.id == id)
            .options(joinedload(Supplier.address))
        )
    ).one_or_none()


async def get_product_from_db(id: str, db_session: AsyncSession):
    return (
        await db_session.scalars(select(Product).where(Product.id == id))
    ).one_or_none()


async def get_image_from_db(id: str, db_session: AsyncSession):
    return (await db_session.scalars(select(Image).where(Image.id == id))).one_or_none()


async def compare_db_supplier_to_payload(
    supplier_payload: dict, db_session: AsyncSession
):
    db_supplier = await get_supplier_from_db(supplier_payload["id"], db_session)
    assert db_supplier is not None
    assert (
        SupplierResponseWithAddress.model_validate(db_supplier).model_dump(mode="json")
        == supplier_payload
    )


async def compare_db_product_to_payload(
    product_payload: dict, db_session: AsyncSession
):
    db_product = await get_product_from_db(product_payload["id"], db_session)
    assert db_product is not None
    assert (
        ProductResponseWithSupplierId.model_validate(db_product).model_dump(mode="json")
        == product_payload
    )


async def check_422_error(response: Response, field: str):
    assert response.status_code == 422
    response_json = response.json()
    assert "detail" in response_json
    detail = response_json["detail"]
    assert len(detail) == 1
    loc = detail[0]["loc"]
    assert isinstance(loc, list)
    assert loc[-1] == field


async def create_products(
    client: AsyncClient, supplier_payloads: List[dict], product_payloads: List[dict]
):
    await create_entities(client, "supplier", supplier_payloads)
    for supplier_payload, product_payload in zip_longest(
        supplier_payloads, product_payloads, fillvalue=supplier_payloads[0]
    ):
        product_payload["supplier_id"] = supplier_payload["id"]
    await create_entities(client, "product", product_payloads)


async def compare_db_image_to_payload(
    image_payload: ImageResponseFull, db_session: AsyncSession
):
    db_image = await get_image_from_db(image_payload.id, db_session)
    assert db_image is not None
    assert db_image.model_dump() == image_payload.model_dump()


async def create_images(
    client: AsyncClient,
    supplier_payloads: List[dict],
    product_payloads: List[dict],
    image_payloads: List[dict],
):
    await create_products(client, supplier_payloads, product_payloads)
    created_images = []
    for image_payload in image_payloads:
        response = await client.post(
            "image",
            files={"image": image_payload["buffer"]},
            params={"product_id": product_payloads[0]["id"]},
        )
        assert response.status_code == 201
        image_payload["buffer"].seek(0)
        created_images.append(
            ImageResponseFull(
                **response.json(),
                **image_payload,
                image=image_payload["buffer"].read(),
            )
        )
    return created_images
