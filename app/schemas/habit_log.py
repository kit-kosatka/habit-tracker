from datetime import date

from pydantic import BaseModel, ConfigDict
from typing import Optional

class HabitLogCreate(BaseModel):
    habit_id: int
    date: Optional[date] = None


class HabitLogResponse(BaseModel):
    id: int
    habit_id: int
    date: date
    is_completed: bool

    model_config = ConfigDict(from_attributes=True)