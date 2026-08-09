from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import select
from app import models
from app.schemas import attachment as schemas


class AttachmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, attachment_id: int):
        return self.db.get(models.Attachment, attachment_id)

    def list_for_task(self, task_id: int):
        return self.db.scalars(
            select(models.Attachment).where(models.Attachment.task_id == task_id).order_by(models.Attachment.uploaded_at)
        ).all()

    def create(self, task_id: int, filename: str, file_path: str, file_size: int | None = None, mime_type: str | None = None):
        obj = models.Attachment(
            task_id=task_id, filename=filename, file_path=file_path, file_size=file_size, mime_type=mime_type
        )
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, attachment: models.Attachment):
        self.db.delete(attachment)
        self.db.commit()