import strawberry

from sqlalchemy.sql.selectable import Select
from sqlmodel import select

from core.db import async_session_maker
from models.license_schema import LicenseTable, LicenseType


@strawberry.type
class LicenseQuery:
    @strawberry.field
    async def get_licenses(self) -> list[LicenseType]:
        async with async_session_maker() as session:
            statement: Select = select(LicenseTable)
            result = await session.execute(statement)
            licenses = result.scalars().all()
            return [
                LicenseType(
                    key=l.key,
                    product_id=l.product_id,
                    owner_id=l.owner_id,
                    activated_at=l.activated_at,
                    expired_at=l.expired_at,
                )
                for l in licenses  # noqa: E741
            ]

    @strawberry.field
    async def get_license(self, key: str) -> LicenseType | None:
        async with async_session_maker() as session:
            statement: Select = select(LicenseTable).where(LicenseTable.key == key)
            result = await session.execute(statement)
            license_obj = result.scalars().first()
            if license_obj:
                return LicenseType(
                    key=license_obj.key,
                    product_id=license_obj.product_id,
                    owner_id=license_obj.owner_id,
                    activated_at=license_obj.activated_at,
                    expired_at=license_obj.expired_at,
                )
            return None
