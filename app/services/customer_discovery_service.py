from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from app.models.restaurant import Restaurant
from app.models.menu_item import MenuItem


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
                    Restaurant.restaurant_name.ilike(f"%{query}%"),
                    Restaurant.city.ilike(f"%{query}%"),
                    Restaurant.cuisine_types.ilike(f"%{query}%")
                )
            )
        )

        restaurants = restaurants_result.scalars().all()

        menu_result = await db.execute(
            select(MenuItem).where(
                or_(
                    MenuItem.item_name.ilike(f"%{query}%"),
                    MenuItem.description.ilike(f"%{query}%"),
                    MenuItem.category.ilike(f"%{query}%"),
                    MenuItem.tags.ilike(f"%{query}%")
                )
            )
        )

        menu_items = menu_result.scalars().all()

        return {
            "success": True,
            "count": len(restaurants) + len(menu_items),
            "restaurants": [
                {
                    "id": str(restaurant.id),
                    "restaurant_name": restaurant.restaurant_name,
                    "city": restaurant.city,
                    "cuisine_types": restaurant.cuisine_types,
                    "is_active": restaurant.is_active,
                    "is_trending": restaurant.is_trending,
                    "is_top_rated": restaurant.is_top_rated
                }
                for restaurant in restaurants
            ],
            "menu_items": [
                {
                    "id": str(menu_item.id),
                    "item_name": menu_item.item_name,
                    "restaurant_id": str(menu_item.restaurant_id),
                    "category": menu_item.category,
                    "tags": menu_item.tags,
                    "is_available": menu_item.is_available,
                    "image_url": menu_item.image_url
                }
                for menu_item in menu_items
            ]
        }

    # CUISINE FILTER
    @staticmethod
    async def cuisine_filter(
        db: AsyncSession,
        cuisine: str
    ):

        result = await db.execute(
            select(Restaurant).where(
                Restaurant.cuisine_types.ilike(
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
            select(Restaurant).where(
                Restaurant.is_trending == True
            )
        )

        restaurants = result.scalars().all()

        return {
            "success": True,
            "count": len(restaurants),
            "data": [
                {
                    "id": str(restaurant.id),
                    "restaurant_name": restaurant.restaurant_name,
                    "city": restaurant.city,
                    "cuisine_types": restaurant.cuisine_types,
                    "is_active": restaurant.is_active,
                    "is_trending": restaurant.is_trending,
                    "is_top_rated": restaurant.is_top_rated
                }
                for restaurant in restaurants
            ]
        }

    @staticmethod
    async def top_rated(
        db: AsyncSession
    ):

        result = await db.execute(
            select(Restaurant).where(
                Restaurant.is_top_rated == True
            )
        )

        restaurants = result.scalars().all()

        return {
            "success": True,
            "count": len(restaurants),
            "data": [
                {
                    "id": str(restaurant.id),
                    "restaurant_name": restaurant.restaurant_name,
                    "city": restaurant.city,
                    "cuisine_types": restaurant.cuisine_types,
                    "is_active": restaurant.is_active,
                    "is_trending": restaurant.is_trending,
                    "is_top_rated": restaurant.is_top_rated
                }
                for restaurant in restaurants
            ]
        }