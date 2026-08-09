from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repositories.tag_repo import TagRepository
from app.schemas import tag as schemas

router = APIRouter(prefix="/tags", tags=["tags"])


@router.post("", response_model=schemas.TagOut, status_code=201)
def create_tag(data: schemas.TagCreate, db: Session = Depends(get_db)):
    repo = TagRepository(db)
    if repo.get_by_name(data.name):
        raise HTTPException(status_code=400, detail="Tag already exists")
    return repo.create(data)


@router.get("", response_model=list[schemas.TagOut])
def list_tags(db: Session = Depends(get_db)):
    return TagRepository(db).list()