from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repositories.task_repo import TaskRepository
from app.schemas import time_entry as schemas
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks/{task_id}/time", tags=["time"])


@router.post("", response_model=schemas.TimeEntryOut, status_code=201)
def log_time(task_id: int, data: schemas.TimeEntryBase, user_id: int = 1, db: Session = Depends(get_db)):
    if not TaskRepository(db).get(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskService(db).log_time(task_id, user_id, data.minutes, data.description)


@router.get("", response_model=list[schemas.TimeEntryOut])
def list_time(task_id: int, db: Session = Depends(get_db)):
    if not TaskRepository(db).get(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    from app.repositories.time_entry_repo import TimeEntryRepository
    return TimeEntryRepository(db).list_for_task(task_id)