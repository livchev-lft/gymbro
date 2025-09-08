from sqlalchemy import Column, Integer, String, Date, ForeignKey, func

from app.core.db import Base


class UserGoal(Base):
    __tablename__ = "user_goals"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    start_date = Column(Date, default=func.current_date())
    end_date = Column(Date, nullable=True)
    progress = Column(Integer, default=0)  # процент выполнения

