from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean
from sqlalchemy.sql import func
from app.db.base_class import Base
from enum import Enum as PyEnum


class UserStatus(PyEnum):
    pending = "pending"
    active = "active"
    rejected = "rejected"


class UserRole(PyEnum):
    investor = "investor"
    fund_manager = "fund_manager"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    # Core personal info
    name = Column(String, nullable=True)
    company = Column(String, nullable=True)
    title = Column(String, nullable=True)
    email = Column(String, unique=True, index=True)
    mobile = Column(String, nullable=True)
    business_type = Column(String, nullable=True)

    # Platform info
    portal_used = Column(String, nullable=True)
    total_investment = Column(Integer, default=0)

    # Access control
    role = Column(Enum(UserRole), nullable=False)
    status = Column(Enum(UserStatus), default=UserStatus.pending)

    password_hash = Column(String, nullable=False)

    # Terms acceptance
    terms_accepted = Column(Boolean, default=False)
    terms_accepted_date = Column(DateTime, nullable=True)

    # 2FA
    twofa_code = Column(String, nullable=True)
    twofa_expires = Column(DateTime, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
