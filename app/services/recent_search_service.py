from sqlalchemy import (
    select,
    delete
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.models.recent_search import (
    RecentSearch
)


class RecentSearchService:

    @staticmethod
    async def get_recent_searches(
        db: AsyncSession
    ):

        result = await db.execute(
            select(RecentSearch)
        )

        return result.scalars().all()

    @staticmethod
    async def add_recent_search(
        keyword: str,
        db: AsyncSession
    ):

        recent_search = RecentSearch(
            keyword=keyword
        )

        db.add(recent_search)

        await db.commit()

        await db.refresh(
            recent_search
        )

        return recent_search

    @staticmethod
    async def clear_recent_searches(
        db: AsyncSession
    ):

        await db.execute(
            delete(RecentSearch)
        )

        await db.commit()

        return {
            "message":
            "All recent searches cleared"
        }