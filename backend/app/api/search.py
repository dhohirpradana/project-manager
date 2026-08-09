from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from ..core.database import get_db
from ..models.models import Project, Task, User
from .deps import get_current_user

router = APIRouter(prefix="/api/search", tags=["search"])

@router.get("/")
def search(
    q: str = Query(..., min_length=1),
    type: str = Query("all", pattern="^(all|tasks|projects)$"),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Full-text search using PostgreSQL FTS, fallback to ILIKE."""
    projects = db.query(Project).filter(Project.owner_id == current_user.id).all()
    project_ids = [p.id for p in projects]
    results = {"tasks": [], "projects": []}

    if type in ("all", "projects"):
        # FTS on project name
        pq = db.query(Project).filter(
            Project.owner_id == current_user.id,
            func.to_tsvector('english', Project.name).op('@@')(func.plainto_tsquery('english', q))
        )
        results["projects"] = pq.limit(limit).all()
        if not results["projects"]:
            # Fallback ILIKE
            pq = db.query(Project).filter(
                Project.owner_id == current_user.id,
                Project.name.ilike(f"%{q}%")
            )
            results["projects"] = pq.limit(limit).all()

    if type in ("all", "tasks"):
        tq = db.query(Task)
        if project_ids:
            tq = tq.filter(Task.project_id.in_(project_ids))
        else:
            tq = tq.filter(Task.id == -1)
        tq = tq.filter(
            func.to_tsvector('english', Task.title).op('@@')(func.plainto_tsquery('english', q))
        )
        results["tasks"] = tq.limit(limit).all()
        if not results["tasks"]:
            # Fallback ILIKE
            tq = db.query(Task)
            if project_ids:
                tq = tq.filter(Task.project_id.in_(project_ids))
            else:
                tq = tq.filter(Task.id == -1)
            tq = tq.filter(Task.title.ilike(f"%{q}%"))
            results["tasks"] = tq.limit(limit).all()

    return results
