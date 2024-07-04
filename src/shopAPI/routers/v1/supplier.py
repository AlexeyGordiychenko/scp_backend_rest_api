from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query, status

from shopAPI.models import (
    SupplierCreate,
    SupplierUpdate,
    SupplierResponseWithAddress,
    ResponseMessage,
)
from shopAPI.controllers import SupplierController

router = APIRouter(
    prefix="/supplier",
    tags=["Supplier"],
)


@router.post(
    "/",
    summary="Create a new supplier.",
    status_code=status.HTTP_201_CREATED,
    response_model=SupplierResponseWithAddress,
)
async def create_supplier_route(
    data: SupplierCreate, controller: SupplierController = Depends()
) -> SupplierResponseWithAddress:
    return await controller.create(data)


@router.get(
    "/all",
    summary="Get all suppliers with pagination.",
    status_code=status.HTTP_200_OK,
    response_model=List[SupplierResponseWithAddress],
)
async def get_suppliers_all(
    name: str = Query(None, description="Supplier's name."),
    offset: int = Query(0, ge=0, description="Offset for pagination."),
    limit: int = Query(100, gt=0, le=100, description="Number of items to return."),
    controller: SupplierController = Depends(),
) -> List[SupplierResponseWithAddress]:
    return await controller.get_all(name=name, offset=offset, limit=limit)


@router.get(
    "/{id}",
    summary="Get a supplier.",
    status_code=status.HTTP_200_OK,
    response_model=SupplierResponseWithAddress,
    responses={404: {"model": ResponseMessage}},
)
async def get_supplier_route(
    id: UUID, controller: SupplierController = Depends()
) -> SupplierResponseWithAddress:
    return await controller.get_by_id(id=id)


@router.patch(
    "/{id}",
    summary="Update a supplier.",
    status_code=status.HTTP_200_OK,
    response_model=SupplierResponseWithAddress,
)
async def update_supplier_route(
    id: UUID,
    data: SupplierUpdate,
    controller: SupplierController = Depends(),
) -> SupplierResponseWithAddress:
    return await controller.update(await controller.get_by_id(id=id), data)


@router.delete(
    "/{id}",
    summary="Delete a supplier.",
    status_code=status.HTTP_200_OK,
    response_model=Optional[ResponseMessage],
)
async def delete_supplier_route(
    id: UUID, controller: SupplierController = Depends()
) -> Optional[ResponseMessage]:
    return await controller.delete(await controller.get_by_id(id=id))
