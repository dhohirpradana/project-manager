from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from app.models.task import TaskStatus, Priority

class TaskBase(BaseModel):
    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.TODO
    priority: Priority = Priority.MEDIUM
    progress: float = Field(default=0.0, ge=0, le=100)
    environment: str | None = None
    assignee_id: int | None = None
    estimated_minutes: int | None = Field(default=None, ge=0)
    spent_minutes: int | None = Field(default=0, ge=0)
    start_date: datetime | None = None
    due_date: datetime | None = None

class TaskCreate(TaskBase):
    project_id: int
    parent_task_id: int | None = None

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    priority: Priority | None = None
    progress: float | None = Field(default=None, ge=0, le=100)
    environment: str | None = None
    assignee_id: int | None = None
    estimated_minutes: int | None = Field(default=None, ge=0)
    spent_minutes: int | None = Field(default=None, ge=0)
    start_date: datetime | None = None
    due_date: datetime | None = None
    parent_task_id: int | None = None

class TaskOut(TaskBase):
    id: int
    project_id: int
    parent_task_id: int | None
    created_by: int
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime | None
    model_config = ConfigDict(from_attributes=True)

class TaskTree(TaskOut):
    subtasks: list["TaskTree"] = []