from sqlmodel import Field, SQLModel
from datetime import date, datetime


class ClientBase(SQLModel):
    client_name: str = Field(nullable=False)
    client_surname: str = Field(nullable=False)
    birthday: date = Field(nullable=False)
    # TODO: Add gender constraint
    gender: str = Field(nullable=False, regex="^(M|F)$")
    registration_date: datetime = Field(nullable=False)


class AddressBase(SQLModel):
    country: str
    city: str
    street: str
