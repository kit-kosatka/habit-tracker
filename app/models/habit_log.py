from sqlalchemy import Column, Integer, ForeignKey, func, Date, Boolean
from app.db.base import Base
from sqlalchemy.orm import relationship


class HabitLog(Base):
    __tablename__ = "habit_logs"
    id = Column(Integer, primary_key=True)
    habit_id = Column(Integer, ForeignKey("habits.id"))
    date = Column(Date, server_default=func.now())
    is_completed = Column(Boolean, default=False)

    habit = relationship("Habit", back_populates="habit_logs")
