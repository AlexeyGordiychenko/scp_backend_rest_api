from uuid import UUID

from sqlmodel import Field
from shopAPI.database import IdMixin
from shopAPI.schemas import AddressBase, ClientBase


class Client(IdMixin, ClientBase, table=True):
    __tablename__ = "client"

    address_id: UUID | None = Field(default=None, foreign_key="address.id")


class Address(IdMixin, AddressBase, table=True):
    __tablename__ = "address"
