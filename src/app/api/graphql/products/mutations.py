import strawberry

from sqlalchemy.sql.selectable import Select
from sqlmodel import select

from core.db import async_session_maker
from models.products_schema import ProductsTable, ProductsType, ProductsTypeEnum


@strawberry.type
class ProductsMutation:
    @strawberry.mutation
    async def create_product(
        self, name: str, type: ProductsTypeEnum, duration_days: int | None = 0
    ) -> ProductsType:
        try:
            async with async_session_maker() as session:
                new_product = ProductsTable(
                    name=name, type=type, duration_days=duration_days
                )
                session.add(new_product)
                await session.commit()
                await session.refresh(new_product)
                # Ensure ID is not None for return type
                if new_product.id is None:
                    raise Exception("Failed to create product")

                return ProductsType.from_pydantic(new_product)
        except Exception as e:
            import traceback

            with open("graphql_error.txt", "w") as f:
                traceback.print_exc(file=f)
            raise e

    @strawberry.mutation
    async def delete_product(self, id: int) -> bool:
        async with async_session_maker() as session:
            statement: Select = select(ProductsTable).where(ProductsTable.id == id)
            result = await session.execute(statement)
            product = result.scalars().first()
            if product:
                await session.delete(product)
                await session.commit()
                return True
            return False
