# Register routes
# from api.discord import discord_router
# from api.omise import omise_router
from fastapi import APIRouter

from app.api.graphql import graphql_app

api_router = APIRouter(prefix="/api")
api_router.include_router(graphql_app, prefix="/graphql")
# api_router.include_router(omise_router)
# api_router.include_router(discord_router)
