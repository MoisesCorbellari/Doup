from pydantic import BaseModel, ConfigDict, Field
from datetime import date
from typing import Optional

class ToDoListResponse(BaseModel):
    id: int
    title: str
    description: str
    created: date
    completed: bool

    class Config:
        model_config = ConfigDict(
            from_attributes=True
        )

class ToDoListRequest(BaseModel):
    title: str = Field(min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=255)
    completed: bool = Field(default=False)