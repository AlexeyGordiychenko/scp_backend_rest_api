from typing import Optional

from datetime import date, datetime
from uuid import UUID

from shopAPI.core.schemas.base import ClientBase


class ClientCreate(ClientBase): ...


class ClientUpdate(ClientBase):
    client_name: Optional[str] = None
    client_surname: Optional[str] = None
    birthday: Optional[date] = None
    gender: Optional[str] = None
    registration_date: Optional[datetime] = None
    # address_id: Optional[UUID] = None
