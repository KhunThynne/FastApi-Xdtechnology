import strawberry

from sqlalchemy.sql.selectable import Select
from sqlmodel import select

from core.db import async_session_maker
from models.product_schema import ProductTable, ProductType, ProductTypeEnum


@strawberry.type
class ProductMutation:
    @strawberry.mutation
    async def create_product(
        self, name: str, type: ProductTypeEnum, duration_days: int
    ) -> ProductType:
        try:
            async with async_session_maker() as session:
                new_product = ProductTable(
                    name=name, type=type, duration_days=duration_days
                )
                session.add(new_product)
                await session.commit()
                await session.refresh(new_product)

                # Ensure ID is not None for return type
                if new_product.id is None:
                    raise Exception("Failed to create product")

                return ProductType(
                    id=new_product.id,
                    name=new_product.name,
                    type=new_product.type,
                    duration_days=new_product.duration_days,
                )
        except Exception as e:
            import traceback

            with open("graphql_error.txt", "w") as f:
                traceback.print_exc(file=f)
            raise e

    @strawberry.mutation
    async def delete_product(self, id: int) -> bool:
        async with async_session_maker() as session:
            statement: Select = select(ProductTable).where(ProductTable.id == id)
            result = await session.execute(statement)
            product = result.scalars().first()
            if product:
                await session.delete(product)
                await session.commit()
                return True
            return False
