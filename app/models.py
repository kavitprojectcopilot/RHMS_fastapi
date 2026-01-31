from sqlalchemy import (
    Column, Integer, String, DateTime, Float, ForeignKey, Text
)
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    country = Column(String(100))
    state = Column(String(100))
    city = Column(String(100))
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    password = Column(String(255), nullable=False)

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.now())
    deleted_at = Column(DateTime, nullable=True)

    role = relationship("Role", back_populates="user")


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(50), unique=True, nullable=False)

    user = relationship("User", back_populates="role")

