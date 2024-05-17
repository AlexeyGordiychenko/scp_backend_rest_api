from contextvars import ContextVar, Token
from functools import wraps
from typing import Union
from uuid import UUID
from uuid_extensions import uuid7

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql.expression import Delete, Insert, Update
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


session_context: ContextVar[str] = ContextVar("session_context")


def get_session_context() -> str:
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)


def get_engine():
    return create_async_engine(
        str(settings.POSTGRES_URI),
        echo=settings.POSTGRES_ECHO,
        future=True,
        pool_size=settings.POSTGRES_POOL_SIZE,
    )


engines = {
    "writer": get_engine(),
    "reader": get_engine(),
}


class RoutingSession(Session):
    def get_bind(self, mapper=None, clause=None, **kwargs):
        if self._flushing or isinstance(clause, (Update, Delete, Insert)):
            return engines["writer"].sync_engine
        return engines["reader"].sync_engine


async_session_factory = sessionmaker(
    class_=AsyncSession,
    sync_session_class=RoutingSession,
    expire_on_commit=False,
)

session: Union[AsyncSession, async_scoped_session] = async_scoped_session(
    session_factory=async_session_factory,
    scopefunc=get_session_context,
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
