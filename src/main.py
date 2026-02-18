from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI
from typeguard import typechecked

from app.api import api_router
from env import _env


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    print("FastAPI is starting up...")
    try:
        from core.db import init_db

        await init_db()
        print("Database connected and tables created successfully.")
    except Exception as e:
        print(f"⚠️ Warning: Could not connect to database: {e}")

    yield
    print("FastAPI is shutting down...")


app = FastAPI(title=_env.APP_NAME, lifespan=lifespan)

app.include_router(api_router)


@app.get("/")
@typechecked
def root() -> dict[str, str]:
    return {"message": "Welcome to Thynne FastAPI"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=_env.HOST,
        port=_env.PORT,
        reload=_env.DEBUG,
    )
