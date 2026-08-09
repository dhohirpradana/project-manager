from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import select
from app import models
from app.schemas import activity_log as schemas


class ActivityLogRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_for_task(self, task_id: int):
        return self.db.scalars(
            select(models.ActivityLog).where(models.ActivityLog.task_id == task_id).order_by(models.ActivityLog.created_at.desc())
        ).all()

    def create(self, task_id: int, user_id: int, action: str, details: str | None = None):
        obj = models.ActivityLog(task_id=task_id, user_id=user_id, action=action, details=details)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj