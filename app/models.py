from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    role = Column(String, default="User")

    is_active = Column(Boolean, default=False)
    is_subscribed = Column(Boolean, default=True)
    

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    priority = Column(String)
    status = Column(String, default="Pending")

    user_id = Column(Integer, ForeignKey("users.id"))
    completed_at = Column(DateTime(timezone=True), nullable=True)
    assigned_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    

