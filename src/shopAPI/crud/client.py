from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import delete, select

from shopAPI.app.models.client import Client
from shopAPI.app.schemas.requests.client import ClientCreate, ClientUpdate


async def create_client(session: AsyncSession, client: ClientCreate) -> Client:
    db_client = Client(**client.model_dump())
    try:
        session.add(db_client)
        await session.commit()
        await session.refresh(db_client)
        return db_client
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail="Client already exists",
        )


async def get_client(session: AsyncSession, id: UUID) -> Client:
    query = select(Client).where(Client.id == id)
    response = await session.execute(query)
    return response.scalar_one_or_none()


async def update_client(
    session: AsyncSession, id: UUID, client: ClientUpdate
) -> Client:
    db_client = await get_client(session, id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")

    for k, v in client.model_dump(exclude_unset=True).items():
        setattr(db_client, k, v)

    try:
        await session.commit()
        await session.refresh(db_client)
        return db_client
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail="Updated client collides with other clients",
        )


async def delete_client(session: AsyncSession, id: UUID) -> int:
    query = delete(Client).where(Client.id == id)
    response = await session.execute(query)
    await session.commit()
    return response.rowcount
