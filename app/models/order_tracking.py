from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.config.database import Base


class OrderTracking(Base):
    __tablename__ = "order_tracking"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(Integer, ForeignKey("orders.id"))

    delivery_partner_id = Column(
        Integer,
        ForeignKey("delivery_partners.id")
    )

    status = Column(String, default="PLACED")

    latitude = Column(Float)
    longitude = Column(Float)

    estimated_time = Column(String)