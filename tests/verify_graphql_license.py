import asyncio
import os
import sys

# Add src to sys.path
sys.path.append(os.path.join(os.getcwd(), "src"))

from app.api.graphql import schema

async def verify_graphql() -> None:
    print("Verifying GraphQL License Schema...")

    # 1. Create Product
    mutation_create_product = """
        mutation {
            createProduct(name: "GQL Product", type: PRO, durationDays: 365) {
                id
                name
                type
            }
        }
    """
    print("\n1. Executing Create Product Mutation:")
    result = await schema.execute(mutation_create_product)
    if result.errors:
        print("Error:", result.errors)
        sys.exit(1)
    print("Result:", result.data)
    product_id = result.data["createProduct"]["id"]

    # 2. Create License
    mutation_create_license = f"""
        mutation {{
            createLicense(key: "GQL-KEY-123", productId: {product_id}) {{
                key
                productId
                ownerId
            }}
        }}
    """
    print("\n2. Executing Create License Mutation:")
    result = await schema.execute(mutation_create_license)
    if result.errors:
        print("Error:", result.errors)
        sys.exit(1)
    print("Result:", result.data)

    # 3. Query License
    query_license = """
        query {
            getLicense(key: "GQL-KEY-123") {
                key
                productId
                ownerId
            }
        }
    """
    print("\n3. Executing Get License Query:")
    result = await schema.execute(query_license)
    if result.errors:
        print("Error:", result.errors)
        sys.exit(1)
    print("Result:", result.data)
    
    # 4. Query All Products
    query_products = """
        query {
            getProducts {
                id
                name
            }
        }
    """
    print("\n4. Executing Get Products Query:")
    result = await schema.execute(query_products)
    if result.errors:
        print("Error:", result.errors)
        sys.exit(1)
    print("Result:", result.data)

    print("\nGraphQL Verification Successful!")


if __name__ == "__main__":
    from core.db import init_db
    
    async def main():
        # Initialize DB to ensure tables exist
        await init_db()
        await verify_graphql()
        
    # Use a single asyncio.run call
    asyncio.run(main())
