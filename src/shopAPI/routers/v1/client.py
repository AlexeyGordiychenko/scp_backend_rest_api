from uuid import UUID
from fastapi import APIRouter, Depends, status

from shopAPI.models import (
    ClientCreate,
    ClientUpdate,
    ClientResponseWithAddress,
)
from shopAPI.controllers import ClientController

router = APIRouter(
    prefix="/client",
    tags=["Client"],
)


@router.post(
    "/",
    summary="Create a new client.",
    status_code=status.HTTP_201_CREATED,
    response_model=ClientResponseWithAddress,
)
async def create_client_route(
    data: ClientCreate, controller: ClientController = Depends()
):
    return await controller.create(data)


@router.get(
    "/{id}",
    summary="Get a client.",
    status_code=status.HTTP_200_OK,
    response_model=ClientResponseWithAddress,
)
async def get_client_route(id: UUID, controller: ClientController = Depends()):
    return await controller.get_by_id(id=id)


@router.patch(
    "/{id}",
    summary="Update a client.",
    status_code=status.HTTP_200_OK,
    response_model=ClientResponseWithAddress,
)
async def update_client_route(
    id: UUID,
    data: ClientUpdate,
    controller: ClientController = Depends(),
):
    return await controller.update(
        await controller.get_by_id(id=id),
        attributes=data.model_dump(exclude_unset=True),
    )


@router.delete(
    "/{id}",
    summary="Delete a client.",
    status_code=status.HTTP_200_OK,
    response_model=bool,
)
async def delete_client_route(id: UUID, controller: ClientController = Depends()):
    return await controller.delete(await controller.get_by_id(id=id))