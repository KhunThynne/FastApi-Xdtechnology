from collections.abc import Awaitable
from typing import Annotated, Any

from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette import status

from env import _env

security = HTTPBearer(auto_error=False)
STATIC_TOKEN = _env.GRAPHQL_ACCESS_TOKEN


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Security(security)],
) -> dict:
    if not STATIC_TOKEN and _env.APP_ENV == "production":
        raise RuntimeError("GRAPHQL_ACCESS_TOKEN must be set in production!")
    if not STATIC_TOKEN:
        return {"username": "admin", "role": "superuser", "mode": "insecure_bypass"}
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if credentials.credentials != STATIC_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {"username": "admin", "role": "superuser"}


async def get_context(
    user: Annotated[dict[str, str], Depends(get_current_user)],
) -> dict[str, Any] | Awaitable[dict[str, Any]]:
    return {"user": user}
