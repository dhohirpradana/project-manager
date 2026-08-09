from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from ..core.database import get_db
from ..models.models import Project, Task, User, StatusEnum
from ..schemas.schemas import DashboardStats
from .deps import get_current_user

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

@router.get("/", response_model=DashboardStats)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    projects = db.query(Project).filter(Project.owner_id == current_user.id).all()
    project_ids = [p.id for p in projects]
    
    tasks = db.query(Task)
    if project_ids:
        tasks = tasks.filter(Task.project_id.in_(project_ids))
    else:
        tasks = tasks.filter(Task.id == -1)  # No projects, no tasks
    
    all_tasks = tasks.all()
    
    # Status breakdown
    status_counts = {}
    priority_counts = {}
    for t in all_tasks:
        status_counts[t.status.value] = status_counts.get(t.status.value, 0) + 1
        priority_counts[t.priority.value] = priority_counts.get(t.priority.value, 0) + 1
    
    # Overdue: due_date < now and not DONE
    now = datetime.utcnow()
    overdue = [t for t in all_tasks if t.due_date and t.due_date < now and t.status != StatusEnum.DONE]
    
    return DashboardStats(
        total_projects=len(projects),
        total_tasks=len(all_tasks),
        tasks_by_status=status_counts,
        tasks_by_priority=priority_counts,
        overdue_tasks=len(overdue)
    )