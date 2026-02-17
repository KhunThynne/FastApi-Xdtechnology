import strawberry

from sqlalchemy.sql.selectable import Select
from sqlmodel import select

from models.user_schema import UserTable, UserType  # Import UserTable มาใช้ Query


@strawberry.type
class UserQuery:
    @strawberry.field
    async def get_users(self, info: strawberry.Info) -> list[UserType]:
        from core.db import async_session_maker

        async with async_session_maker() as session:
            statement: Select = select(UserTable)
            result = await session.execute(statement)
            users_db = result.scalars().all()
            return [
                UserType(id=u.id, username=u.username, email=u.email) for u in users_db
            ]

    @strawberry.field
    async def get_user(
        self, info: strawberry.Info, id: int | None = None, username: str | None = None
    ) -> UserType | None:
        from core.db import async_session_maker

        async with async_session_maker() as session:
            statement: Select = select(UserTable)

            if id is not None:
                statement = statement.where(UserTable.id == id)  #
            elif username is not None:
                statement = statement.where(UserTable.username == username)  #
            else:
                return None

            result = await session.execute(statement)
            user = result.scalars().first()

            if user:
                return UserType(id=user.id, username=user.username, email=user.email)
            return None
