from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ..core.database import get_db
from ..models.models import Task, Project, User, Comment, TimeEntry, ActivityLog, task_dependencies
from ..schemas.schemas import TaskCreate, TaskUpdate, TaskOut, CommentOut, TimeEntryOut, ActivityLogOut
from .deps import get_current_user

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

def _log_activity(db, task_id, user_id, action, details=None):
    db.add(ActivityLog(task_id=task_id, user_id=user_id, action=action, details=details))

def _check_circular_dependency(db, task_id: int, dependency_ids: List[int]) -> bool:
    """Check if adding dependencies creates a cycle using DFS."""
    # Build adjacency: task -> tasks that depend on it
    def has_path(start: int, target: int, visited: set) -> bool:
        if start == target:
            return True
        if start in visited:
            return False
        visited.add(start)
        # Find all tasks that depend on start
        dependents = db.query(Task).join(
            task_dependencies,
            task_dependencies.c.task_id == Task.id
        ).filter(task_dependencies.c.depends_on_id == start).all()
        for dep in dependents:
            if has_path(dep.id, target, visited):
                return True
        return False

    for dep_id in dependency_ids:
        if dep_id == task_id:
            return True  # self-dependency
        # If task depends on dep_id, and dep_id can reach task_id (directly or transitively)
        if has_path(dep_id, task_id, set()):
            return True
    return False

@router.post("/", response_model=TaskOut, status_code=201)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = db.query(Project).filter(Project.id == task.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    task_data = task.model_dump(exclude={"dependency_ids"})
    db_task = Task(**task_data)
    db.add(db_task)
    db.flush()  # Get task id
    
    if task.dependency_ids:
        if _check_circular_dependency(db, db_task.id, task.dependency_ids):
            db.rollback()
            raise HTTPException(status_code=400, detail="Circular dependency detected")
        deps = db.query(Task).filter(Task.id.in_(task.dependency_ids)).all()
        if len(deps) != len(set(task.dependency_ids)):
            db.rollback()
            raise HTTPException(status_code=400, detail="Some dependency tasks not found")
        db_task.dependencies.extend(deps)
    
    _log_activity(db, db_task.id, current_user.id, "created", f"Task '{db_task.title}' created")
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/", response_model=List[TaskOut])
def list_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    project_id: Optional[int] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    assignee_id: Optional[int] = None,
    sort_by: Optional[str] = Query("created_at", pattern="^(created_at|due_date|priority|status|title)$"),
    order: str = Query("asc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Task)
    if project_id:
        query = query.filter(Task.project_id == project_id)
    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    if assignee_id:
        query = query.filter(Task.assignee_id == assignee_id)
    
    sort_col = getattr(Task, sort_by)
    if order == "desc":
        query = query.order_by(sort_col.desc())
    else:
        query = query.order_by(sort_col.asc())
    
    return query.offset(skip).limit(limit).all()

@router.get("/{task_id}", response_model=TaskOut)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task_update.model_dump(exclude_unset=True)
    dependency_ids = update_data.pop("dependency_ids", None)
    
    if dependency_ids is not None:
        if _check_circular_dependency(db, task_id, dependency_ids):
            raise HTTPException(status_code=400, detail="Circular dependency detected")
        deps = db.query(Task).filter(Task.id.in_(dependency_ids)).all()
        if len(deps) != len(set(dependency_ids)):
            raise HTTPException(status_code=400, detail="Some dependency tasks not found")
        task.dependencies = deps
    
    for key, value in update_data.items():
        setattr(task, key, value)
    
    _log_activity(db, task_id, current_user.id, "updated", f"Task '{task.title}' updated")
    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    _log_activity(db, task_id, current_user.id, "deleted", f"Task '{task.title}' deleted")
    db.delete(task)
    db.commit()
    return None

# Task sub-resources
@router.get("/{task_id}/comments", response_model=List[CommentOut])
def get_task_comments(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = _get_task_or_404(db, task_id)
    return db.query(Comment).filter(Comment.task_id == task.id).all()

@router.get("/{task_id}/time-entries", response_model=List[TimeEntryOut])
def get_task_time_entries(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = _get_task_or_404(db, task_id)
    return db.query(TimeEntry).filter(TimeEntry.task_id == task.id).all()

@router.get("/{task_id}/activity", response_model=List[ActivityLogOut])
def get_task_activity(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = _get_task_or_404(db, task_id)
    return db.query(ActivityLog).filter(ActivityLog.task_id == task.id).order_by(ActivityLog.created_at.desc()).all()

@router.get("/{task_id}/dependencies", response_model=List[TaskOut])
def get_task_dependencies(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = _get_task_or_404(db, task_id)
    return task.dependencies

# Timer
@router.post("/{task_id}/timer/start", response_model=TimeEntryOut)
def start_timer(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = _get_task_or_404(db, task_id)
    
    # Stop any running timer for this user
    running = db.query(TimeEntry).filter(
        TimeEntry.user_id == current_user.id,
        TimeEntry.is_running == True
    ).all()
    for entry in running:
        entry.end_time = datetime.utcnow()
        entry.duration_seconds = int((entry.end_time - entry.start_time).total_seconds())
        entry.is_running = False
    
    new_entry = TimeEntry(
        task_id=task.id,
        user_id=current_user.id,
        start_time=datetime.utcnow(),
        is_running=True
    )
    db.add(new_entry)
    _log_activity(db, task.id, current_user.id, "timer_started", f"Timer started on '{task.title}'")
    db.commit()
    db.refresh(new_entry)
    return new_entry

@router.post("/{task_id}/timer/stop", response_model=TimeEntryOut)
def stop_timer(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = _get_task_or_404(db, task_id)
    
    entry = db.query(TimeEntry).filter(
        TimeEntry.task_id == task.id,
        TimeEntry.user_id == current_user.id,
        TimeEntry.is_running == True
    ).first()
    if not entry:
        raise HTTPException(status_code=404, detail="No running timer for this task")
    
    entry.end_time = datetime.utcnow()
    entry.duration_seconds = int((entry.end_time - entry.start_time).total_seconds())
    entry.is_running = False
    
    # Update actual hours on task
    task.actual_hours = (task.actual_hours or 0) + (entry.duration_seconds / 3600)
    
    _log_activity(db, task.id, current_user.id, "timer_stopped", f"Timer stopped on '{task.title}'")
    db.commit()
    db.refresh(entry)
    return entry

def _get_task_or_404(db, task_id):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task