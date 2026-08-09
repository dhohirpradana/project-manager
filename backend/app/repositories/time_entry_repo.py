from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app import models
from app.schemas import time_entry as schemas


class TimeEntryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, entry_id: int):
        return self.db.get(models.TimeEntry, entry_id)

    def list_for_task(self, task_id: int):
        return self.db.scalars(
            select(models.TimeEntry).where(models.TimeEntry.task_id == task_id).order_by(models.TimeEntry.logged_at)
        ).all()

    def total_minutes_for_task(self, task_id: int):
        return self.db.scalar(
            select(func.coalesce(func.sum(models.TimeEntry.minutes), 0)).where(models.TimeEntry.task_id == task_id)
        ) or 0

    def create(self, data: schemas.TimeEntryCreate, user_id: int):
        obj = models.TimeEntry(task_id=data.task_id, minutes=data.minutes, description=data.description, user_id=user_id)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, entry: models.TimeEntry):
        self.db.delete(entry)
        self.db.commit()