from dataclasses import dataclass

import strawberry

from strawberry.fastapi import GraphQLRouter


@strawberry.type
@dataclass
class UserType:
    id: int
    username: str
    email: str


@strawberry.type
class Query:
    @strawberry.field
    def get_users(self) -> list[UserType]:
        return [UserType(id=1, username="KhunThynne", email="thynne@example.com")]


# 3. สร้าง Schema และ Router
schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)
