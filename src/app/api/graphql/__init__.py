from collections.abc import Awaitable
from typing import Annotated, Any

import strawberry

from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette import status
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
from env import _env

security = HTTPBearer()
STATIC_TOKEN = _env.GRAPHQL_ACCESS_TOKEN


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Security(security)],
) -> dict:
    if credentials.credentials != STATIC_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"username": "admin", "role": "superuser"}


@strawberry.type
class Query(UserQuery, ProductQuery, LicenseQuery):
    pass


@strawberry.type
class Mutation(UserMutation, ProductMutation, LicenseMutation):
    pass


async def get_context(
    user: Annotated[dict[str, str], Depends(get_current_user)],
) -> dict[str, Any] | Awaitable[dict[str, Any]]:
    return {"user": user}


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context,  # type: ignore
)
