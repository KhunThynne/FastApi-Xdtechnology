from uuid import UUID

import strawberry

from core.db import async_session_maker
from models.users_schema import UsersTable, UsersType
from repository.users_repo import UserRepository


@strawberry.type
class UsersMutation:
    @strawberry.mutation
    async def create_user(self, username: str, email: str) -> UsersType:
        async with async_session_maker() as session:
            user_repo = UserRepository(session)
            new_user = UsersTable(username=username, email=email)
            await user_repo.add(new_user)
            return UsersType.from_pydantic(new_user)

    @strawberry.mutation
    async def delete_user(self, id: UUID) -> UUID:
        async with async_session_maker() as session:
            repo = UserRepository(session)
            deleted_id = await repo.get_and_delete(id)
            if deleted_id:
                return deleted_id
            raise Exception(f"User with id {id} not found")
