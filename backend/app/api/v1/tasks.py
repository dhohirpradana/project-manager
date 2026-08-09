from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repositories.task_repo import TaskRepository
from app.repositories.project_repo import ProjectRepository
from app.schemas import task as schemas

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=schemas.TaskOut, status_code=201)
def create_task(data: schemas.TaskCreate, created_by: int = 1, db: Session = Depends(get_db)):
    repo = TaskRepository(db)
    if not ProjectRepository(db).get(data.project_id):
        raise HTTPException(status_code=400, detail="Project not found")
    if data.parent_task_id is not None and not repo.get(data.parent_task_id):
        raise HTTPException(status_code=400, detail="Parent task not found")
    return repo.create(data, created_by=created_by)


@router.get("", response_model=list[schemas.TaskOut])
def list_tasks(project_id: int | None = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return TaskRepository(db).list(project_id=project_id, skip=skip, limit=limit)


@router.get("/tree", response_model=list[schemas.TaskTree])
def task_tree(project_id: int | None = None, db: Session = Depends(get_db)):
    tasks = TaskRepository(db).build_tree(project_id=project_id)
    return _serialize_tree(tasks)


def _serialize_tree(tasks):
    result = []
    for t in tasks:
        d = schemas.TaskOut.model_validate(t).model_dump()
        d["subtasks"] = _serialize_tree(getattr(t, "_subtasks", []))
        result.append(d)
    return result


@router.get("/{task_id}", response_model=schemas.TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = TaskRepository(db).get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, data: schemas.TaskUpdate, db: Session = Depends(get_db)):
    repo = TaskRepository(db)
    task = repo.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if data.parent_task_id is not None:
        if data.parent_task_id == task_id:
            raise HTTPException(status_code=400, detail="Task cannot be its own parent")
        if not repo.get(data.parent_task_id):
            raise HTTPException(status_code=400, detail="Parent task not found")
    return repo.update(task, data)


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    repo = TaskRepository(db)
    task = repo.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    repo.delete(task)