import asyncio
from sqlalchemy import select

from app.config.database import AsyncSessionLocal
from app.config.security import hash_password
from app.models.restaurant import Restaurant


DEMO_RESTAURANTS = [
    {
        "restaurant_name": "Demo Pizza Place",
        "owner_name": "Demo Owner 1",
        "owner_email": "demo1@example.com",
        "owner_phone": "1111111111",
        "password": "Password123!",
        "restaurant_phone": "2222222222",
        "address_line1": "123 Demo St",
        "city": "DemoCity",
        "state": "DemoState",
        "pincode": "000001",
    },
    {
        "restaurant_name": "Demo Sushi Bar",
        "owner_name": "Demo Owner 2",
        "owner_email": "demo2@example.com",
        "owner_phone": "3333333333",
        "password": "Password123!",
        "restaurant_phone": "4444444444",
        "address_line1": "456 Demo Ave",
        "city": "DemoCity",
        "state": "DemoState",
        "pincode": "000002",
    },
]


async def seed():
    async with AsyncSessionLocal() as session:
        created = []
        for r in DEMO_RESTAURANTS:
            # check existing by owner_email
            q = await session.execute(select(Restaurant).where(Restaurant.owner_email == r["owner_email"]))
            existing = q.scalar_one_or_none()
            if existing:
                existing.is_trending = True
                existing.is_active = True
                existing.status = "approved"
                await session.commit()
                await session.refresh(existing)
                created.append(existing)
                print(f"Updated existing restaurant as trending: {existing.owner_email} -> {existing.id}")
            else:
                restaurant = Restaurant(
                    restaurant_name=r["restaurant_name"],
                    owner_name=r["owner_name"],
                    owner_email=r["owner_email"],
                    owner_phone=r["owner_phone"],
                    password_hash=hash_password(r["password"]),
                    restaurant_phone=r["restaurant_phone"],
                    address_line1=r["address_line1"],
                    city=r["city"],
                    state=r["state"],
                    pincode=r["pincode"],
                    is_trending=True,
                    is_active=True,
                    status="approved",
                )

                session.add(restaurant)
                await session.commit()
                await session.refresh(restaurant)
                created.append(restaurant)
                print(f"Created restaurant: {restaurant.owner_email} -> {restaurant.id}")

        print(f"Total trending restaurants ensured: {len(created)}")


if __name__ == "__main__":
    asyncio.run(seed())
