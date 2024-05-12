from sqlalchemy import Select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from shopAPI.app.models import Client
from shopAPI.core.repository import BaseRepository


class ClientRepository(BaseRepository[Client]):
    """
    Client repository provides all the database operations for the Client model.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=Client, session=session)

    def _join_address(self, query: Select) -> Select:
        """
        Join address.

        :param query: Query.
        :return: Query.
        """
        return query.options(joinedload(Client.address)).execution_options(
            contains_joined_collection=True
        )
