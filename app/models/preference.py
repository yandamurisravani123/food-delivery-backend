from sqlalchemy import Column, Integer, String
from app.config.database import Base


class Preference(Base):

    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)