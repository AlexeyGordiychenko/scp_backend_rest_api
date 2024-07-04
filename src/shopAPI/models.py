import enum
from uuid import UUID
from pydantic import ConfigDict
from sqlalchemy import LargeBinary
from sqlmodel import Field, Relationship, SQLModel, Column, Enum
from datetime import date
from typing import Any, Dict, Optional
from pydantic_extra_types.phone_numbers import PhoneNumber

from shopAPI.database import IdMixin, TimestampMixin

PhoneNumber.phone_format = "E164"


def field_example(param: Any) -> Dict[str, Dict[str, Any]]:
    """
    Returns field example for swagger documentation

    It's a workaround for SQLModel bug,
    see https://github.com/tiangolo/sqlmodel/discussions/833
    """
    return {"schema_extra": {"json_schema_extra": {"example": param}}}


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
    country: str = Field(**field_example("Australia"))
    city: str = Field(**field_example("Sydney"))
    street: str = Field(**field_example("Bond Street"))

    model_config = ConfigDict(extra="forbid")


class Address(AddressBase, IdMixin, table=True):
    __tablename__ = "address"
    client: "Client" = Relationship(back_populates="address")
    supplier: "Supplier" = Relationship(back_populates="address")


class AddressUpdate(AddressBase):
    country: Optional[str] = Field(None, **field_example("Canada"))
    city: Optional[str] = Field(None, **field_example("Vancouver"))
    street: Optional[str] = Field(None, **field_example("Main Street"))


class AddressResponse(AddressBase): ...


class ClientBase(SQLModel):
    client_name: str = Field(nullable=False, **field_example("John"))
    client_surname: str = Field(nullable=False, **field_example("Doe"))
    birthday: date = Field(nullable=False, **field_example("1990-01-01"))
    gender: Gender = Field(
        sa_column=Column(
            Enum(Gender),
            nullable=False,
        ),
        **field_example("male"),
    )

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
    client_name: Optional[str] = Field(None, **field_example("Jane"))
    client_surname: Optional[str] = Field(None, **field_example("Parker"))
    birthday: Optional[date] = Field(None, **field_example("2000-12-31"))
    gender: Optional[Gender] = Field(None, **field_example("female"))
    address: Optional[AddressUpdate] = None


class ClientResponse(ClientBase):
    id: UUID


class ClientResponseWithAddress(ClientResponse):
    address: AddressResponse | None = None


class SupplierBase(SQLModel):
    name: str = Field(nullable=False, **field_example("Coca-Cola"))
    phone_number: PhoneNumber = Field(nullable=False, **field_example("+12124567890"))

    model_config = ConfigDict(extra="forbid")


class Supplier(IdMixin, SupplierBase, table=True):
    __tablename__ = "supplier"
    address_id: UUID | None = Field(foreign_key="address.id")
    address: Address | None = Relationship(
        sa_relationship_kwargs={"cascade": "all"}, back_populates="supplier"
    )
    products: list["Product"] = Relationship(back_populates="supplier")

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
    name: Optional[str] = Field(None, **field_example("Pepsi"))
    phone_number: Optional[PhoneNumber] = Field(None, **field_example("+12124560987"))
    address: Optional[AddressUpdate] = None


class SupplierResponse(SupplierBase):
    id: UUID


class SupplierResponseWithAddress(SupplierResponse):
    address: AddressResponse | None = None


class ProductBase(SQLModel):
    name: str = Field(nullable=False, **field_example("Diet Coke"))
    category: str = Field(nullable=False, **field_example("Drinks"))
    price: float = Field(nullable=False, **field_example(1.99))
    available_stock: int = Field(nullable=False, **field_example(100))
    last_update_date: date = Field(nullable=False)

    model_config = ConfigDict(extra="forbid")


class Product(IdMixin, ProductBase, table=True):
    __tablename__ = "product"
    supplier_id: UUID = Field(foreign_key="supplier.id")
    supplier: Supplier | None = Relationship(back_populates="products")
    images: list["Image"] = Relationship(back_populates="product")


class ProductCreate(ProductBase):
    supplier_id: UUID


class ProductUpdate(ProductBase):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    available_stock: Optional[int] = None
    last_update_date: Optional[date] = None
    supplier_id: Optional[UUID] = None


class ProductUpdateStock(SQLModel):
    amount_to_reduce: int = Field(nullable=False, gt=0)
    model_config = ConfigDict(extra="forbid")


class ProductResponse(ProductBase):
    id: UUID


class ProductResponseWithSupplierId(ProductResponse):
    supplier_id: UUID


class ImageBase(SQLModel):
    image: bytes = Field(sa_column=Column(LargeBinary, nullable=False))
    extension: str = Field(nullable=False)

    model_config = ConfigDict(extra="forbid")


class Image(IdMixin, ImageBase, table=True):
    __tablename__ = "image"
    product_id: UUID = Field(foreign_key="product.id")
    product: Product = Relationship(back_populates="images")


class ImageCreate(ImageBase):
    product_id: UUID


class ImageUpdate(ImageBase): ...


class ImageResponse(SQLModel):
    id: UUID


class ImageResponseWithProductId(ImageResponse):
    product_id: UUID


class ImageResponseFull(ImageBase, ImageResponseWithProductId):
    model_config = ConfigDict(extra="ignore")
