from sqlalchemy import (
    Column,
    Integer,
    String
)

from app.config.database import Base


class Cuisine(Base):

    __tablename__ = "cuisines"

    id = Column(Integer, primary_key=True)

    name = Column(String)

    image = Column(String)