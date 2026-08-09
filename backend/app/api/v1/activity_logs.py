from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repositories.task_repo import TaskRepository
from app.repositories.activity_log_repo import ActivityLogRepository
from app.schemas import activity_log as schemas

router = APIRouter(prefix="/tasks/{task_id}/activity", tags=["activity"])


@router.get("", response_model=list[schemas.ActivityLogOut])
def list_activity(task_id: int, db: Session = Depends(get_db)):
    if not TaskRepository(db).get(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return ActivityLogRepository(db).list_for_task(task_id)