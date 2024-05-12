from shopAPI.core.database.mixins.id import IdMixin
from shopAPI.core.schemas.base import ClientBase


class Client(IdMixin, ClientBase, table=True):
    __tablename__ = "client"
