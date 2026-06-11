from datetime import datetime

from sqlalchemy import (
    Integer,
    Float,
    String,
    DateTime
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.db.base import Base


class OperationsDashboard(Base):
    __tablename__ = "operations_dashboard"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    total_orders: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    completed_orders: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    cancelled_orders: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    active_drivers: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    active_restaurants: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )


class KPIDashboard(Base):
    __tablename__ = "kpi_dashboard"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    total_revenue: Mapped[float] = mapped_column(
        Float,
        default=0
    )

    average_order_value: Mapped[float] = mapped_column(
        Float,
        default=0
    )

    customer_retention_rate: Mapped[float] = mapped_column(
        Float,
        default=0
    )

    delivery_success_rate: Mapped[float] = mapped_column(
        Float,
        default=0
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )


class LiveOrder(Base):
    __tablename__ = "live_orders"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    order_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    customer_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    restaurant_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    driver_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    amount: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )