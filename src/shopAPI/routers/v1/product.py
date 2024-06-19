from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status

from shopAPI.models import (
    ProductCreate,
    ProductResponseWithSupplierId,
    ProductUpdate,
    ErrorMessage,
    ProductUpdateStock,
)
from shopAPI.controllers import ProductController

router = APIRouter(
    prefix="/product",
    tags=["Product"],
)


@router.post(
    "/",
    summary="Create a new product.",
    status_code=status.HTTP_201_CREATED,
    response_model=ProductResponseWithSupplierId,
    responses={404: {"model": ErrorMessage}},
)
async def create_product_route(
    data: ProductCreate, controller: ProductController = Depends()
):
    return await controller.create(data)


@router.get(
    "/all",
    summary="Get all products with pagination.",
    status_code=status.HTTP_200_OK,
    response_model=List[ProductResponseWithSupplierId],
)
async def get_products_all(
    name: str = Query(None, description="Product's name."),
    offset: int = Query(0, ge=0, description="Offset for pagination."),
    limit: int = Query(100, gt=0, le=100, description="Number of items to return."),
    controller: ProductController = Depends(),
):
    return await controller.get_all(name=name, offset=offset, limit=limit)


@router.get(
    "/{id}",
    summary="Get a product.",
    status_code=status.HTTP_200_OK,
    response_model=ProductResponseWithSupplierId,
    responses={404: {"model": ErrorMessage}},
)
async def get_product_route(id: UUID, controller: ProductController = Depends()):
    return await controller.get_by_id(id=id)


@router.patch(
    "/{id}",
    summary="Update product's stock.",
    status_code=status.HTTP_200_OK,
    response_model=ProductResponseWithSupplierId,
    responses={400: {"model": ErrorMessage}},
)
async def update_product_stock_route(
    id: UUID,
    data: ProductUpdateStock,
    controller: ProductController = Depends(),
):
    obj = await controller.get_by_id(id=id, for_update=True)
    new_stock = obj.available_stock - data.amount_to_reduce
    if new_stock < 0:
        raise HTTPException(status_code=400, detail="Not enough stock")
    return await controller.update(obj, ProductUpdate(available_stock=new_stock))


@router.delete(
    "/{id}",
    summary="Delete a product.",
    status_code=status.HTTP_200_OK,
    response_model=bool,
)
async def delete_product_route(id: UUID, controller: ProductController = Depends()):
    return await controller.delete(await controller.get_by_id(id=id))
