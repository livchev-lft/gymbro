from sqlalchemy import Index, Column, Integer, String, Date, Enum, ForeignKey, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from .base import Base
from .enum_models import Gender, Goal, Experience

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    birthdate = Column(Date, nullable=False)
    last_weight = Column(Integer, nullable=True)
    height = Column(Integer, nullable=False)
    goal = Column(Enum(Goal), nullable=False)
    experience = Column(Enum(Experience), nullable=False)
    settings = Column(JSONB, default=lambda: {"notifications": True, "units": "kg", "language": "ru"})
    metrics = relationship("UserMetric", back_populates="user")

class UserMetric(Base):
    __tablename__ = "user_metrics"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    date = Column(Date, server_default=func.current_date())
    weight = Column(Integer)

    user = relationship("User", back_populates="metrics")

Index("idx_user_date_desc", UserMetric.user_id, UserMetric.date.desc())
