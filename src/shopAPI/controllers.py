import io
from typing import Any, Generic, List, Type, TypeVar
from uuid import UUID
import zipfile
from fastapi import Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession
from PIL import Image as PILImage
from shopAPI.database import Transactional, get_session
from shopAPI.models import (
    Client,
    Image,
    Product,
    ProductUpdateStock,
    Supplier,
)
from shopAPI.repositories import (
    BaseRepository,
    ClientRepository,
    ImageRepository,
    ProductRepository,
    SupplierRepository,
)

ModelType = TypeVar("ModelType", bound=SQLModel)


class BaseController(Generic[ModelType]):
    """Base class for data controllers."""

    def __init__(self, model: Type[ModelType], repository: BaseRepository):
        self.model_class = model
        self.repository = repository

    async def get_by_id(
        self, id: UUID, join_: set[str] | None = None, for_update: bool = False
    ) -> ModelType:
        """
        Returns the model instance matching the id.

        :param id: The id to match.
        :param join_: The joins to make.
        :return: The model instance.
        """

        db_obj = await self.repository.get_by(
            field="id", value=id, join_=join_, unique=True, for_update=for_update
        )
        if not db_obj:
            raise HTTPException(
                status_code=404, detail=f"{self.model_class.__name__} not found"
            )

        return db_obj

    async def get_all(
        self, offset: int = 0, limit: int = 100, join_: set[str] | None = None
    ) -> list[ModelType]:
        """
        Returns a list of records based on pagination params.

        :param skip: The number of records to skip.
        :param limit: The number of records to return.
        :param join_: The joins to make.
        :return: A list of records.
        """

        response = await self.repository.get_all(offset, limit, join_)
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

    @Transactional()
    async def update(self, model: ModelType, model_update: ModelType) -> ModelType:
        """
        Updates an Object in the DB.

        :param id: The id to match.
        :param attributes: The attributes to create the object with.
        :return: The updated object.
        """
        update = await self.repository.update(
            model, model_update.model_dump(exclude_unset=True)
        )
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
    def __init__(self, session: AsyncSession = Depends(get_session)):
        super().__init__(model=Client, repository=ClientRepository(session=session))

    async def get_by_id(self, id: UUID) -> ModelType:
        return await super().get_by_id(id=id, join_={"address"})

    async def get_all(
        self, name: str, surname: str, offset: int, limit: int
    ) -> List[ModelType]:
        db_objs = await self.repository.get_all(
            name=name, surname=surname, offset=offset, limit=limit
        )

        return db_objs


class SupplierController(BaseController[Supplier]):
    def __init__(self, session: AsyncSession = Depends(get_session)):
        super().__init__(model=Supplier, repository=SupplierRepository(session=session))

    async def get_by_id(self, id: UUID) -> ModelType:
        return await super().get_by_id(id=id, join_={"address"})

    async def get_all(self, name: str, offset: int, limit: int) -> List[ModelType]:
        db_objs = await self.repository.get_all(name=name, offset=offset, limit=limit)

        return db_objs


class ProductController(BaseController[Product]):
    def __init__(
        self,
        session: AsyncSession = Depends(get_session),
        supplier: SupplierController = Depends(),
    ):
        super().__init__(model=Product, repository=ProductRepository(session=session))
        self.supplier = supplier

    @Transactional()
    async def create(self, model_create: Product) -> Product:
        await self.supplier.get_by_id(model_create.supplier_id)
        return await super().create(model_create)

    @Transactional()
    async def update(self, model: ModelType, model_update: ModelType) -> ModelType:
        if model_update.supplier_id:
            await self.supplier.get_by_id(model_update.supplier_id)
        return await super().update(model, model_update)

    async def get_by_id(self, id: UUID, for_update: bool = False) -> ModelType:
        if for_update:
            return await super().get_by_id(id=id, for_update=for_update)
        else:
            return await super().get_by_id(id=id, join_={"supplier"})

    async def get_all(self, name: str, offset: int, limit: int) -> List[ModelType]:
        db_objs = await self.repository.get_all(name=name, offset=offset, limit=limit)

        return db_objs


class ImageController(BaseController[Image]):
    def __init__(
        self,
        session: AsyncSession = Depends(get_session),
        product: ProductController = Depends(),
    ):
        super().__init__(model=Image, repository=ImageRepository(session=session))
        self.product = product

    @Transactional()
    async def create(self, model_create: ModelType) -> ModelType:
        await self.product.get_by_id(model_create.product_id)
        try:
            img = PILImage.open(io.BytesIO(model_create.image))
            img.verify()
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid image")
        return await super().create(model_create)

    async def get_all_images_by_product_id(
        self, product_id: UUID, offset: int, limit: int
    ) -> List[ModelType]:
        await self.product.get_by_id(product_id)
        db_objs = await self.repository.get_all(
            product_id=product_id, offset=offset, limit=limit
        )

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zf:
            for image in db_objs:
                zf.writestr(f"{image.id}.{image.extension}", image.image)
        zip_buffer.seek(0)

        return f"{product_id}.zip", zip_buffer.getvalue()
