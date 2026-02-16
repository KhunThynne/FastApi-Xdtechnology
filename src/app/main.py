from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn

from api import api_router
from env import _env
from fastapi import FastAPI
from typeguard import typechecked

# DATABASE_URL = "postgresql://root:root@localhost:5432/fastapi_db"
# engine = create_engine(DATABASE_URL, echo=True)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # --- Code to run on startup ---
    print("FastAPI is starting up...")
    # สร้าง task ให้บอทรันใน background
    # asyncio.create_task(client.start(DISCORD_BOT_TOKEN))
    # await client.wait_until_ready()
    # print(f"Bot '{client.user}' is ready!")

    yield  # <--- แอปพลิเคชันจะทำงาน ณ จุดนี้

    # --- Code to run on shutdown (ถ้ามี) ---
    print("FastAPI is shutting down, closing bot connection...")
    # await client.close()


app = FastAPI(title="Thynne FastAPI")

app.include_router(api_router)


@app.get("/")
@typechecked
def root() -> dict[str, str]:
    return {"message": "Welcome to Thynne FastAPI"}


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=_env.HOST,
        port=_env.PORT,
        reload=_env.DEBUG,
    )
