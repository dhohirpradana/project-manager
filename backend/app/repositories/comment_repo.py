from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import select
from app import models
from app.schemas import comment as schemas


class CommentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, comment_id: int):
        return self.db.get(models.Comment, comment_id)

    def list_for_task(self, task_id: int):
        return self.db.scalars(
            select(models.Comment).where(models.Comment.task_id == task_id).order_by(models.Comment.created_at)
        ).all()

    def create(self, data: schemas.CommentCreate, author_id: int):
        obj = models.Comment(task_id=data.task_id, content=data.content, author_id=author_id)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, comment: models.Comment, data: schemas.CommentUpdate):
        comment.content = data.content
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def delete(self, comment: models.Comment):
        self.db.delete(comment)
        self.db.commit()