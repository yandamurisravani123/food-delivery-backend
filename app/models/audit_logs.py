from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.sql import func
 
from app.config.database import Base
 
 
class AuditLog(Base):
    __tablename__ = "audit_logs"
 
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
 
    action = Column(
        String(255)
    )
 
    description = Column(
        String(500)
    )
 
    created_at = Column(
        DateTime,
        server_default=func.now()
    )