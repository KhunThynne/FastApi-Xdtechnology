from uuid import UUID

import strawberry

from sqlalchemy.sql.selectable import Select
from sqlmodel import select

from core.db import async_session_maker
from models.licenses_schema import LicensesTable, LicensesType
from repository.licenses_repo import LicensesRepository


@strawberry.type
class LicensesQuery:
    @strawberry.field
    async def get_licenses(self) -> list[LicensesType]:
        async with async_session_maker() as session:
            repo = LicensesRepository(session)
            licenses = await repo.get_all(limit=100)
            return [LicensesType.from_pydantic(li) for li in licenses]

    @strawberry.field
    async def get_license_by_product_id(self, product_id: UUID) -> LicensesType | None:
        async with async_session_maker() as session:
            statement: Select = select(LicensesTable).where(
                LicensesTable.product_id == product_id
            )
            result = await session.execute(statement)
            license_obj: LicensesTable | None = result.scalars().first()
            if license_obj:
                return LicensesType.from_pydantic(license_obj)
            return None

    @strawberry.field
    async def get_license(self, key: str) -> LicensesType | None:
        async with async_session_maker() as session:
            statement: Select = select(LicensesTable).where(LicensesTable.key == key)
            result = await session.execute(statement)
            license_obj: LicensesTable | None = result.scalars().first()
            if license_obj:
                return LicensesType.from_pydantic(license_obj)
            return None
