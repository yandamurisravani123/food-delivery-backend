from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.restaurant import Restaurant


class SearchService:

    @staticmethod
    async def search_restaurants(
        keyword: str,
        db: AsyncSession
    ):
        stmt = select(Restaurant).where(
            or_(
                Restaurant.restaurant_name.ilike(f"%{keyword}%"),
                Restaurant.cuisine_types.ilike(f"%{keyword}%"),
                Restaurant.city.ilike(f"%{keyword}%"),
                Restaurant.owner_name.ilike(f"%{keyword}%"),
            )
        )
        result = await db.execute(stmt)
        return result.scalars().all()
