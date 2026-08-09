from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from app.models.project import ProjectStatus, Priority

class ProjectBase(BaseModel):
    name: str
    description: str | None = None
    status: ProjectStatus = ProjectStatus.PLANNED
    priority: Priority = Priority.MEDIUM
    start_date: datetime | None = None
    due_date: datetime | None = None

class ProjectCreate(ProjectBase):
    parent_id: int | None = None

class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    status: ProjectStatus | None = None
    priority: Priority | None = None
    start_date: datetime | None = None
    due_date: datetime | None = None
    parent_id: int | None = None

class ProjectOut(ProjectBase):
    id: int
    parent_id: int | None
    created_by: int
    created_at: datetime
    updated_at: datetime | None
    archived_at: datetime | None
    model_config = ConfigDict(from_attributes=True)

class ProjectTree(ProjectOut):
    children: list["ProjectTree"] = []