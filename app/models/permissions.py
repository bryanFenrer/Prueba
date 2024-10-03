from sqlalchemy import Column, Integer, String, Enum
from app.db.database import Base 

class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(255))
    status = Column(Enum('active', 'inactive', name="status"), default='active')