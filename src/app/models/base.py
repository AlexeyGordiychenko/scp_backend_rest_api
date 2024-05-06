from sqlmodel import SQLModel, Field
from uuid import UUID
from uuid_extensions import uuid7


class IdMixin(SQLModel):
    id: UUID = Field(
        default_factory=uuid7,
        primary_key=True,
        index=True,
        nullable=False,
    )


class DeleteResponse(SQLModel):
    deleted: int
