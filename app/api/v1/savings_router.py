from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from uuid import UUID
from app.config.database import get_db
from app.models.order import Order

router = APIRouter(tags=["Savings"])


# 1. TOTAL SAVINGS OVERVIEW

@router.get("/savings/overview")
async def savings_overview(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Total savings of a user (all time)
    """

    result = await db.execute(
        select(func.sum(Order.discount_amount))
        .where(Order.user_id == user_id)
    )

    total_savings = result.scalar() or 0

    return {
        "user_id": user_id,
        "total_savings": float(total_savings),
        "currency": "INR"
    }


# 2. MONTHLY SAVINGS BREAKDOWN

@router.get("/savings/monthly")
async def monthly_savings(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Month-wise savings
    """

    result = await db.execute(
        select(
            func.extract("month", Order.created_at).label("month"),
            func.sum(Order.discount_amount).label("savings")
        )
        .where(Order.user_id == user_id)
        .group_by(func.extract("month", Order.created_at))
        .order_by("month")
    )

    rows = result.all()

    return {
        "user_id": user_id,
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
    """
    Compare total spend vs total savings
    """

    result = await db.execute(
        select(
            func.sum(Order.total_amount),
            func.sum(Order.discount_amount)
        )
        .where(Order.user_id == user_id)
    )

    total_spent, total_saved = result.one()

    return {
        "user_id": user_id,
        "total_spent": float(total_spent or 0),
        "total_saved": float(total_saved or 0),
        "net_spent": float((total_spent or 0) - (total_saved or 0))
    }


# 4. DAILY SAVINGS (OPTIONAL DASHBOARD)

@router.get("/savings/daily")
async def daily_savings(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Day-wise savings for charts
    """

    result = await db.execute(
        select(
            func.date(Order.created_at).label("date"),
            func.sum(Order.discount_amount).label("savings")
        )
        .where(Order.user_id == user_id)
        .group_by(func.date(Order.created_at))
        .order_by("date")
    )

    rows = result.all()

    return {
        "user_id": user_id,
        "daily_savings": [
            {
                "date": str(row.date),
                "savings": float(row.savings or 0)
            }
            for row in rows
        ]
    }