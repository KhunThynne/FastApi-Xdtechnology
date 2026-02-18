import uuid

from uuid import UUID

import strawberry

from sqlmodel import Field, SQLModel

from type import StrawberryPydanticBase


class UserBase(SQLModel):
    username: str
    email: str


class UserTable(UserBase, table=True):
    __tablename__ = "users"
    id: UUID = Field(
        default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False
    )
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)


@strawberry.experimental.pydantic.type(model=UserBase, all_fields=True)
class UserType(StrawberryPydanticBase):
    id: UUID
