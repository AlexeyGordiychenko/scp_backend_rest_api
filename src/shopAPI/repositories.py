from functools import reduce
from typing import Any, Generic, List, Type, TypeVar
from uuid import UUID
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select
from sqlalchemy.orm import joinedload
from sqlmodel import SQLModel

from shopAPI.models import Client, Image, Product, Supplier

ModelType = TypeVar("ModelType", bound=SQLModel)


class BaseRepository(Generic[ModelType]):
    """Base class for data repositories."""

    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.session = session
        self.model_class: Type[ModelType] = model

    async def create(self, attributes: dict[str, Any]) -> ModelType:
        """
        Creates the model instance.

        :param attributes: The attributes to create the model with.
        :return: The created model instance.
        """
        if attributes is None:
            attributes = {}
        model = self.model_class(**attributes)
        self.session.add(model)
        return model

    async def update(self, model: ModelType, attributes: dict[str, Any]) -> ModelType:
        """
        Updated the model instance.

        :param model: The model to update.
        :param attributes: The attributes to update the model with.
        :return: The updated model instance.
        """
        for k, v in attributes.items():
            setattr(model, k, v)
        self.session.add(model)
        return model

    async def get_all(
        self, offset: int = 0, limit: int = 100, join_: set[str] | None = None
    ) -> list[ModelType]:
        """
        Returns a list of model instances.

        :param offset: The number of records to skip.
        :param limit: The number of record to return.
        :param join_: The joins to make.
        :return: A list of model instances.
        """
        query = self._query(join_)
        query = query.offset(offset).limit(limit)

        if join_ is not None:
            return await self._all_unique(query)

        return await self._all(query)

    async def get_by(
        self,
        field: str,
        value: Any,
        join_: set[str] | None = None,
        unique: bool = False,
        for_update: bool = False,
    ) -> ModelType:
        """
        Returns the model instance matching the field and value.

        :param field: The field to match.
        :param value: The value to match.
        :param join_: The joins to make.
        :param unique: Whether to return a unique instance.
        :param for_update: Whether to lock the record for update.
        :return: The model instance.
        """
        query = self._query(join_)
        query = await self._get_by(query, field, value)
        if for_update:
            query = query.with_for_update()
        if unique:
            return await self._one_or_none(query)
        if join_ is not None:
            return await self._all_unique(query)

        return await self._all(query)

    async def delete(self, model: ModelType) -> None:
        """
        Deletes the model.

        :param model: The model to delete.
        :return: None
        """
        await self.session.delete(model)

    def _query(self, join_: set[str] | None = None) -> Select:
        """
        Returns a callable that can be used to query the model.

        :param join_: The joins to make.
        :return: A callable that can be used to query the model.
        """
        query = select(self.model_class)
        query = self._optional_join(query, join_)

        return query

    async def _all(self, query: Select) -> list[ModelType]:
        """
        Returns all results from the query.

        :param query: The query to execute.
        :return: A list of model instances.
        """
        query = await self.session.scalars(query)
        return query.all()

    async def _all_unique(self, query: Select) -> list[ModelType]:
        """
        Returns all unique results from the query

        :param query: The query to execute.
        :return: A list of unique model instances.
        """
        result = await self.session.execute(query)
        return result.unique().scalars().all()

    async def _one_or_none(self, query: Select) -> ModelType | None:
        """Returns the first result from the query or None.

        :param query: The query to execute.
        :return: The model instance or None.
        """
        query = await self.session.scalars(query)
        return query.one_or_none()

    async def _get_by(self, query: Select, field: str, value: Any) -> Select:
        """
        Returns the query filtered by the given column.

        :param query: The query to filter.
        :param field: The column to filter by.
        :param value: The value to filter by.
        :return: The filtered query.
        """
        return query.where(getattr(self.model_class, field) == value)

    def _optional_join(self, query: Select, join_: set[str] | None = None) -> Select:
        """
        Returns the query with the given joins.

        :param query: The query to join.
        :param join_: The joins to make.
        :return: The query with the given joins.
        """
        if not join_:
            return query

        if not isinstance(join_, set):
            raise TypeError("join_ must be a set")

        return reduce(self._add_join_to_query, join_, query)

    def _add_join_to_query(self, query: Select, join_: set[str]) -> Select:
        """
        Returns the query with the given join.

        :param query: The query to join.
        :param join_: The join to make.
        :return: The query with the given join.
        """
        return getattr(self, "_join_" + join_)(query)


class ClientRepository(BaseRepository[Client]):
    """
    Client repository provides all the database operations for the Client model.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=Client, session=session)

    async def get_all(
        self, name: str, surname: str, offset: int, limit: int
    ) -> List[Client] | None:
        query = self._query(join_={"address"})
        if name:
            query = query.filter(Client.client_name == name)
        if surname:
            query = query.filter(Client.client_surname == surname)
        query = query.offset(offset).limit(limit)
        return await self._all_unique(query)

    def _join_address(self, query: Select) -> Select:
        """
        Joins address table.

        :param query: The query to join.
        :return: Query.
        """
        return query.options(joinedload(Client.address)).execution_options(
            contains_joined_collection=True
        )


class SupplierRepository(BaseRepository[Supplier]):
    """
    Supplier repository provides all the database operations for the Supplier model.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=Supplier, session=session)

    async def get_all(
        self, name: str, offset: int, limit: int
    ) -> List[Supplier] | None:
        query = self._query(join_={"address"})
        if name:
            query = query.filter(Supplier.name == name)
        query = query.offset(offset).limit(limit)
        return await self._all_unique(query)

    def _join_address(self, query: Select) -> Select:
        """
        Joins address table.

        :param query: The query to join.
        :return: Query.
        """
        return query.options(joinedload(Supplier.address)).execution_options(
            contains_joined_collection=True
        )


class ProductRepository(BaseRepository[Product]):
    """
    Product repository provides all the database operations for the Product model.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=Product, session=session)

    async def get_all(self, name: str, offset: int, limit: int) -> List[Product] | None:
        query = self._query(join_={"supplier"})
        if name:
            query = query.filter(Product.name == name)
        query = query.offset(offset).limit(limit)
        return await self._all_unique(query)

    def _join_supplier(self, query: Select) -> Select:
        """
        Joins supplier table.

        :param query: The query to join.
        :return: Query.
        """
        return query.options(joinedload(Product.supplier)).execution_options(
            contains_joined_collection=True
        )

    def _join_images(self, query: Select) -> Select:
        """
        Joins images table.

        :param query: The query to join.
        :return: Query.
        """
        return query.options(joinedload(Product.images)).execution_options(
            contains_joined_collection=True
        )


class ImageRepository(BaseRepository[Image]):
    """
    Image repository provides all the database operations for the Image model.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=Image, session=session)

    async def get_all(
        self, product_id: UUID, offset: int, limit: int
    ) -> List[Product] | None:
        query = self._query()
        query = query.filter(Image.product_id == product_id)
        query = query.offset(offset).limit(limit)
        return await self._all_unique(query)
