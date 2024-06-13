from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, Query, status

from shopAPI.models import (
    ClientCreate,
    ClientUpdate,
    ClientResponseWithAddress,
    ErrorMessage,
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
    "/all",
    summary="Get all clients with pagination.",
    status_code=status.HTTP_200_OK,
    response_model=List[ClientResponseWithAddress],
)
async def get_clients_all(
    name: str = Query(None, description="Client's name."),
    surname: str = Query(None, description="Client's surname."),
    offset: int = Query(0, ge=0, description="Offset for pagination."),
    limit: int = Query(100, gt=0, le=100, description="Number of items to return."),
    controller: ClientController = Depends(),
):
    return await controller.get_all(
        name=name, surname=surname, offset=offset, limit=limit
    )


@router.get(
    "/{id}",
    summary="Get a client.",
    status_code=status.HTTP_200_OK,
    response_model=ClientResponseWithAddress,
    responses={404: {"model": ErrorMessage}},
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
    return await controller.update(await controller.get_by_id(id=id), data)


@router.delete(
    "/{id}",
    summary="Delete a client.",
    status_code=status.HTTP_200_OK,
    response_model=bool,
)
async def delete_client_route(id: UUID, controller: ClientController = Depends()):
    return await controller.delete(await controller.get_by_id(id=id))
