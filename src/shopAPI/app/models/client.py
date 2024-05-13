from uuid import UUID

from sqlmodel import Field
from shopAPI.core.database.mixins.id import IdMixin
from shopAPI.core.schemas.base import ClientBase


class Client(IdMixin, ClientBase, table=True):
    __tablename__ = "client"

    address_id: UUID | None = Field(default=None, foreign_key="address.id")
