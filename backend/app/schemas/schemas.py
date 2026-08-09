from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class StatusEnum(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    BLOCKED = "BLOCKED"

class PriorityEnum(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"

# User
class UserCreate(BaseModel):
    email: str
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

# Project
class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    parent_id: Optional[int] = None

class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    parent_id: Optional[int] = None

class ProjectOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    owner_id: int
    parent_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ProjectWithChildren(ProjectOut):
    children: List[ProjectOut] = []
    
    class Config:
        from_attributes = True

# Task
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    status: StatusEnum = StatusEnum.TODO
    priority: PriorityEnum = PriorityEnum.MEDIUM
    progress: int = Field(default=0, ge=0, le=100)
    project_id: int
    assignee_id: Optional[int] = None
    parent_task_id: Optional[int] = None
    estimated_hours: Optional[float] = Field(None, ge=0)
    due_date: Optional[datetime] = None
    dependency_ids: List[int] = []
    
    @field_validator('progress')
    @classmethod
    def validate_progress(cls, v):
        if v < 0 or v > 100:
            raise ValueError('progress must be 0-100')
        return v

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None
    status: Optional[StatusEnum] = None
    priority: Optional[PriorityEnum] = None
    progress: Optional[int] = Field(None, ge=0, le=100)
    assignee_id: Optional[int] = None
    parent_task_id: Optional[int] = None
    estimated_hours: Optional[float] = Field(None, ge=0)
    due_date: Optional[datetime] = None
    dependency_ids: Optional[List[int]] = None
    
    @field_validator('progress')
    @classmethod
    def validate_progress(cls, v):
        if v is not None and (v < 0 or v > 100):
            raise ValueError('progress must be 0-100')
        return v

class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: StatusEnum
    priority: PriorityEnum
    progress: int
    project_id: int
    assignee_id: Optional[int]
    parent_task_id: Optional[int]
    estimated_hours: Optional[float]
    actual_hours: float
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Comment
class CommentCreate(BaseModel):
    content: str = Field(..., min_length=1)
    task_id: int

class CommentUpdate(BaseModel):
    content: str = Field(..., min_length=1)

class CommentOut(BaseModel):
    id: int
    content: str
    task_id: int
    author_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# TimeEntry
class TimeEntryOut(BaseModel):
    id: int
    task_id: int
    user_id: int
    start_time: datetime
    end_time: Optional[datetime]
    duration_seconds: Optional[int]
    is_running: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# ActivityLog
class ActivityLogOut(BaseModel):
    id: int
    task_id: int
    user_id: int
    action: str
    details: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Dashboard
class DashboardStats(BaseModel):
    total_projects: int
    total_tasks: int
    tasks_by_status: dict
    tasks_by_priority: dict
    overdue_tasks: int

# Report
class ReportQuery(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    project_id: Optional[int] = None
    user_id: Optional[int] = None
