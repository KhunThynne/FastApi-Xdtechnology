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
            print(licenses[0])
            return [LicenseType.from_pydantic(license) for license in licenses]

    @strawberry.field
    async def get_license(self, key: str) -> LicenseType | None:
        async with async_session_maker() as session:
            statement: Select = select(LicenseTable).where(LicenseTable.key == key)
            result = await session.execute(statement)
            license_obj: LicenseTable | None = result.scalars().first()
            if license_obj:
                return LicenseType.from_pydantic(license_obj)
            return None
