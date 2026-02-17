import strawberry

from core.db import async_session_maker
from models.user_schema import UserTable, UserType


@strawberry.type
class UserMutation:
    @strawberry.mutation
    async def create_user(self, username: str, email: str) -> UserType:
        async with async_session_maker() as session:
            new_user = UserTable(username=username, email=email)
            session.add(new_user)
            await session.commit()

            await session.refresh(new_user)

            return UserType(
                id=new_user.id,
                username=new_user.username,
                email=new_user.email,
            )

    @strawberry.mutation
    async def delete_user(self, id: int) -> int:
        async with async_session_maker() as session:
            user = await session.get(UserTable, id)
            if user:
                await session.delete(user)
                await session.commit()

                if user.id is not None:
                    return user.id

            raise Exception(f"User with id {id} not found")
