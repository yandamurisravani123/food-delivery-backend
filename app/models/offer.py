from sqlalchemy import Column, Integer, String
from app.config.database import Base


class Offer(Base):

    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String)

    image = Column(String)

    description = Column(String)