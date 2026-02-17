# env.py
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv(".env")
load_dotenv(".env.local", override=True)


class Env(BaseSettings):
    APP_NAME: str = "FastApi-Thynne"
    DEBUG: bool = True
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    DATABASE_URL: str = Field(default="")
    # OMISE_PUBLIC_KEY: str = Field(default=None)
    # OMISE_SECRET_KEY: str = Field(default=None)
    # DISCORD_BOT_TOKEN: str = Field(default=None)
    # DISCORD_GUILD_ID: int = Field(default=None)

    class Config:
        pass


_env = Env()


def __getattr__(name: str) -> str:
    return getattr(_env, name)
