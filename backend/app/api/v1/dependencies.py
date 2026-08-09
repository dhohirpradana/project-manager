from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repositories.task_repo import TaskRepository
from app.schemas import dependency as schemas
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks/{task_id}/dependencies", tags=["dependencies"])


@router.post("", response_model=schemas.DependencyOut, status_code=201)
def add_dependency(task_id: int, data: dict, db: Session = Depends(get_db)):
    depends_on_task_id = data.get("depends_on_task_id")
    if depends_on_task_id is None:
        raise HTTPException(status_code=400, detail="depends_on_task_id required")
    if not TaskRepository(db).get(task_id) or not TaskRepository(db).get(depends_on_task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    try:
        return TaskService(db).add_dependency(task_id, depends_on_task_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=list[schemas.DependencyOut])
def list_dependencies(task_id: int, db: Session = Depends(get_db)):
    if not TaskRepository(db).get(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    from app.repositories.dependency_repo import DependencyRepository
    return DependencyRepository(db).list_for_task(task_id)