from datetime import UTC, datetime
from uuid import UUID

import strawberry

from sqlalchemy.sql.selectable import Select
from sqlmodel import select

from core.db import async_session_maker
from models.licenses_schema import LicensesTable, LicensesType
from repository.licenses_repo import LicensesRepository
from utils.license import generate_product_key


@strawberry.type
class LicenseMutation:
    @strawberry.mutation
    async def create_license(
        self,
        product_id: UUID,
        key: str | None = None,
    ) -> LicensesType:
        async with async_session_maker() as session:
            final_key = key if key else generate_product_key()

            new_license = LicensesTable(key=final_key, product_id=product_id)

            repo = LicensesRepository(session)
            await repo.add(new_license)
            return LicensesType.from_pydantic(new_license)

    @strawberry.mutation
    async def delete_license(self, id: UUID) -> bool:
        async with async_session_maker() as session:
            repo = LicensesRepository(session)
            license_obj = await repo.get_by_id(id)

            if license_obj:
                return await repo.delete(license_obj)

            return False

    @strawberry.mutation
    async def revoke_license(self, key: str) -> bool:
        async with async_session_maker() as session:
            statement: Select = select(LicensesTable).where(LicensesTable.key == key)
            result = await session.execute(statement)
            license_obj = result.scalars().first()

            if license_obj:
                license_obj.expired_at = datetime.now(UTC)

                session.add(license_obj)
                await session.commit()
                return True

            return False
