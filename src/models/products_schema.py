import enum
import uuid

from uuid import UUID

import strawberry

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import ENUM
from sqlmodel import Field, SQLModel

from .shared import StrawberryPydanticBase


class ProductsTypeEnum(enum.Enum):
    PRO = "pro"
    LITE = "lite"
    FREE = "free"


class ProductsBase(SQLModel):
    name: str
    type: ProductsTypeEnum  # e.g., "Pro", "Lite"
    duration_days: int


class ProductsTable(ProductsBase, table=True):
    __tablename__ = "products"
    id: UUID = Field(
        default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False
    )
    type: ProductsTypeEnum = Field(
        sa_column=Column(
            ENUM(ProductsTypeEnum, name="producttypeenum", create_type=False),
            nullable=False,
        )
    )


@strawberry.experimental.pydantic.type(model=ProductsBase, all_fields=True)
class ProductsType(StrawberryPydanticBase):
    id: UUID
