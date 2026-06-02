from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
 
from app.models.restaurant import Restaurant
from app.models.cart import Cart
 
 
class HomeFeedService:
 
    # BANNERS
    @staticmethod
    async def banners():
 
        return [
            {
                "title": "50% OFF",
                "image": "banner1.png"
            },
            {
                "title": "Free Delivery",
                "image": "banner2.png"
            }
        ]
 
    # PICKED FOR YOU
    @staticmethod
    async def picked_for_you(
        db: AsyncSession
    ):
 
        result = await db.execute(
            select(Restaurant).limit(5)
        )
 
        return result.scalars().all()
 
    # POPULAR NEAR YOU
    @staticmethod
    async def popular_near_you(
        db: AsyncSession
    ):
 
        result = await db.execute(
            select(Restaurant).limit(10)
        )
 
        return result.scalars().all()
 
    # TRENDING
    @staticmethod
    async def trending_restaurants(
        db: AsyncSession
    ):
 
        result = await db.execute(
            select(Restaurant).limit(8)
        )
 
        return result.scalars().all()
 
    # CUISINES
    @staticmethod
    async def cuisines():
 
        return [
            "Pizza",
            "Burger",
            "Asian",
            "Healthy",
            "Desserts",
            "Indian",
            "Chinese"
        ]
 
    # OFFERS
    @staticmethod
    async def offers():
 
        return [
            {
                "title": "50% OFF",
                "coupon_code": "SAVE50"
            },
            {
                "title": "Free Delivery",
                "coupon_code": "FREEDEL"
            }
        ]
 
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
 
        return {
            "cart_count": len(cart_items)
        }
 
    # COMPLETE HOME FEED
    @staticmethod
    async def home_feed(
        db: AsyncSession,
        customer_id=None
    ):
 
        return {
            "banners": await HomeFeedService.banners(),
            "picked_for_you":
                await HomeFeedService
                .picked_for_you(db),
 
            "popular_near_you":
                await HomeFeedService
                .popular_near_you(db),
 
            "trending_restaurants":
                await HomeFeedService
                .trending_restaurants(db),
 
            "cuisines":
                await HomeFeedService
                .cuisines(),
 
            "offers":
                await HomeFeedService
                .offers(),
 
            "cart_count":
                await HomeFeedService
                .cart_count(
                    db,
                    customer_id
                ) if customer_id else 0
        }