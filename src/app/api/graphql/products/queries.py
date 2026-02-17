import strawberry

from sqlalchemy.sql.selectable import Select
from sqlmodel import select

from core.db import async_session_maker
from models.product_schema import ProductTable, ProductType


@strawberry.type
class ProductQuery:
    @strawberry.field
    async def get_products(self) -> list[ProductType]:
        async with async_session_maker() as session:
            statement: Select = select(ProductTable)
            result = await session.execute(statement)
            products = result.scalars().all()
            return [
                ProductType(
                    id=p.id,
                    name=p.name,
                    type=p.type,
                    duration_days=p.duration_days,
                )
                for p in products
                if p.id is not None
            ]

    @strawberry.field
    async def get_product(self, id: int) -> ProductType | None:
        async with async_session_maker() as session:
            statement: Select = select(ProductTable).where(ProductTable.id == id)
            result = await session.execute(statement)
            product = result.scalars().first()
            if product and product.id is not None:
                return ProductType(
                    id=product.id,
                    name=product.name,
                    type=product.type,
                    duration_days=product.duration_days,
                )
            return None
