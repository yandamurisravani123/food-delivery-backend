from sqlalchemy import Column, Integer, Float
from app.config.database import Base


class Cart(Base):

    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer)
    quantity = Column(Integer)
    total_price = Column(Float)