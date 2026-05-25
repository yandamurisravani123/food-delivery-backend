from sqlalchemy import Column, Integer
from app.config.database import Base


class CartPreference(Base):

    __tablename__ = "cart_preferences"

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer)
    preference_id = Column(Integer)