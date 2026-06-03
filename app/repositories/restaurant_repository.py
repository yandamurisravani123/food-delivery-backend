from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.restaurant import Restaurant
from app.models.review import Review


class RestaurantRepository:

    # Create Restaurant
    @staticmethod
    async def create_restaurant(
        session: AsyncSession,
        data: dict
    ):
        restaurant = Restaurant(**data)

        session.add(restaurant)

        await session.commit()
        await session.refresh(restaurant)

        return restaurant

    # Get Restaurant By ID
    @staticmethod
    async def get_by_id(
        session: AsyncSession,
        restaurant_id: UUID
    ):
        result = await session.execute(
            select(Restaurant).where(
                Restaurant.id == restaurant_id
            )
        )

        return result.scalar_one_or_none()

    # Get Restaurant By Owner Email
    @staticmethod
    async def get_by_owner_email(
        session: AsyncSession,
        owner_email: str
    ):
        result = await session.execute(
            select(Restaurant).where(
                Restaurant.owner_email == owner_email
            )
        )

        return result.scalar_one_or_none()

    # Get All Restaurants
    @staticmethod
    async def get_all(
        session: AsyncSession
    ):
        result = await session.execute(
            select(Restaurant)
        )

        return result.scalars().all()

    # Get Pending Restaurants
    @staticmethod
    async def list_pending(
        session: AsyncSession
    ):
        result = await session.execute(
            select(Restaurant).where(
                Restaurant.status == "pending"
            )
        )

        return result.scalars().all()

    # Approve Restaurant
    @staticmethod
    async def approve_restaurant(
        session: AsyncSession,
        restaurant: Restaurant,
        approved_by: UUID
    ):
        from datetime import datetime, timezone

        restaurant.status = "approved"
        restaurant.is_active = True
        restaurant.approved_by = approved_by
        restaurant.approved_at = datetime.now(timezone.utc)

        await session.commit()
        await session.refresh(restaurant)

        return restaurant

    # Reject Restaurant
    @staticmethod
    async def reject_restaurant(
        session: AsyncSession,
        restaurant: Restaurant,
        approved_by: UUID
    ):
        restaurant.status = "rejected"
        restaurant.is_active = False
        restaurant.approved_by = approved_by

        await session.commit()
        await session.refresh(restaurant)

        return restaurant

    # Get Restaurant Reviews
    @staticmethod
    async def get_restaurant_reviews(
        session: AsyncSession,
        restaurant_id: UUID
    ):
        result = await session.execute(
            select(Review).where(
                Review.restaurant_id == restaurant_id
            )
        )

        return result.scalars().all()

    # Helper - Get Restaurant Or Raise
    @staticmethod
    async def get_restaurant_by_id(
        session: AsyncSession,
        restaurant_id: UUID
    ):
        restaurant = await RestaurantRepository.get_by_id(
            session,
            restaurant_id
        )

        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found"
            )

        return restaurant