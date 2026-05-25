from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.password_token import PasswordResetToken
from app.models.user import User
from app.models.restaurant import Restaurant
from app.models.delivery import DeliveryAgent


class AuthRepository:
    @staticmethod
    async def get_user_by_email(session: AsyncSession, email: str):
        result = await session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_id(session: AsyncSession, user_id: int):
        result = await session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_restaurant_by_email(session: AsyncSession, email: str):
        result = await session.execute(
            select(Restaurant).where(Restaurant.owner_email == email)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_restaurant_by_id(session: AsyncSession, restaurant_id: int):
        result = await session.execute(
            select(Restaurant).where(Restaurant.id == restaurant_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_delivery_agent_by_email(session: AsyncSession, email: str):
        result = await session.execute(
            select(DeliveryAgent).where(DeliveryAgent.email == email)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_delivery_agent_by_id(session: AsyncSession, delivery_agent_id: int):
        result = await session.execute(
            select(DeliveryAgent).where(DeliveryAgent.id == delivery_agent_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create_user(
        session: AsyncSession,
        full_name: str,
        email: str,
        phone: str | None,
        hashed_password: str,
        role: str,
        is_verified: bool,
        is_active: bool,
        is_super_admin: bool,
    ):
        user = User(
            full_name=full_name,
            email=email,
            phone=phone,
            hashed_password=hashed_password,
            role=role,
            is_verified=is_verified,
            is_active=is_active,
            is_super_admin=is_super_admin,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def create_reset_token(session: AsyncSession, entity_type: str, entity_id, token_hash: str, expires_at):
        reset_token = PasswordResetToken(
            entity_type=entity_type,
            entity_id=entity_id,
            token_hash=token_hash,
            expires_at=expires_at,
            is_used=False,
        )
        session.add(reset_token)
        await session.commit()
        await session.refresh(reset_token)
        return reset_token

    @staticmethod
    async def get_reset_token_by_hash(session: AsyncSession, token_hash: str):
        result = await session.execute(
            select(PasswordResetToken).where(PasswordResetToken.token_hash == token_hash)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def mark_reset_token_used(session: AsyncSession, reset_token: PasswordResetToken):
        from datetime import datetime, timezone
        reset_token.is_used = True
        reset_token.used_at = datetime.now(timezone.utc)
        await session.commit()
        await session.refresh(reset_token)
        return reset_token

    @staticmethod
    async def update_user_password(session: AsyncSession, user: User, hashed_password: str):
        user.hashed_password = hashed_password
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def update_restaurant_password(session: AsyncSession, restaurant: Restaurant, hashed_password: str):
        restaurant.password_hash = hashed_password
        await session.commit()
        await session.refresh(restaurant)
        return restaurant

    @staticmethod
    async def update_delivery_agent_password(session: AsyncSession, delivery_agent: DeliveryAgent, hashed_password: str):
        delivery_agent.password_hash = hashed_password
        await session.commit()
        await session.refresh(delivery_agent)
        return delivery_agent