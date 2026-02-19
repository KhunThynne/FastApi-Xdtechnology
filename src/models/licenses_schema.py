from datetime import datetime
from uuid import UUID, uuid4

import strawberry

from sqlmodel import Field, SQLModel

from .shared import StrawberryPydanticBase


class LicensesBase(SQLModel):
    key: str
    product_id: UUID
    owner_id: UUID | None = None
    activated_at: datetime | None = None
    expired_at: datetime | None = None


class LicensesTable(LicensesBase, table=True):
    __tablename__ = "licenses"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    product_id: UUID = Field(foreign_key="products.id", unique=True, nullable=False)
    key: str = Field(nullable=False, unique=True)


@strawberry.experimental.pydantic.type(model=LicensesBase, all_fields=True)
class LicensesType(StrawberryPydanticBase):
    id: UUID
