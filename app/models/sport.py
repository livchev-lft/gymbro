from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship

from app.core.db import Base
from .enum_models import Experience


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    muscle_group = Column(String, nullable=False)
    description = Column(String, nullable=True)
    equipment = Column(String, nullable=True)
    difficulty = Column(Enum(Experience), nullable=True)

class WorkoutSession(Base):
    __tablename__ = "workout_sessions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    date = Column(Date, nullable=False)
    notes = Column(String, nullable=False)

    exercises = relationship("WorkoutExercise", back_populates="session")

class WorkoutExercise(Base):
    __tablename__ = "workout_exercises"

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("workout_sessions.id"))
    exercise_id = Column(Integer, ForeignKey("exercises.id"))
    sets = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=True)

    session = relationship("WorkoutSession", back_populates="exercises")
    exercise = relationship("Exercise")

