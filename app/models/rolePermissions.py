from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, Enum
from app.db.database import Base 

class RolePermission(Base):
    __tablename__ = "role_permissions"
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
    permission_id = Column(Integer, ForeignKey("permissions.id"), primary_key=True)
    role = relationship("Role", backref="role_permissions", cascade="delete, merge")
    permission = relationship("Permission", backref="role_permissions", cascade="delete, merge")
    status = Column(Enum('active', 'inactive', name="status"), default='active')