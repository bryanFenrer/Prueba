from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, Enum
from app.db.database import Base 

class UserPermission(Base):
    __tablename__ = "user_permissions"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    permission_id = Column(Integer, ForeignKey("permissions.id"), primary_key=True)
    status = Column(Enum('active', 'inactive', name="status"), default='active')
    user = relationship("User", backref="user_permissions", cascade="delete, merge")
    permission = relationship("Permission", backref="user_permissions", cascade="delete, merge")
    