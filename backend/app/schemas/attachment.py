from datetime import datetime
from pydantic import BaseModel, ConfigDict

class AttachmentOut(BaseModel):
    id: int
    task_id: int
    filename: str
    file_path: str
    file_size: int | None
    mime_type: str | None
    uploaded_at: datetime
    model_config = ConfigDict(from_attributes=True)