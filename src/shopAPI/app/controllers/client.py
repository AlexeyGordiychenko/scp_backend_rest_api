from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from shopAPI.core.controller import BaseController
from shopAPI.app.models.client import Client
from shopAPI.app.repositories import ClientRepository
from shopAPI.core.database.session import get_session


class ClientController(BaseController[Client]):
    def __init__(self, repository: ClientRepository):
        super().__init__(model=Client, repository=repository)


def get_client_controller(
    session: AsyncSession = Depends(get_session),
) -> ClientController:
    return ClientController(repository=ClientRepository(session=session))
