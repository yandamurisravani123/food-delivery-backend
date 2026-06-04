from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.security import hash_password
from app.repositories.delivery_repository import DeliveryAgentRepository
from app.utils.email_utils import send_delivery_approved_email, send_delivery_rejected_email
import uuid
from sqlalchemy import select
from app.models.delivery import (
    DeliveryAgent,
    DriverStats,
    DriverOrder,
    DriverShift,
    PeakHourBonus,
    EarningsBoost,
    DriverChallenge,
    DriverHotspot
)

# app/services/delivery_service.py

from fastapi import HTTPException, status
from app.repositories.delivery_repository import DeliveryAgentRepository
from app.models.delivery import DeliveryAgent



from fastapi import HTTPException, status

from app.models.delivery import DeliveryAgent
from app.repositories.delivery_repository import DeliveryAgentRepository


class DeliveryAgentService:

    @staticmethod
    async def register(session, payload):
        pass

    @staticmethod
    async def pending_list(session):
        return await DeliveryAgentRepository.list_pending(session)

    @staticmethod
    async def approve_delivery_agent(
        session,
        delivery_agent_id,
        approved_by
    ):
        pass

    @staticmethod
    async def reject_delivery_agent(
        session,
        delivery_agent_id,
        approved_by
    ):
        pass

    @staticmethod
    async def get_all_delivery_agents(session):
        return await DeliveryAgentRepository.get_all(session)

    @staticmethod
    async def get_delivery_agent_by_id(
        session,
        delivery_agent_id
    ):
        delivery_agent = await DeliveryAgentRepository.get_by_id(
            session,
            delivery_agent_id
        )

        if not delivery_agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Delivery agent not found"
            )

        return delivery_agent

    # ==========================
    # BREAK MANAGEMENT
    # ==========================

    @staticmethod
    async def start_break(
        session,
        delivery_agent_id
    ):

        agent = await session.get(
            DeliveryAgent,
            delivery_agent_id
        )

        if not agent:
            raise HTTPException(
                status_code=404,
                detail="Delivery agent not found"
            )

        agent.is_on_break = True

        await session.commit()

        return {
            "message": "Break started",
            "break_minutes": 15
        }

    @staticmethod
    async def end_break(
        session,
        delivery_agent_id
    ):

        agent = await session.get(
            DeliveryAgent,
            delivery_agent_id
        )

        if not agent:
            raise HTTPException(
                status_code=404,
                detail="Delivery agent not found"
            )

        agent.is_on_break = False

        await session.commit()

        return {
            "message": "Break ended"
        }

    @staticmethod
    async def break_status(
        session,
        delivery_agent_id
    ):

        agent = await session.get(
            DeliveryAgent,
            delivery_agent_id
        )

        if not agent:
            raise HTTPException(
                status_code=404,
                detail="Delivery agent not found"
            )

        return {
    "online": agent.is_active,
    "is_on_break": agent.is_on_break,
    "remaining_minutes": 12 if agent.is_on_break else 0,
    "today_break_time": agent.today_break_time,
    "goal_completion": agent.goal_completion,
    "deliveries_completed": agent.deliveries_completed
}

    # ==========================
    # AVAILABILITY SETTINGS
    # ==========================

    @staticmethod
    async def save_availability_settings(
        session,
        delivery_agent_id,
        payload
    ):

        agent = await session.get(
            DeliveryAgent,
            delivery_agent_id
        )

        if not agent:
            raise HTTPException(
                status_code=404,
                detail="Delivery agent not found"
            )

        agent.is_auto_accept = payload["is_auto_accept"]
        agent.working_radius_km = payload["working_radius_km"]

        agent.accept_cod = payload["accept_cod"]
        agent.accept_bulk_orders = payload["accept_bulk_orders"]
        agent.accept_fragile_items = payload["accept_fragile_items"]
        agent.accept_long_distance = payload["accept_long_distance"]

        agent.vehicle_mode = payload["vehicle_mode"]

        await session.commit()

        return {
            "message": "Availability settings updated successfully"
        }

    @staticmethod
    async def get_availability_settings(
        session,
        delivery_agent_id
    ):

        agent = await session.get(
            DeliveryAgent,
            delivery_agent_id
        )

        if not agent:
            raise HTTPException(
                status_code=404,
                detail="Delivery agent not found"
            )

        return {
            "online": agent.is_active,
            "auto_accept_orders": agent.is_auto_accept,
            "working_radius_km": agent.working_radius_km,
            "cash_on_delivery": agent.accept_cod,
            "bulk_orders": agent.accept_bulk_orders,
            "fragile_items": agent.accept_fragile_items,
            "long_distance_trips": agent.accept_long_distance,
            "vehicle_mode": agent.vehicle_mode
        }


class DeliveryDashboardService:

    @staticmethod
    async def get_dashboard(
        db: AsyncSession,
        delivery_agent_id: uuid.UUID
    ):

        # Delivery Agent
        agent = await db.get(
            DeliveryAgent,
            delivery_agent_id
        )

        if not agent:
            return None

        # Driver Stats
        stats_result = await db.execute(
            select(DriverStats).where(
                DriverStats.delivery_agent_id == delivery_agent_id
            )
        )
        stats = stats_result.scalar_one_or_none()

        # Active Order
        order_result = await db.execute(
            select(DriverOrder).where(
                DriverOrder.delivery_agent_id == delivery_agent_id
            )
        )
        active_order = order_result.scalar_one_or_none()

        # Shifts
        shifts_result = await db.execute(
            select(DriverShift).where(
                DriverShift.delivery_agent_id == delivery_agent_id
            )
        )
        shifts = shifts_result.scalars().all()

        # Challenge
        challenge_result = await db.execute(
            select(DriverChallenge).where(
                DriverChallenge.delivery_agent_id == delivery_agent_id
            )
        )
        challenge = challenge_result.scalar_one_or_none()

        # Hotspot
        hotspot_result = await db.execute(
            select(DriverHotspot)
        )
        hotspot = hotspot_result.scalar_one_or_none()

        # Peak Hour Bonus
        peak_result = await db.execute(
            select(PeakHourBonus).where(
                PeakHourBonus.active.is_(True)
            )
        )
        peak = peak_result.scalar_one_or_none()

        # Earnings Boost
        boost_result = await db.execute(
            select(EarningsBoost).where(
                EarningsBoost.active.is_(True)
            )
        )
        boost = boost_result.scalar_one_or_none()

        # Progress %
        progress = 0

        if (
            stats
            and stats.daily_goal
            and stats.daily_goal > 0
        ):
            progress = round(
                (stats.today_earnings / stats.daily_goal) * 100,
                2
            )

        return {

            "driver": {
                "id": str(agent.id),
                "name": agent.full_name,
                "online": agent.is_active
            },

            "online_status": agent.is_active,

            "weekly_hours":
            stats.weekly_hours if stats else 0,

            "estimated_earnings":
            stats.estimated_earnings if stats else 0,

            "peak_hour": {
                "active": bool(peak),
                "bonus_per_delivery":
                    peak.bonus_amount if peak else 0,
                "ends_in_minutes":
                    peak.expires_in_minutes if peak else 0
            },

            "earnings": {
                "today":
                    stats.today_earnings if stats else 0,

                "goal":
                    stats.daily_goal if stats else 200,

                "completed_orders":
                    stats.completed_orders if stats else 0,

                "total_orders":
                    stats.total_orders if stats else 0,

                "progress_percentage":
                    progress
            },

            "active_order": {
                "order_id":
                    str(active_order.id)
                    if active_order else None,

                "restaurant_name":
                    active_order.restaurant_name
                    if active_order else None,

                "distance_to_dropoff":
                    active_order.drop_distance
                    if active_order else None,

                "status":
                    active_order.status
                    if active_order else None
            },

            "rating":
                stats.rating if stats else 0,

            "acceptance_rate":
                stats.acceptance_rate if stats else 0,

            "available_shifts": [
                {
                    "id": str(shift.id),
                    "title": shift.title,
                    "start_time": shift.start_time,
                    "end_time": shift.end_time,
                    "estimated_earning": shift.estimated_earning,
                    "is_booked": shift.is_booked,
                    "demand_tag": shift.demand_tag
                }
                for shift in shifts
            ],

            "challenge": {
                "title":
                    challenge.title if challenge else None,

                "description":
                    challenge.description if challenge else None,

                "reward_amount":
                    challenge.reward_amount if challenge else 0
            },

            "hotspot": {
                "zone_name":
                    hotspot.zone_name if hotspot else None,

                "bonus_amount":
                    hotspot.bonus_amount if hotspot else 0
            },

            "shift_available":
                len(shifts) > 0,

            "zone_map_enabled":
                True,

            "boost": {
                "available":
                    bool(boost),

                "message":
                    f"{boost.boost_percentage}% extra in {boost.zone_name}"
                    if boost else None,

                "percentage":
                    boost.boost_percentage if boost else 0,

                "zone":
                    boost.zone_name if boost else None
            }
        }
    



class DeliveryHomeService:

    @staticmethod
    async def get_home(
        db,
        delivery_agent_id
    ):

        # Delivery Agent from DB
        agent = await db.get(
            DeliveryAgent,
            delivery_agent_id
        )

        if not agent:
            return None

        # Hotspots from DB
        hotspot_result = await db.execute(
            select(DriverHotspot)
        )

        hotspots = hotspot_result.scalars().all()

        return {

            "delivery_agent": {
                "id": str(agent.id),
                "name": agent.full_name,
                "online": agent.is_active
            },

            "nearby_zones": [
                {
                    "id": str(hotspot.id),
                    "zone_name": hotspot.zone_name,
                    "distance_miles": hotspot.distance_miles,
                    "active_orders": hotspot.active_orders,
                    "earnings_multiplier": hotspot.earnings_multiplier,
                    "demand_level": hotspot.demand_level
                }
                for hotspot in hotspots
            ]
        }





    
  