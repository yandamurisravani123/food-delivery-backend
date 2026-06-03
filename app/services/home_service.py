from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.restaurant import Restaurant


class HomeService:

    @staticmethod
    async def get_home_data(
        db: AsyncSession
    ):

        result = await db.execute(
            select(
                Restaurant.id,
                Restaurant.restaurant_name
            )
        )

        restaurants = result.all()

        data = []

        for restaurant in restaurants:

            data.append({

                "id":
                    str(restaurant.id),

                "restaurant_name":
                    restaurant.restaurant_name
            })

        return {
            "restaurants": data
        }