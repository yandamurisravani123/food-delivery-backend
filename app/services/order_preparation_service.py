from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.order_preparation import OrderPreparation
from app.models.preparation_step import PreparationStep


class OrderPreparationService:

    # -----------------------------
    # GET FULL PREPARATION DETAILS
    # -----------------------------
    @staticmethod
    async def get_preparation(db: AsyncSession, order_id: int):

        prep_result = await db.execute(
            select(OrderPreparation).where(OrderPreparation.order_id == order_id)
        )
        prep = prep_result.scalar_one_or_none()

        steps_result = await db.execute(
            select(PreparationStep)
            .where(PreparationStep.order_id == order_id)
            .order_by(PreparationStep.sequence)
        )

        steps = steps_result.scalars().all()

        return {
            "order_id": order_id,
            "current_stage": prep.current_stage if prep else "ORDER_RECEIVED",
            "progress_percent": prep.progress_percent if prep else 0,
            "estimated_ready_time": prep.estimated_ready_time if prep else None,
            "chef_note": prep.chef_note if prep else None,
            "steps": steps
        }

    # -----------------------------
    # UPDATE PREPARATION STATUS
    # -----------------------------
    @staticmethod
    async def update_preparation(
        db: AsyncSession,
        order_id: int,
        stage: str,
        progress: int,
        note: str | None = None
    ):

        result = await db.execute(
            select(OrderPreparation).where(OrderPreparation.order_id == order_id)
        )

        prep = result.scalar_one_or_none()

        if not prep:
            prep = OrderPreparation(order_id=order_id)

        prep.current_stage = stage
        prep.progress_percent = progress
        prep.chef_note = note

        db.add(prep)
        await db.commit()
        await db.refresh(prep)

        return prep


    # -----------------------------
    # CREATE DEFAULT STEPS (when order is created)
    # -----------------------------
    @staticmethod
    async def create_steps(db: AsyncSession, order_id: int):

        default_steps = [
            ("Order Received", 1),
            ("Ingredients Being Prepped", 2),
            ("Cooking in Progress", 3),
            ("Quality Check", 4),
            ("Ready for Pickup", 5),
        ]

        for title, seq in default_steps:
            step = PreparationStep(
                order_id=order_id,
                title=title,
                sequence=seq,
                status="PENDING"
            )
            db.add(step)

        await db.commit()