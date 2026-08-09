from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ActivityLogOut(BaseModel):
    id: int
    task_id: int
    user_id: int
    action: str
    details: str | None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)