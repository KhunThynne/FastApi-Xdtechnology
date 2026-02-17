from datetime import datetime

import strawberry

from sqlalchemy.sql.selectable import Select
from sqlmodel import select

from core.db import async_session_maker
from models.license_schema import LicenseTable, LicenseType


@strawberry.type
class LicenseMutation:
    @strawberry.mutation
    async def create_license(self, key: str, product_id: int) -> LicenseType:
        async with async_session_maker() as session:
            new_license = LicenseTable(key=key, product_id=product_id)
            session.add(new_license)
            await session.commit()
            await session.refresh(new_license)
            return LicenseType(
                key=new_license.key,
                product_id=new_license.product_id,
                owner_id=new_license.owner_id,
                activated_at=new_license.activated_at,
                expired_at=new_license.expired_at,
            )

    @strawberry.mutation
    async def revoke_license(self, key: str) -> bool:
        async with async_session_maker() as session:
            statement: Select = select(LicenseTable).where(LicenseTable.key == key)
            result = await session.execute(statement)
            license_obj = result.scalars().first()
            if license_obj:
                # Set expired_at to now to maximize revocability or just delete?
                # Usually revoke means expire immediately.
                license_obj.expired_at = datetime.utcnow()
                session.add(license_obj)
                await session.commit()
                return True
            return False
