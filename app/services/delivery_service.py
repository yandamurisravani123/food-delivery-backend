from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.security import hash_password
from app.repositories.delivery_repository import DeliveryAgentRepository
from app.utils.email_utils import send_delivery_approved_email, send_delivery_rejected_email


class DeliveryAgentService:
    @staticmethod
    async def register(session: AsyncSession, payload: dict):
        if payload["password"] != payload["confirm_password"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password and confirm password do not match",
            )

        existing = await DeliveryAgentRepository.get_by_email(session, payload["email"])
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Delivery agent already registered",
            )

        data = payload.copy()
        data.pop("confirm_password")
        data["password_hash"] = hash_password(data.pop("password"))
        data["status"] = "pending"
        data["is_active"] = False

        delivery_agent = await DeliveryAgentRepository.create_delivery_agent(session, data)
        return delivery_agent

    @staticmethod
    async def pending_list(session: AsyncSession):
        return await DeliveryAgentRepository.list_pending(session)

    @staticmethod
    async def approve_delivery_agent(session, delivery_agent_id, approved_by):
        delivery_agent = await DeliveryAgentRepository.get_by_id(
            session, delivery_agent_id
        )

        if not delivery_agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Delivery agent not found",
            )

        if delivery_agent.status == "approved":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Delivery agent already approved",
            )

        approved_delivery_agent = await DeliveryAgentRepository.approve(
            session, delivery_agent, approved_by
        )

        try:
            send_delivery_approved_email(
                to_email=approved_delivery_agent.email,
                full_name=approved_delivery_agent.full_name,
            )
        except Exception:
            pass

        return approved_delivery_agent

    @staticmethod
    async def reject_delivery_agent(session, delivery_agent_id, approved_by):
        delivery_agent = await DeliveryAgentRepository.get_by_id(
            session, delivery_agent_id
        )

        if not delivery_agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Delivery agent not found",
            )

        if delivery_agent.status == "rejected":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Delivery agent already rejected",
            )

        rejected_delivery_agent = await DeliveryAgentRepository.reject(
            session, delivery_agent, approved_by
        )

        try:
            send_delivery_rejected_email(
                to_email=rejected_delivery_agent.email,
                full_name=rejected_delivery_agent.full_name,
            )
        except Exception:
            pass

        return rejected_delivery_agent
    
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