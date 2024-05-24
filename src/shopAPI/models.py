from uuid import UUID
from sqlmodel import Field, Relationship, SQLModel
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

    class Config:
        extra = "forbid"


class Address(AddressBase, table=True):
    __tablename__ = "address"
    client_id: UUID | None = Field(
        primary_key=True, index=True, nullable=False, foreign_key="client.id"
    )
    client: "Client" = Relationship(back_populates="address")


class AddressUpdate(AddressBase):
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

    class Config:
        extra = "forbid"


class Client(IdMixin, ClientBase, table=True):
    __tablename__ = "client"
    address: Address | None = Relationship(back_populates="client")

    def __init__(self, **kwargs):
        address_data = kwargs.pop("address", None)
        super().__init__(**kwargs)
        if address_data:
            self.address = Address(**address_data)

    def __setattr__(self, name, value):
        if name == "address" and isinstance(value, dict):
            for attr, val in value.items():
                setattr(self.address, attr, val)
        else:
            super().__setattr__(name, value)


class ClientCreate(ClientBase):
    address: AddressBase


class ClientUpdate(ClientBase):
    client_name: Optional[str] = None
    client_surname: Optional[str] = None
    birthday: Optional[date] = None
    gender: Optional[str] = None
    registration_date: Optional[datetime] = None
    address: Optional[AddressUpdate] = None


class ClientResponse(ClientBase):
    id: UUID


class ClientResponseWithAddress(ClientResponse):
    address: AddressResponse | None = None
