from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import date, datetime
from uuid import UUID

from models.base import IdMixin


class ClientBase(SQLModel):
    client_name: str = Field(nullable=False)
    client_surname: str = Field(nullable=False)
    birthday: date = Field(nullable=False)
    # TODO: Add gender constraint
    gender: str = Field(nullable=False, regex="^(M|F)$")
    registration_date: datetime = Field(nullable=False)
    # address_id: UUID = Field(nullable=False, foreign_key="address.id")


class ClientCreate(ClientBase): ...


class ClientUpdate(ClientBase):
    client_name: Optional[str] = None
    client_surname: Optional[str] = None
    birthday: Optional[date] = None
    gender: Optional[str] = None
    registration_date: Optional[datetime] = None
    # address_id: Optional[UUID] = None


class Client(IdMixin, ClientBase, table=True):
    __tablename__ = "client"


class ClientResponse(Client, table=False): ...
