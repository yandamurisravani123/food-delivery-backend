<<<<<<< HEAD

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
=======
>>>>>>> 2f6cbfeb697fc8df4b0e6dc03fde77b955d4c69c
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.models.order import Order

router = APIRouter(tags=["Savings"])


# 1. TOTAL SAVINGS OVERVIEW

@router.get("/savings/overview")
async def savings_overview(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(func.sum(Order.discount_amount))
        .where(Order.user_id == user_id)
    )

    total_savings = result.scalar() or 0

    return {
        "user_id": str(user_id),
        "total_savings": float(total_savings),
        "currency": "INR"
    }


# 2. MONTHLY SAVINGS BREAKDOWN

@router.get("/savings/monthly")
async def monthly_savings(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(
            func.extract("month", Order.created_at).label("month"),
            func.sum(Order.discount_amount).label("savings")
        )
        .where(Order.user_id == user_id)
        .group_by(func.extract("month", Order.created_at))
        .order_by(func.extract("month", Order.created_at))
    )

    rows = result.all()

    return {
        "user_id": str(user_id),
        "monthly_savings": [
            {
                "month": int(row.month),
                "savings": float(row.savings or 0)
            }
            for row in rows
        ]
    }


# 3. TOTAL SPENT VS SAVINGS

@router.get("/savings/compare")
async def savings_compare(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(
            func.sum(Order.total).label("total_spent"),
            func.sum(Order.discount_amount).label("total_saved")
        )
        .where(Order.user_id == user_id)
    )

    row = result.one()

    total_spent = row.total_spent or 0
    total_saved = row.total_saved or 0

    return {
        "user_id": str(user_id),
        "total_spent": float(total_spent),
        "total_saved": float(total_saved),
        "net_spent": float(total_spent - total_saved)
    }


# 4. DAILY SAVINGS

@router.get("/savings/daily")
async def daily_savings(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(
            func.date(Order.created_at).label("date"),
            func.sum(Order.discount_amount).label("savings")
        )
        .where(Order.user_id == user_id)
        .group_by(func.date(Order.created_at))
        .order_by(func.date(Order.created_at))
    )

    rows = result.all()

    return {
        "user_id": str(user_id),
        "daily_savings": [
            {
                "date": str(row.date),
                "savings": float(row.savings or 0)
            }
            for row in rows
        ]
    }