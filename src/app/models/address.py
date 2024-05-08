from typing import Optional
from sqlmodel import SQLModel

from models.base import IdMixin


class AddressBase(SQLModel):
    country: str
    city: str
    street: str


class AddressCreate(AddressBase):
    pass


class AddressUpdate(AddressBase):
    country: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None


class Address(IdMixin, AddressBase, table=True):
    __tablename__ = "address"


class AddressResponse(Address, table=False):
    pass
