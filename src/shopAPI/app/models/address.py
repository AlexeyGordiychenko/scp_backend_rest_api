from shopAPI.core.database.mixins.id import IdMixin
from shopAPI.core.schemas.base import AddressBase


class Address(IdMixin, AddressBase, table=True):
    __tablename__ = "address"
