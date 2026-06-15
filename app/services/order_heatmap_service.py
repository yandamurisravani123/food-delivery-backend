from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import OrderTracking
from app.schemas.order_heatmap import (
    HeatmapPoint,
    OrderHeatmapResponse,
)


class OrderHeatmapService:

    @staticmethod
    async def get_heatmap(
        db: AsyncSession,
    ) -> OrderHeatmapResponse:

        result = await db.execute(
            select(
                OrderTracking.latitude,
                OrderTracking.longitude,
                func.count(
                    func.distinct(OrderTracking.order_id)
                ).label("orders")
            )
            .group_by(
                OrderTracking.latitude,
                OrderTracking.longitude
            )
            .order_by(
                func.count(
                    func.distinct(OrderTracking.order_id)
                ).desc()
            )
        )

        rows = result.all()

        return OrderHeatmapResponse(
            heatmap=[
                HeatmapPoint(
                    latitude=row.latitude,
                    longitude=row.longitude,
                    orders=row.orders,
                )
                for row in rows
            ]
        )