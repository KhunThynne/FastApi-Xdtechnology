import strawberry

from app.api.graphql.users.types import UserType


@strawberry.type
class UserQuery:
    @strawberry.field
    def get_users(self) -> list[UserType]:
        return [UserType(id=1, username="KhunThynne", email="[EMAIL_ADDRESS]")]

    @strawberry.field
    def get_user(
        self, id: int | None = None, username: str | None = None
    ) -> UserType | None:
        users = [
            UserType(id=1, username="KhunThynne", email="thynne@example.com"),
            UserType(id=2, username="parns", email="parns@example.com"),
        ]
        if id is not None:
            return next((u for u in users if u.id == id), None)

        if username is not None:
            return next((u for u in users if u.username == username), None)

        return None
