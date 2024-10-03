from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from app.db.database import Base 

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(100))
    password = Column(String(100))
    email = Column(String(150), unique=True)
    role_id = Column(Integer, ForeignKey("roles.id"), default=3)
    status = Column(Enum('active', 'inactive', name="status"), default='active')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    role = relationship("Role", backref="users", cascade="delete, merge")






