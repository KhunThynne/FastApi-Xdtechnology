from datetime import datetime
from enum import StrEnum
from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy.sql.selectable import Select
from sqlmodel import select

from core.db import async_session_maker
from models.licenses_schema import LicensesTable
from models.products_schema import ProductsTable

router = APIRouter(prefix="/license", tags=["License"])


class LicenseStatus(StrEnum):
    VALID = "Valid"
    EXPIRED = "Expired"
    NOT_FOUND = "Not_Found"
    UNAUTHORIZED = "Unauthorized"


class LicenseValidateRequest(BaseModel):
    product_key: str
    user_id: UUID | None = None


class LicenseValidateResponse(BaseModel):
    status: LicenseStatus
    product_type: str | None = None
    remaining_days: int | None = None


@router.post("/validate", response_model=LicenseValidateResponse)
async def validate_license(payload: LicenseValidateRequest) -> LicenseValidateResponse:
    async with async_session_maker() as session:
        statement: Select = select(LicensesTable, ProductsTable).where(
            LicensesTable.key == payload.product_key,
            LicensesTable.product_id == ProductsTable.id,
        )
        result = await session.execute(statement)
        license_data = result.first()

        if not license_data:
            return LicenseValidateResponse(status=LicenseStatus.NOT_FOUND)

        license_obj, product_obj = license_data

        # 1. Check Activation (No Owner)
        if not license_obj.owner_id:
            return LicenseValidateResponse(
                status=LicenseStatus.VALID,
                product_type=product_obj.type,
                remaining_days=product_obj.duration_days,
            )

        # 2. Check Ownership
        if payload.user_id and license_obj.owner_id != payload.user_id:
            return LicenseValidateResponse(
                status=LicenseStatus.UNAUTHORIZED,
                product_type=product_obj.type,
                remaining_days=None,
            )

        if license_obj.owner_id and (
            not payload.user_id or license_obj.owner_id != payload.user_id
        ):
            return LicenseValidateResponse(
                status=LicenseStatus.UNAUTHORIZED,
                product_type=product_obj.type,
                remaining_days=None,
            )

        # 3. Check Expiration
        now = datetime.utcnow()
        if license_obj.expired_at and license_obj.expired_at < now:
            return LicenseValidateResponse(
                status=LicenseStatus.EXPIRED,
                product_type=product_obj.type,
                remaining_days=0,
            )

        remaining = None
        if license_obj.expired_at:
            remaining = (license_obj.expired_at - now).days
            # Ensure non-negative
            remaining = max(0, remaining)

        return LicenseValidateResponse(
            status=LicenseStatus.VALID,
            product_type=product_obj.type,
            remaining_days=remaining,
        )
