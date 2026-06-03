from sqlalchemy import Column, Integer, String, Float
from app.config.database import Base


class Extra(Base):

    __tablename__ = "extras"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)