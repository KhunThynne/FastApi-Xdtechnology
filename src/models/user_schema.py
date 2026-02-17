import uuid

from dataclasses import dataclass
from uuid import UUID

import strawberry

from sqlmodel import Field, SQLModel


@dataclass
class UserBase:
    username: str
    email: str


class UserTable(UserBase, SQLModel, table=True):  # type: ignore
    __tablename__ = "users"
    id: UUID = Field(
        default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False
    )
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)


@strawberry.type
@dataclass
class UserType(UserBase):
    id: UUID
