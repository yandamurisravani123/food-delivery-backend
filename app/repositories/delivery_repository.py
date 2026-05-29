from alembic.util import status
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.delivery import DeliveryAgent


class DeliveryAgentRepository:
    @staticmethod
    async def get_by_email(session: AsyncSession, email: str):
        result = await session.execute(
            select(DeliveryAgent).where(DeliveryAgent.email == email)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_id(session: AsyncSession, delivery_agent_id: int):
        result = await session.execute(
            select(DeliveryAgent).where(DeliveryAgent.id == delivery_agent_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create_delivery_agent(session: AsyncSession, data: dict):
        delivery_agent = DeliveryAgent(**data)

        session.add(delivery_agent)
        await session.commit()
        await session.refresh(delivery_agent)

        return delivery_agent

    @staticmethod
    async def list_pending(session: AsyncSession):
        result = await session.execute(
            select(DeliveryAgent).where(DeliveryAgent.status == "pending")
        )
        return result.scalars().all()

    @staticmethod
    async def approve(session: AsyncSession, delivery_agent: DeliveryAgent, approved_by: int):
        from datetime import datetime, timezone

        delivery_agent.status = "approved"
        delivery_agent.is_active = True
        delivery_agent.approved_by = approved_by
        delivery_agent.approved_at = datetime.now(timezone.utc)

        await session.commit()
        await session.refresh(delivery_agent)

        return delivery_agent

    @staticmethod
    async def reject(session: AsyncSession, delivery_agent: DeliveryAgent, approved_by: int):
        delivery_agent.status = "rejected"
        delivery_agent.is_active = False
        delivery_agent.approved_by = approved_by

        await session.commit()
        await session.refresh(delivery_agent)

        return delivery_agent
    
    @staticmethod
    async def get_all_delivery_agents(session):
        return await DeliveryAgentRepository.get_all(session)

    @staticmethod
    async def get_delivery_agent_by_id(session, delivery_agent_id):
        delivery_agent = await DeliveryAgentRepository.get_by_id(
            session,
            delivery_agent_id,
        )

        if not delivery_agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Delivery agent not found",
            )

        return delivery_agent
    
    @staticmethod
    async def get_all(session):
        result = await session.execute(select(DeliveryAgent))
        return result.scalars().all()

    @staticmethod
    async def get_by_id(session, delivery_agent_id):
        result = await session.execute(
            select(DeliveryAgent).where(
                DeliveryAgent.id == delivery_agent_id
            )
        )
        return result.scalar_one_or_none()