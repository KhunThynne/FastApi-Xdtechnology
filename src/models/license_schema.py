from datetime import datetime
from uuid import UUID, uuid4

import strawberry

from sqlmodel import Field, SQLModel

from type import StrawberryPydanticBase


class LicenseBase(SQLModel):
    key: str
    product_id: UUID
    owner_id: UUID | None = None
    activated_at: datetime | None = None
    expired_at: datetime | None = None


class LicenseTable(LicenseBase, table=True):
    __tablename__ = "licenses"
    id: UUID = Field(default_factory=uuid4, primary_key=True)


@strawberry.experimental.pydantic.type(model=LicenseBase, all_fields=True)
class LicenseType(StrawberryPydanticBase):
    id: UUID
