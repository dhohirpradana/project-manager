from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import select
from app import models
from app.schemas import task as schemas


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, task_id: int):
        return self.db.get(models.Task, task_id)

    def get_subtasks(self, parent_task_id: int):
        return self.db.scalars(
            select(models.Task).where(models.Task.parent_task_id == parent_task_id).order_by(models.Task.id)
        ).all()

    def list(self, project_id: int | None = None, skip: int = 0, limit: int = 100):
        stmt = select(models.Task)
        if project_id is not None:
            stmt = stmt.where(models.Task.project_id == project_id)
        return self.db.scalars(stmt.offset(skip).limit(limit)).all()

    def list_roots(self, project_id: int | None = None):
        stmt = select(models.Task).where(models.Task.parent_task_id.is_(None))
        if project_id is not None:
            stmt = stmt.where(models.Task.project_id == project_id)
        return self.db.scalars(stmt.order_by(models.Task.id)).all()

    def create(self, data: schemas.TaskCreate, created_by: int):
        obj = models.Task(**data.model_dump(), created_by=created_by)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, task: models.Task, data: schemas.TaskUpdate):
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(task, field, value)
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task: models.Task):
        self.db.delete(task)
        self.db.commit()

    def build_tree(self, project_id: int | None = None, root_id: int | None = None) -> list[models.Task]:
        stmt = select(models.Task)
        if project_id is not None:
            stmt = stmt.where(models.Task.project_id == project_id)
        all_tasks = self.db.scalars(stmt.order_by(models.Task.id)).all()
        by_id = {t.id: t for t in all_tasks}
        roots = []
        for t in all_tasks:
            if t.parent_task_id and t.parent_task_id in by_id:
                parent = by_id[t.parent_task_id]
                if not hasattr(parent, "_subtasks"):
                    parent._subtasks = []
                parent._subtasks.append(t)
            else:
                roots.append(t)
        for t in all_tasks:
            t._subtasks = getattr(t, "_subtasks", [])
        if root_id is not None and root_id in by_id:
            return [by_id[root_id]]
        return roots