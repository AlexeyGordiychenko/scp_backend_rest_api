from asyncio import current_task
from functools import wraps
from uuid import UUID
from uuid_extensions import uuid7

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker
from sqlmodel import Field, SQLModel

from shopAPI.config import settings


class IdMixin(SQLModel):
    id: UUID = Field(
        default_factory=uuid7,
        primary_key=True,
        index=True,
        nullable=False,
    )


class Transactional:
    def __init__(self, refresh: bool = False):
        self.refresh = refresh

    def __call__(self, function):
        @wraps(function)
        async def decorator(*args, **kwargs):
            try:
                result = await function(*args, **kwargs)
                await session.commit()
                if self.refresh:
                    await session.refresh(result)
                return result
            except Exception as exception:
                await session.rollback()
                raise exception

        return decorator


engine = create_async_engine(
    str(settings.POSTGRES_URI),
    echo=settings.POSTGRES_ECHO,
    future=True,
    pool_size=settings.POSTGRES_POOL_SIZE,
)

async_session_factory = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

session = async_scoped_session(
    session_factory=async_session_factory,
    scopefunc=current_task,
)


async def get_session():
    """
    Get the database session.
    This can be used for dependency injection.

    :return: The database session.
    """
    try:
        yield session
    finally:
        await session.close()
