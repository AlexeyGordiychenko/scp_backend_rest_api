from typing import Optional

from shopAPI.core.schemas.base import AddressBase


class AddressCreate(AddressBase): ...


class AddressUpdate(AddressBase):
    country: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None
