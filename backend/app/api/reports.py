from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from typing import Optional
from ..core.database import get_db
from ..models.models import Project, Task, TimeEntry, User, ActivityLog
from .deps import get_current_user

router = APIRouter(prefix="/api/reports", tags=["reports"])

@router.get("/")
def get_report(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    project_id: Optional[int] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Base task query for user's projects
    projects = db.query(Project).filter(Project.owner_id == current_user.id).all()
    project_ids = [p.id for p in projects]
    
    task_query = db.query(Task)
    if project_ids:
        task_query = task_query.filter(Task.project_id.in_(project_ids))
    else:
        task_query = task_query.filter(Task.id == -1)
    
    if project_id:
        task_query = task_query.filter(Task.project_id == project_id)
    if start_date:
        task_query = task_query.filter(Task.created_at >= start_date)
    if end_date:
        task_query = task_query.filter(Task.created_at <= end_date)
    
    tasks = task_query.all()
    
    # Time entries
    time_query = db.query(TimeEntry)
    task_ids = [t.id for t in tasks]
    if task_ids:
        time_query = time_query.filter(TimeEntry.task_id.in_(task_ids))
    else:
        time_query = time_query.filter(TimeEntry.id == -1)
    if user_id:
        time_query = time_query.filter(TimeEntry.user_id == user_id)
    if start_date:
        time_query = time_query.filter(TimeEntry.start_time >= start_date)
    if end_date:
        time_query = time_query.filter(TimeEntry.start_time <= end_date)
    
    time_entries = time_query.all()
    total_seconds = sum([te.duration_seconds or 0 for te in time_entries if te.duration_seconds])
    
    # Completed count
    completed = len([t for t in tasks if t.status == "DONE"])
    
    return {
        "total_tasks": len(tasks),
        "completed_tasks": completed,
        "completion_rate": round((completed / len(tasks) * 100), 2) if tasks else 0,
        "total_time_hours": round(total_seconds / 3600, 2),
        "time_entries": len(time_entries),
        "report_period": {
            "start": start_date.isoformat() if start_date else None,
            "end": end_date.isoformat() if end_date else None
        }
    }