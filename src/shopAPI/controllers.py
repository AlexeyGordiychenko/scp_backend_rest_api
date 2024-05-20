from typing import Any, Generic, Type, TypeVar
from uuid import UUID

from fastapi import Depends, HTTPException
from pydantic import BaseModel

from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession

from shopAPI.database import Transactional
from shopAPI.database import get_session
from shopAPI.models import Client
from shopAPI.repositories import BaseRepository, ClientRepository

ModelType = TypeVar("ModelType", bound=SQLModel)


class BaseController(Generic[ModelType]):
    """Base class for data controllers."""

    def __init__(self, model: Type[ModelType], repository: BaseRepository):
        self.model_class = model
        self.repository = repository

    async def get_by_id(self, id: UUID, join_: set[str] | None = None) -> ModelType:
        """
        Returns the model instance matching the id.

        :param id: The id to match.
        :param join_: The joins to make.
        :return: The model instance.
        """

        db_obj = await self.repository.get_by(
            field="id", value=id, join_=join_, unique=True
        )
        if not db_obj:
            raise HTTPException(status_code=404, detail="Client not found")

        return db_obj

    async def get_all(
        self, skip: int = 0, limit: int = 100, join_: set[str] | None = None
    ) -> list[ModelType]:
        """
        Returns a list of records based on pagination params.

        :param skip: The number of records to skip.
        :param limit: The number of records to return.
        :param join_: The joins to make.
        :return: A list of records.
        """

        response = await self.repository.get_all(skip, limit, join_)
        return response

    @Transactional()
    async def create(self, model_create: ModelType) -> ModelType:
        """
        Creates a new Object in the DB.

        :param attributes: The attributes to create the object with.
        :return: The created object.
        """
        create = await self.repository.create(
            self.extract_attributes_from_schema(model_create)
        )
        return create

    @Transactional(refresh=True)
    async def update(self, model: ModelType, attributes: dict[str, Any]) -> ModelType:
        """
        Updates an Object in the DB.

        :param id: The id to match.
        :param attributes: The attributes to create the object with.
        :return: The updated object.
        """
        update = await self.repository.update(model, attributes)
        return update

    @Transactional()
    async def delete(self, model: ModelType) -> bool:
        """
        Deletes the Object from the DB.

        :param model: The model to delete.
        :return: True if the object was deleted, False otherwise.
        """
        await self.repository.delete(model)
        return True

    @staticmethod
    def extract_attributes_from_schema(
        schema: BaseModel, excludes: set = None
    ) -> dict[str, Any]:
        """
        Extracts the attributes from the schema.

        :param schema: The schema to extract the attributes from.
        :param excludes: The attributes to exclude.
        :return: The attributes.
        """

        return schema.model_dump(exclude=excludes, exclude_unset=True)


class ClientController(BaseController[Client]):
    def __init__(self, repository: ClientRepository = Depends()):
        super().__init__(model=Client, repository=repository)
