from typing import Optional

from datetime import date, datetime

from shopAPI.core.schemas.base import ClientBase, AddressBase


class ClientCreate(ClientBase):
    address: AddressBase


class ClientUpdate(ClientBase):
    client_name: Optional[str] = None
    client_surname: Optional[str] = None
    birthday: Optional[date] = None
    gender: Optional[str] = None
    registration_date: Optional[datetime] = None
