from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

import strawberry

from sqlmodel import Field, SQLModel


@dataclass
class LicenseBase:
    key: str
    product_id: int
    owner_id: UUID | None = None
    activated_at: datetime | None = None
    expired_at: datetime | None = None


class LicenseTable(LicenseBase, SQLModel, table=True):
    __tablename__ = "licenses"
    id: UUID | None = Field(default=None, primary_key=True)
    key: str = Field(primary_key=True)
    product_id: int = Field(foreign_key="producttable.id")
    owner_id: UUID | None = Field(
        default=None, foreign_key="usertable.id", nullable=True
    )


@strawberry.type
@dataclass
class LicenseType(LicenseBase):
    id: UUID | None = None
