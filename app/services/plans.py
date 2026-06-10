from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.plans import Plan


class PlanService:

    @staticmethod
    async def get_all_plans(db: AsyncSession):
        result = await db.execute(select(Plan))
        return result.scalars().all()

    @staticmethod
    async def get_plan_by_id(db: AsyncSession, plan_id: int):
        result = await db.execute(
            select(Plan).where(Plan.id == plan_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create_plan(db: AsyncSession, plan_data):
        plan = Plan(
            name=plan_data.name,
            price=plan_data.price,
            description=plan_data.description,
            duration_days=plan_data.duration_days,
            free_trial_days=plan_data.free_trial_days,
            is_popular=plan_data.is_popular,
            is_featured=plan_data.is_featured,
            is_active=plan_data.is_active,
            badge_text=plan_data.badge_text,
            button_text=plan_data.button_text,
            theme_color=plan_data.theme_color,
            icon_url=plan_data.icon_url,
            display_order=plan_data.display_order,
        )
        db.add(plan)
        await db.commit()
        await db.refresh(plan)
        return plan

    @staticmethod
    async def delete_plan(db: AsyncSession, plan_id: int):
        result = await db.execute(
            select(Plan).where(Plan.id == plan_id)
        )
        plan = result.scalar_one_or_none()

        if not plan:
            return None

        await db.delete(plan)
        await db.commit()

        return {"message": "Plan Deleted"}