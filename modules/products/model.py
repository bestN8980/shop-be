from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, Numeric
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy.orm import relationship


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(String(512), nullable=False)
    description = Column(Text)
    price = Column(Integer, nullable=False)
    stock = Column(Integer, nullable=False)
    category_id = Column(Integer,ForeignKey("categories.id"), nullable=False, index=True)
    is_deleted = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True),server_default= func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True),server_default=func.now(), onupdate=func.now())

    #relationship
    category = relationship("Category", back_populates="products")