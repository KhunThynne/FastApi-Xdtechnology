import strawberry

from strawberry.fastapi import GraphQLRouter

# Licenses
from app.api.graphql.licenses.mutations import LicenseMutation
from app.api.graphql.licenses.queries import LicensesQuery

# Products
from app.api.graphql.products.mutations import ProductsMutation
from app.api.graphql.products.queries import ProductsQuery
from app.api.graphql.security import get_context

# Test
from app.api.graphql.test import TestQuery

# Users
from app.api.graphql.users.mutations import UsersMutation
from app.api.graphql.users.queries import UsersQuery


@strawberry.type
class Query(UsersQuery, ProductsQuery, LicensesQuery, TestQuery):
    pass


@strawberry.type
class Mutation(UsersMutation, ProductsMutation, LicenseMutation):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context,  # type: ignore
)
