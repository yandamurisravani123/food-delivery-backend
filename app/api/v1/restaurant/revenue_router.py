from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.config.database import get_db
from app.models.revenue_report import RevenueReport

router = APIRouter(
    prefix="/revenue",
)

# CREATE REVENUE REPORT

@router.post("/create")
async def create_revenue_report(

    restaurant_id: UUID,

    total_revenue: float,

    total_orders: int,

    avg_order_value: float,

    gst_amount: float,

    platform_commission: float,

    delivery_fee: float,

    net_earnings: float,

    digital_payments: float,

    card_payments: float,

    cash_on_delivery: float,

    db: AsyncSession = Depends(get_db)
):

    report = RevenueReport(

        restaurant_id=restaurant_id,

        total_revenue=total_revenue,

        total_orders=total_orders,

        avg_order_value=avg_order_value,

        gst_amount=gst_amount,

        platform_commission=platform_commission,

        delivery_fee=delivery_fee,

        net_earnings=net_earnings,

        digital_payments=digital_payments,

        card_payments=card_payments,

        cash_on_delivery=cash_on_delivery
    )

    db.add(report)

    await db.commit()

    await db.refresh(report)

    return {
        "message": "Revenue report created",
        "report_id": str(report.id)
    }

# GET REVENUE REPORT

@router.get("/{restaurant_id}")
async def get_revenue_report(
    restaurant_id: UUID,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(RevenueReport).where(
            RevenueReport.restaurant_id == restaurant_id
        )
    )

    report = result.scalar_one_or_none()

    if not report:
        return {
            "message": "No revenue report found"
        }

    return report

# UPDATE REPORT

@router.put("/{report_id}")
async def update_revenue_report(

    report_id: UUID,

    total_revenue: float,

    net_earnings: float,

    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(RevenueReport).where(
            RevenueReport.id == report_id
        )
    )

    report = result.scalar_one_or_none()

    if not report:
        return {
            "message": "Report not found"
        }

    report.total_revenue = total_revenue
    report.net_earnings = net_earnings

    await db.commit()

    return {
        "message": "Revenue report updated"
    }

# DELETE REPORT

@router.delete("/{report_id}")
async def delete_revenue_report(
    report_id: UUID,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(RevenueReport).where(
            RevenueReport.id == report_id
        )
    )

    report = result.scalar_one_or_none()

    if not report:
        return {
            "message": "Report not found"
        }

    await db.delete(report)

    await db.commit()

    return {
        "message": "Revenue report deleted"
    }

# REVENUE HISTORY

@router.get("/history/{restaurant_id}")
async def revenue_history(
    restaurant_id: UUID,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(RevenueReport).where(
            RevenueReport.restaurant_id == restaurant_id
        )
    )

    reports = result.scalars().all()

    return reports

# PAYMENT METHODS

@router.get("/payment-methods/{restaurant_id}")
async def payment_methods(
    restaurant_id: UUID,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(RevenueReport).where(
            RevenueReport.restaurant_id == restaurant_id
        )
    )

    report = result.scalar_one_or_none()

    if not report:
        return {
            "message": "No data found"
        }

    return {

        "digital_payments": report.digital_payments,

        "card_payments": report.card_payments,

        "cash_on_delivery": report.cash_on_delivery
    }