import enum
from uuid import UUID
from pydantic import ConfigDict
from sqlmodel import Field, Relationship, SQLModel, Column, Enum
from datetime import date
from typing import Optional
from pydantic_extra_types.phone_numbers import PhoneNumber

from shopAPI.database import IdMixin, TimestampMixin

PhoneNumber.phone_format = "E164"


class Gender(str, enum.Enum):
    female = "female"
    male = "male"
    other = "other"
    not_given = "not given"


class ApiStatus(SQLModel):
    name: str = Field(...)
    version: str = Field(...)
    status: str = Field(...)
    message: str = Field(...)
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "ShopAPI",
                    "version": "1.0.0",
                    "status": "OK",
                    "message": "Visit /swagger for documentation.",
                },
            ]
        }
    )


class ErrorMessage(SQLModel):
    detail: str


class AddressBase(SQLModel):
    country: str
    city: str
    street: str

    model_config = ConfigDict(extra="forbid")


class Address(AddressBase, IdMixin, table=True):
    __tablename__ = "address"
    client: "Client" = Relationship(back_populates="address")
    supplier: "Supplier" = Relationship(back_populates="address")


class AddressUpdate(AddressBase):
    country: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None


class AddressResponse(AddressBase): ...


class ClientBase(SQLModel):
    client_name: str = Field(nullable=False)
    client_surname: str = Field(nullable=False)
    birthday: date = Field(nullable=False)
    gender: Gender = Field(sa_column=Column(Enum(Gender), nullable=False))

    model_config = ConfigDict(extra="forbid")


class Client(IdMixin, TimestampMixin, ClientBase, table=True):
    __tablename__ = "client"
    address_id: UUID | None = Field(foreign_key="address.id")
    address: Address | None = Relationship(
        sa_relationship_kwargs={"cascade": "all"}, back_populates="client"
    )

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
    gender: Optional[Gender] = None
    address: Optional[AddressUpdate] = None


class ClientResponse(ClientBase):
    id: UUID


class ClientResponseWithAddress(ClientResponse):
    address: AddressResponse | None = None


class SupplierBase(SQLModel):
    name: str = Field(nullable=False)
    phone_number: PhoneNumber = Field(nullable=False)

    model_config = ConfigDict(extra="forbid")


class Supplier(IdMixin, SupplierBase, table=True):
    __tablename__ = "supplier"
    address_id: UUID | None = Field(foreign_key="address.id")
    address: Address | None = Relationship(
        sa_relationship_kwargs={"cascade": "all"}, back_populates="supplier"
    )

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


class SupplierCreate(SupplierBase):
    address: AddressBase


class SupplierUpdate(SupplierBase):
    name: Optional[str] = None
    phone_number: Optional[PhoneNumber] = None
    address: Optional[AddressUpdate] = None


class SupplierResponse(SupplierBase):
    id: UUID


class SupplierResponseWithAddress(SupplierResponse):
    address: AddressResponse | None = None
