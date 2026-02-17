import asyncio
import os
import sys
from uuid import uuid4

from fastapi.testclient import TestClient
from sqlmodel import select

# Add src to sys.path
sys.path.append(os.path.join(os.getcwd(), "src"))

from core.db import async_session_maker, init_db
from main import app
from models.license_schema import LicenseTable
from models.product_schema import ProductTable
from models.user_schema import UserTable

# Use TestClient as context manager to trigger lifespan
client = TestClient(app)


async def setup_data():
    await init_db()
    async with async_session_maker() as session:
        # Create User
        user = UserTable(
            username=f"test_lic_{uuid4().hex[:8]}",
            email=f"test_lic_{uuid4().hex[:8]}@example.com",
        )
        session.add(user)

        # Create Product
        product = ProductTable(name="Test Product", type="Pro", duration_days=30)
        session.add(product)
        await session.commit()
        await session.refresh(user)
        await session.refresh(product)

        # Create License (Ready)
        lic_ready = LicenseTable(
            key=f"KEY-READY-{uuid4().hex[:4]}", product_id=product.id
        )
        session.add(lic_ready)

        # Create License (Owned)
        lic_owned = LicenseTable(
            key=f"KEY-OWNED-{uuid4().hex[:4]}", product_id=product.id, owner_id=user.id
        )
        session.add(lic_owned)

        await session.commit()
        await session.refresh(lic_ready)
        await session.refresh(lic_owned)

        return user, product, lic_ready, lic_owned


async def verify():
    print("Setting up data...")
    user, product, lic_ready, lic_owned = await setup_data()

    print("\n1. Test Not Found")
    with TestClient(app) as client:
        resp = client.post("/api/license/validate", json={"product_key": "INVALID-KEY"})
        print(f"Status: {resp.status_code}")
        print(resp.json())
        assert resp.json()["status"] == "Not_Found"

        print("\n2. Test Ready (No Owner)")
        resp = client.post(
            "/api/license/validate",
            json={"product_key": lic_ready.key, "user_id": str(user.id)},
        )
        print(resp.json())
        assert resp.json()["status"] == "Valid"
        assert resp.json()["remaining_days"] == 30

        print("\n3. Test Owned (Correct Owner)")
        resp = client.post(
            "/api/license/validate",
            json={"product_key": lic_owned.key, "user_id": str(user.id)},
        )
        print(resp.json())
        assert resp.json()["status"] == "Valid"

        print("\n4. Test Owned (Wrong Owner)")
        resp = client.post(
            "/api/license/validate",
            json={"product_key": lic_owned.key, "user_id": str(uuid4())},
        )
        print(resp.json())
        assert resp.json()["status"] == "Unauthorized"

    print("\nVerification Passed!")


if __name__ == "__main__":
    asyncio.run(verify())
