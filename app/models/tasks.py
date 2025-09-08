from sqlalchemy import Boolean, Column, Integer, String, Date, ForeignKey

from app.core.db import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    due_date = Column(Date, nullable=True)
    completed = Column(Boolean, default=False)
    priority = Column(Integer, default=0)  # 0-low,1-medium,2-high
