import enum
import uuid

from uuid import UUID

import strawberry

from sqlmodel import Field, SQLModel

from type import StrawberryPydanticBase


class ProductTypeEnum(enum.StrEnum):
    PRO = "pro"
    LITE = "lite"
    FREE = "free"


class ProductBase(SQLModel):
    name: str
    type: ProductTypeEnum  # e.g., "Pro", "Lite"
    duration_days: int


class ProductTable(ProductBase, table=True):
    __tablename__ = "products"
    id: UUID = Field(
        default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False
    )
    name: str = Field(index=True)


@strawberry.experimental.pydantic.type(model=ProductBase, all_fields=True)
class ProductType(StrawberryPydanticBase):
    id: UUID
