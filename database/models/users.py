from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.sql import func
from database.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    complete_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    status = Column(Boolean, default=True)
    role = Column(String(255), default="user")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())