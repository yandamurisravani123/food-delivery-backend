from sqlalchemy import Column, Float, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
<<<<<<< HEAD

from app.config.database import Base

import uuid


class RevenueReport(Base):

    __tablename__ = "revenue_reports"

=======
 
from app.config.database import Base
 
import uuid
 
 
class RevenueReport(Base):
 
    __tablename__ = "revenue_reports"
 
>>>>>>> 6da5f03 (testing)
    # PRIMARY KEY
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
    # FOREIGN KEY
    restaurant_id = Column(
        UUID(as_uuid=True),
        ForeignKey("restaurants.id")
    )
<<<<<<< HEAD

    total_revenue = Column(Float, default=0)

    total_orders = Column(Integer, default=0)

    avg_order_value = Column(Float, default=0)

    gst_amount = Column(Float, default=0)

    platform_commission = Column(Float, default=0)

    delivery_fee = Column(Float, default=0)

    net_earnings = Column(Float, default=0)

    digital_payments = Column(Float, default=0)

    card_payments = Column(Float, default=0)

    cash_on_delivery = Column(Float, default=0)

=======
 
    total_revenue = Column(Float, default=0)
 
    total_orders = Column(Integer, default=0)
 
    avg_order_value = Column(Float, default=0)
 
    gst_amount = Column(Float, default=0)
 
    platform_commission = Column(Float, default=0)
 
    delivery_fee = Column(Float, default=0)
 
    net_earnings = Column(Float, default=0)
 
    digital_payments = Column(Float, default=0)
 
    card_payments = Column(Float, default=0)
 
    cash_on_delivery = Column(Float, default=0)
 
>>>>>>> 6da5f03 (testing)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )