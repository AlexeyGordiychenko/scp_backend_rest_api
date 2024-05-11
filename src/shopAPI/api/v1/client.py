from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from shopAPI.crud.client import create_client, delete_client, get_client, update_client
from shopAPI.db.session import get_session
from shopAPI.models.base import DeleteResponse
from shopAPI.models.client import ClientCreate, ClientResponse, ClientUpdate

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
    data: ClientCreate,
    db: AsyncSession = Depends(get_session),
):
    return await create_client(session=db, client=data)


@router.get(
    "/{id}",
    summary="Get a client.",
    status_code=status.HTTP_200_OK,
    response_model=ClientResponse,
)
async def get_client_route(id: UUID, db: AsyncSession = Depends(get_session)):
    return await get_client(session=db, id=id)


@router.patch(
    "/{id}",
    summary="Update a client.",
    status_code=status.HTTP_200_OK,
    response_model=ClientResponse,
)
async def update_client_route(
    id: UUID,
    data: ClientUpdate,
    db: AsyncSession = Depends(get_session),
):
    return await update_client(session=db, id=id, client=data)


@router.delete(
    "/{id}",
    summary="Delete a client.",
    status_code=status.HTTP_200_OK,
    response_model=DeleteResponse,
)
async def delete_client_route(id: UUID, db: AsyncSession = Depends(get_session)):
    deleted = await delete_client(session=db, id=id)
    return DeleteResponse(deleted=deleted)
