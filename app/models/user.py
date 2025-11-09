import datetime

from sqlalchemy import Index, Column, Integer, String, Date, Enum, ForeignKey, func, DateTime, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import relationship

from app.core.db import Base
from .enum_models import Gender, Goal, Experience

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String, nullable=True)
    gender = Column(Enum(Gender), nullable=True)
    birthdate = Column(Date, nullable=True)
    last_weight = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    goal = Column(Enum(Goal), nullable=True)
    experience = Column(Enum(Experience), nullable=True)
    settings = Column(JSONB, default=lambda: {"notifications": True, "units": "kg", "language": "ru"})
    hashed_password = Column(String, nullable=True)

    refresh_tokens = relationship("RefreshToken", back_populates="user")
    sessions = relationship("SessionToken", back_populates="user", cascade="all, delete")
    metrics = relationship("UserMetric", back_populates="user")
    hints = relationship("UserHint", uselist=False, back_populates="user")

def default_hints():
    return {
        "start": False,
        "first_training": False,
        "settings": False,
        "goals": False,
        "stats": False,
        "weight": False,
    }

class UserHint(Base):
    __tablename__ = "user_hints"

    user_id = Column(ForeignKey(User.user_id), primary_key=True)
    hints = Column(MutableDict.as_mutable(JSONB), default=default_hints)

    user = relationship("User", back_populates="hints")

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id = Column(Integer, primary_key=True)
    token = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    session_id = Column(String, ForeignKey("session_tokens.session_id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="refresh_tokens")
    session = relationship("SessionToken")

Index("idx_refresh_token", RefreshToken.token)

class SessionToken(Base):
    __tablename__ = "session_tokens"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    session_id = Column(String, unique=True, nullable=False)  # UUID
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.datetime.now(datetime.timezone.utc))
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="sessions")

class UserMetric(Base):
    __tablename__ = "user_metrics"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    date = Column(Date, server_default=func.current_date())
    weight = Column(Integer)

    user = relationship("User", back_populates="metrics")

Index("idx_user_date_desc", UserMetric.user_id, UserMetric.date.desc())
