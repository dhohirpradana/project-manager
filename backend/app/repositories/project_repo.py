from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import select
from app import models
from app.schemas import project as schemas


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, project_id: int):
        return self.db.get(models.Project, project_id)

    def get_children(self, parent_id: int):
        return self.db.scalars(
            select(models.Project).where(models.Project.parent_id == parent_id).order_by(models.Project.name)
        ).all()

    def list(self, skip: int = 0, limit: int = 100):
        return self.db.scalars(select(models.Project).offset(skip).limit(limit)).all()

    def list_roots(self):
        return self.db.scalars(
            select(models.Project).where(models.Project.parent_id.is_(None)).order_by(models.Project.name)
        ).all()

    def create(self, data: schemas.ProjectCreate, created_by: int):
        obj = models.Project(**data.model_dump(), created_by=created_by)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, project: models.Project, data: schemas.ProjectUpdate):
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(project, field, value)
        self.db.commit()
        self.db.refresh(project)
        return project

    def delete(self, project: models.Project):
        self.db.delete(project)
        self.db.commit()

    def build_tree(self, root_id: int | None = None) -> list[models.Project]:
        """Load all projects and assemble a nested tree in memory."""
        all_projects = self.db.scalars(select(models.Project).order_by(models.Project.id)).all()
        by_id = {p.id: p for p in all_projects}
        roots = []
        for p in all_projects:
            if p.parent_id and p.parent_id in by_id:
                parent = by_id[p.parent_id]
                if not hasattr(parent, "_children"):
                    parent._children = []
                parent._children.append(p)
            else:
                roots.append(p)

        # Attach child lists to the Project objects for serialization
        for p in all_projects:
            p._children = getattr(p, "_children", [])

        if root_id is not None and root_id in by_id:
            return [by_id[root_id]]
        return roots