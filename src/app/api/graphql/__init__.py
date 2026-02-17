import strawberry

from strawberry.fastapi import GraphQLRouter

# Licenses
from app.api.graphql.licenses.mutations import LicenseMutation
from app.api.graphql.licenses.queries import LicenseQuery

# Products
from app.api.graphql.products.mutations import ProductMutation
from app.api.graphql.products.queries import ProductQuery

# Users
from app.api.graphql.users.mutations import UserMutation
from app.api.graphql.users.queries import UserQuery


@strawberry.type
class Query(UserQuery, ProductQuery, LicenseQuery):
    pass


@strawberry.type
class Mutation(UserMutation, ProductMutation, LicenseMutation):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)
