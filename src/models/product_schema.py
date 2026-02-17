import enum

from dataclasses import dataclass

import strawberry

from sqlmodel import Field, SQLModel


class ProductTypeEnum(enum.StrEnum):
    PRO = "pro"
    LITE = "lite"
    FREE = "free"


@dataclass
class ProductBase:
    name: str
    type: ProductTypeEnum  # e.g., "Pro", "Lite"
    duration_days: int


class ProductTable(ProductBase, SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)


@strawberry.type
@dataclass
class ProductType(ProductBase):
    id: int
