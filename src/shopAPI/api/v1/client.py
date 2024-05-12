from uuid import UUID
from fastapi import APIRouter, Depends, status

from shopAPI.app.schemas.requests.client import ClientCreate, ClientUpdate
from shopAPI.app.schemas.responses.client import ClientResponse
from shopAPI.app.controllers import ClientController, get_client_controller

router = APIRouter(
    prefix="/client",
    tags=["Client"],
)


@router.post(
    "/",
    summary="Create a new client.",
    status_code=status.HTTP_201_CREATED,
    response_model=ClientResponse,
)
async def create_client_route(
    data: ClientCreate, controller: ClientController = Depends(get_client_controller)
):
    return await controller.create(attributes=data.model_dump())


@router.get(
    "/{id}",
    summary="Get a client.",
    status_code=status.HTTP_200_OK,
    response_model=ClientResponse,
)
async def get_client_route(
    id: UUID, controller: ClientController = Depends(get_client_controller)
):
    return await controller.get_by_id(id=id)


@router.patch(
    "/{id}",
    summary="Update a client.",
    status_code=status.HTTP_200_OK,
    response_model=ClientResponse,
)
async def update_client_route(
    id: UUID,
    data: ClientUpdate,
    controller: ClientController = Depends(get_client_controller),
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
async def delete_client_route(
    id: UUID, controller: ClientController = Depends(get_client_controller)
):
    return await controller.delete(await controller.get_by_id(id=id))
