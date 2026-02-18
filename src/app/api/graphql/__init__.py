import strawberry

from strawberry.fastapi import GraphQLRouter

from app.api.graphql.security import get_context
from app.api.graphql.users.mutations import UserMutation
from app.api.graphql.users.queries import UserQuery


@strawberry.type
class Query(UserQuery):
    pass


@strawberry.type
class Mutation(UserMutation):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context,  # type: ignore
)
