from sqlalchemy import Column, Integer
from app.config.database import Base


class CartExtra(Base):

    __tablename__ = "cart_extras"

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer)
    extra_id = Column(Integer)