from uuid import UUID

from alembic.util import status
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.restaurant import Restaurant


class RestaurantRepository:
    @staticmethod
    async def get_by_id(session: AsyncSession, restaurant_id: int):
        result = await session.execute(
            select(Restaurant).where(Restaurant.id == restaurant_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_owner_email(session: AsyncSession, owner_email: str):
        result = await session.execute(
            select(Restaurant).where(Restaurant.owner_email == owner_email)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create_restaurant(session: AsyncSession, data: dict):
        restaurant = Restaurant(**data)
        session.add(restaurant)
        await session.commit()
        await session.refresh(restaurant)
        return restaurant

    @staticmethod
    async def list_pending(session: AsyncSession):
        result = await session.execute(
            select(Restaurant).where(Restaurant.status == "pending")
        )
        return result.scalars().all()

    @staticmethod
    async def approve_restaurant(session: AsyncSession, restaurant: Restaurant, approved_by: int):
        restaurant.status = "approved"
        restaurant.is_active = True
        restaurant.approved_by = approved_by
        from datetime import datetime, timezone
        restaurant.approved_at = datetime.now(timezone.utc)

        await session.commit()
        await session.refresh(restaurant)
        return restaurant

    @staticmethod
    async def reject_restaurant(session: AsyncSession, restaurant: Restaurant, approved_by: int):
        restaurant.status = "rejected"
        restaurant.is_active = False
        restaurant.approved_by = approved_by

        await session.commit()
        await session.refresh(restaurant)
        return restaurant
    @staticmethod
    async def get_all_restaurants(session):
        return await RestaurantRepository.get_all(session)

    @staticmethod
    async def get_restaurant_by_id(session, restaurant_id):
        restaurant = await RestaurantRepository.get_by_id(
            session,
            restaurant_id,
        )

        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found",
            )

        return restaurant
    
    @staticmethod
    async def get_all(session):
        result = await session.execute(select(Restaurant))
        return result.scalars().all()

    @staticmethod
    async def get_by_id(session, restaurant_id: UUID):
        result = await session.execute(
            select(Restaurant).where(Restaurant.id == restaurant_id)
        )
        return result.scalar_one_or_none()