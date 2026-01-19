from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

from app.entities.task import TaskStatus

class TaskCreateDTO(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=5)
    due_date: Optional[date] = None
    assignee_user_id: Optional[int] = None

class TaskUpdateDTO(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=200)
    description: Optional[str] = Field(default=None, min_length=5)
    due_date: Optional[date] = None
    assignee_user_id: Optional[int] = None

class TaskTransitionDTO(BaseModel):
    status: TaskStatus

class TaskResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    status: TaskStatus
    due_date: Optional[date] = None
    assignee_user_id: Optional[int] = None
