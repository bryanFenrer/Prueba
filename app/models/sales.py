from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, DECIMAL
from app.db.database import Base 

class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, )
    user_id = Column(Integer, ForeignKey("users.id"))
    product_name = Column(String(255))
    quantity = Column(Integer)
    total_price = Column(DECIMAL(10, 2))
    sale_date = Column(DateTime, default=datetime.now)
    status = Column(Enum('completed', 'pending',name="status_sale"))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    user = relationship("User", backref="sales", cascade="delete, merge")