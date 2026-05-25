from sqlalchemy import select

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.models.restaurant import Restaurant

from app.models.filter import Filter

from app.models.recent_search import (
    RecentSearch
)

from app.models.user_location import (
    UserLocation
)


class HomeService:

    @staticmethod
    async def get_home_data(
        db: AsyncSession
    ):

        location_result = await db.execute(
            select(UserLocation)
        )

        filter_result = await db.execute(
            select(Filter)
        )

        recent_result = await db.execute(
            select(RecentSearch)
        )

        trending_result = await db.execute(
            select(Restaurant).where(
                Restaurant.is_trending == True
            )
        )

        top_result = await db.execute(
            select(Restaurant).where(
                Restaurant.is_top_rated == True
            )
        )

        return {
            "location":
                location_result.scalars().first(),

            "filters":
                filter_result.scalars().all(),

            "recent_searches":
                recent_result.scalars().all(),

            "trending_restaurants":
                trending_result.scalars().all(),

            "top_rated_restaurants":
                top_result.scalars().all()
        }