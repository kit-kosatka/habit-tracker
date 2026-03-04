from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

class HabitCreate(BaseModel):
    title: str
    description: Optional[str] = None

class HabitUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class HabitRead(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)