from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repositories.project_repo import ProjectRepository
from app.schemas import project as schemas

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("", response_model=schemas.ProjectOut, status_code=201)
def create_project(data: schemas.ProjectCreate, created_by: int = 1, db: Session = Depends(get_db)):
    repo = ProjectRepository(db)
    if data.parent_id is not None and not repo.get(data.parent_id):
        raise HTTPException(status_code=400, detail="Parent project not found")
    return repo.create(data, created_by=created_by)


@router.get("", response_model=list[schemas.ProjectOut])
def list_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return ProjectRepository(db).list(skip=skip, limit=limit)


@router.get("/tree", response_model=list[schemas.ProjectTree])
def project_tree(db: Session = Depends(get_db)):
    projects = ProjectRepository(db).build_tree()
    return _serialize_tree(projects)


def _serialize_tree(projects):
    result = []
    for p in projects:
        d = schemas.ProjectOut.model_validate(p).model_dump()
        d["children"] = _serialize_tree(getattr(p, "_children", []))
        result.append(d)
    return result


@router.get("/{project_id}", response_model=schemas.ProjectOut)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = ProjectRepository(db).get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.patch("/{project_id}", response_model=schemas.ProjectOut)
def update_project(project_id: int, data: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    repo = ProjectRepository(db)
    project = repo.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if data.parent_id is not None:
        if data.parent_id == project_id:
            raise HTTPException(status_code=400, detail="Project cannot be its own parent")
        if not repo.get(data.parent_id):
            raise HTTPException(status_code=400, detail="Parent project not found")
    return repo.update(project, data)


@router.delete("/{project_id}", status_code=204)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    repo = ProjectRepository(db)
    project = repo.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    repo.delete(project)