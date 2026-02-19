from uuid import UUID

import strawberry

from sqlalchemy.sql.selectable import Select
from sqlmodel import select

from core.db import async_session_maker
from models.users_schema import UsersTable, UsersType  # Import UserTable มาใช้ Query
from repository.users_repo import UserRepository


@strawberry.type
class UsersQuery:
    @strawberry.field
    async def get_users(self, info: strawberry.Info) -> list[UsersType]:
        async with async_session_maker() as session:
            repo = UserRepository(session)
            users_db = await repo.get_all(limit=100)
            return [UsersType.from_pydantic(u) for u in users_db]

    @strawberry.field
    async def get_user(
        self, info: strawberry.Info, id: UUID | None = None, username: str | None = None
    ) -> UsersType | None:
        async with async_session_maker() as session:
            statement: Select = select(UsersTable)

            if id is not None:
                statement = statement.where(UsersTable.id == id)  #
            elif username is not None:
                statement = statement.where(UsersTable.username == username)  #
            else:
                return None

            result = await session.execute(statement)
            user = result.scalars().first()

            if user:
                return UsersType.from_pydantic(user)
            return None
