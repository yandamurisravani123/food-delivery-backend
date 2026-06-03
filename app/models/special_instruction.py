from sqlalchemy import Column, Integer, String
from app.config.database import Base


class SpecialInstruction(Base):

    __tablename__ = "special_instructions"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer)
    instruction = Column(String)