from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class TimeEntryBase(BaseModel):
    minutes: int = Field(ge=1)
    description: str | None = None

class TimeEntryCreate(TimeEntryBase):
    task_id: int

class TimeEntryOut(TimeEntryBase):
    id: int
    task_id: int
    user_id: int
    logged_at: datetime
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)