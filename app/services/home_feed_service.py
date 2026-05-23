from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.models.restaurant import Restaurant
from app.models.cart import Cart


class HomeFeedService:

    # PICKED FOR YOU
    @staticmethod
    async def picked_for_you(
        db: AsyncSession
    ):

        result = await db.execute(
            select(Restaurant)
            .limit(5)
        )

        return result.scalars().all()

    # POPULAR NEAR YOU
    @staticmethod
    async def popular_near_you(
        db: AsyncSession
    ):

        result = await db.execute(
            select(Restaurant)
            .limit(10)
        )

        return result.scalars().all()

    # EXPLORE CUISINES
    @staticmethod
    async def cuisines():

        return [
            "Pizza",
            "Burger",
            "Sushi",
            "Asian",
            "Desserts",
            "Indian",
            "Chinese"
        ]

    # FILTERS
    @staticmethod
    async def filtered_restaurants(
        db: AsyncSession,
        cuisine: str = None,
        min_rating: float = None
    ):

        query = select(Restaurant)

        if cuisine:
            query = query.where(
                Restaurant.cuisine_type.ilike(
                    f"%{cuisine}%"
                )
            )

        if min_rating:
            query = query.where(
                Restaurant.rating >= min_rating
            )

        result = await db.execute(
            query
        )

        return result.scalars().all()

    # CART COUNT
    @staticmethod
    async def cart_count(
        db: AsyncSession,
        customer_id
    ):

        result = await db.execute(
            select(Cart).where(
                Cart.customer_id == customer_id
            )
        )

        cart_items = (
            result.scalars().all()
        )

        return len(cart_items)

    # COMPLETE HOME FEED
    @staticmethod
    async def home_feed(
        db: AsyncSession,
        customer_id=None
    ):

        picked = await (
            HomeFeedService
            .picked_for_you(db)
        )

        popular = await (
            HomeFeedService
            .popular_near_you(db)
        )

        cuisines = await (
            HomeFeedService
            .cuisines()
        )

        cart_items = 0

        if customer_id:
            cart_items = await (
                HomeFeedService
                .cart_count(
                    db,
                    customer_id
                )
            )

        return {
            "picked_for_you": picked,
            "explore_cuisines": cuisines,
            "popular_near_you": popular,
            "cart_count": cart_items
        }