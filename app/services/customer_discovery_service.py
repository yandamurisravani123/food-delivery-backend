from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from app.models.restaurant import Restaurant
from app.models.menu import MenuItem


class CustomerDiscoveryService:

    # SEARCH RESTAURANTS + FOOD ITEMS
    @staticmethod
    async def search(
        db: AsyncSession,
        query: str
    ):

        restaurants_result = await db.execute(
            select(Restaurant).where(
                or_(
                    Restaurant.restaurant_name.ilike(
                        f"%{query}%"
                    )
                )
            )
        )

        restaurants = (
            restaurants_result.scalars().all()
        )

        menu_result = await db.execute(
            select(MenuItem).where(
                or_(
                    MenuItem.item_name.ilike(
                        f"%{query}%"
                    )
                )
            )
        )

        menu_items = (
            menu_result.scalars().all()
        )

        return {
            "restaurants": restaurants,
            "menu_items": menu_items
        }

    # CUISINE FILTER
    @staticmethod
    async def cuisine_filter(
        db: AsyncSession,
        cuisine: str
    ):

        result = await db.execute(
            select(Restaurant).where(
                Restaurant.cuisine_type.ilike(
                    f"%{cuisine}%"
                )
            )
        )

        return result.scalars().all()

    # TRENDING RESTAURANTS
    @staticmethod
    async def trending_restaurants(
        db: AsyncSession
    ):

        result = await db.execute(
            select(Restaurant)
        )

        return result.scalars().all()

    # TOP RATED RESTAURANTS
    @staticmethod
    async def top_rated(
        db: AsyncSession
    ):

        result = await db.execute(
            select(Restaurant)
        )

        return result.scalars().all()