from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Enum
from app.db.database import Base 

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(Enum('administrador', 'manager', 'ventas', name="name_role"),default="ventas")
    description = Column(String(255))
    status = Column(Enum('active', 'inactive', name="status"), default='active')