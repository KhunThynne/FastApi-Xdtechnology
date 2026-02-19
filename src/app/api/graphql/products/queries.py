import strawberry

from sqlalchemy.sql.selectable import Select
from sqlmodel import select

from core.db import async_session_maker
from models.products_schema import ProductsTable, ProductsType


@strawberry.type
class ProductsQuery:
    @strawberry.field
    async def get_products(self) -> list[ProductsType]:
        async with async_session_maker() as session:
            statement: Select = select(ProductsTable)
            result = await session.execute(statement)
            products = result.scalars().all()
            return [ProductsType.from_pydantic(p) for p in products if p.id is not None]

    @strawberry.field
    async def get_product(self, id: int) -> ProductsType | None:
        async with async_session_maker() as session:
            statement: Select = select(ProductsTable).where(ProductsTable.id == id)
            result = await session.execute(statement)
            product = result.scalars().first()
            if product and product.id is not None:
                return ProductsType.from_pydantic(product)
            return None
