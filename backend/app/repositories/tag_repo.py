from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import select
from app import models
from app.schemas import tag as schemas


class TagRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, tag_id: int):
        return self.db.get(models.Tag, tag_id)

    def get_by_name(self, name: str):
        return self.db.scalar(select(models.Tag).where(models.Tag.name == name))

    def list(self):
        return self.db.scalars(select(models.Tag).order_by(models.Tag.name)).all()

    def create(self, data: schemas.TagCreate):
        obj = models.Tag(name=data.name, color=data.color)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get_or_create(self, name: str, color: str | None = None):
        tag = self.get_by_name(name)
        if tag:
            return tag
        return self.create(schemas.TagCreate(name=name, color=color))

    def delete(self, tag: models.Tag):
        self.db.delete(tag)
        self.db.commit()