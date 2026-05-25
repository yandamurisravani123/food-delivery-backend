from sqlalchemy import Column, Integer, String, Float
from app.config.database import Base


class MenuItem(Base):

    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)