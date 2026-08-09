from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import select
from app import models
from app.schemas import user as schemas
from app.core.security import get_password_hash


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, user_id: int):
        return self.db.get(models.User, user_id)

    def get_by_username(self, username: str):
        return self.db.scalar(select(models.User).where(models.User.username == username))

    def get_by_email(self, email: str):
        return self.db.scalar(select(models.User).where(models.User.email == email))

    def list(self, skip: int = 0, limit: int = 100):
        return self.db.scalars(select(models.User).offset(skip).limit(limit)).all()

    def create(self, data: schemas.UserCreate):
        obj = models.User(
            username=data.username,
            email=data.email,
            full_name=data.full_name,
            hashed_password=get_password_hash(data.password),
        )
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, user: models.User, data: schemas.UserUpdate):
        for field, value in data.model_dump(exclude_unset=True).items():
            if field == "password" and value:
                setattr(user, "hashed_password", get_password_hash(value))
            else:
                setattr(user, field, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: models.User):
        self.db.delete(user)
        self.db.commit()