from uuid import UUID
from sqlmodel import Field, SQLModel
from datetime import date, datetime
from typing import Optional

from shopAPI.database import IdMixin


class ApiStatus(SQLModel):
    name: str = Field(..., schema_extra={"example": "ShopAPI"})
    version: str = Field(..., schema_extra={"example": "1.0.0"})
    status: str = Field(..., schema_extra={"example": "OK"})
    message: str = Field(
        ..., schema_extra={"example": "Visit /swagger for documentation."}
    )


class AddressBase(SQLModel):
    country: str
    city: str
    street: str


class AddressCreate(AddressBase):
    client_id: UUID


class AddressUpdate(AddressCreate):
    country: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None


class AddressResponse(AddressBase): ...


class ClientBase(SQLModel):
    client_name: str = Field(nullable=False)
    client_surname: str = Field(nullable=False)
    birthday: date = Field(nullable=False)
    # TODO: Add gender constraint
    gender: str = Field(nullable=False, regex="^(M|F)$")
    registration_date: datetime = Field(nullable=False)


class ClientCreate(ClientBase):
    address: AddressBase


class ClientUpdate(ClientBase):
    client_name: Optional[str] = None
    client_surname: Optional[str] = None
    birthday: Optional[date] = None
    gender: Optional[str] = None
    registration_date: Optional[datetime] = None


class ClientResponse(ClientBase):
    id: UUID


class Client(IdMixin, ClientBase, table=True):
    __tablename__ = "client"


class Address(IdMixin, AddressBase, table=True):
    __tablename__ = "address"
    client_id: UUID | None = Field(
        primary_key=True, index=True, nullable=False, foreign_key="client.id"
    )
