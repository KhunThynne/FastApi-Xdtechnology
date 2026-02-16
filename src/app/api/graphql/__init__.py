import strawberry

from app.api.graphql.users.queries import UserQuery
from strawberry.fastapi import GraphQLRouter


@strawberry.type
class Query(UserQuery):
    pass


schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)
