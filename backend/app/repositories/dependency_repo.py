from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import select
from app import models
from app.schemas import dependency as schemas


class DependencyRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, dependency_id: int):
        return self.db.get(models.TaskDependency, dependency_id)

    def list_for_task(self, task_id: int):
        return self.db.scalars(
            select(models.TaskDependency).where(models.TaskDependency.task_id == task_id)
        ).all()

    def list_blocked_by(self, task_id: int):
        """Tasks that this task depends on."""
        return self.db.scalars(
            select(models.TaskDependency).where(models.TaskDependency.task_id == task_id)
        ).all()

    def create(self, data: schemas.DependencyCreate):
        obj = models.TaskDependency(task_id=data.task_id, depends_on_task_id=data.depends_on_task_id)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def exists(self, task_id: int, depends_on_task_id: int) -> bool:
        return self.db.scalar(
            select(models.TaskDependency).where(
                models.TaskDependency.task_id == task_id,
                models.TaskDependency.depends_on_task_id == depends_on_task_id,
            )
        ) is not None

    def delete(self, dependency: models.TaskDependency):
        self.db.delete(dependency)
        self.db.commit()