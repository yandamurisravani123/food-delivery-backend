# app/repositories/cuisine_repository.py

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.cuisine import Cuisine


class CuisineRepository:

    @staticmethod
    async def create_cuisine(
        session: AsyncSession,
        data: dict
    ):
        cuisine = Cuisine(**data)

        session.add(cuisine)

        await session.commit()

        await session.refresh(cuisine)

        return cuisine