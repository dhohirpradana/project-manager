from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repositories.task_repo import TaskRepository
from app.repositories.attachment_repo import AttachmentRepository
from app.schemas import attachment as schemas
from pydantic import BaseModel


class AttachmentCreate(BaseModel):
    filename: str
    file_path: str
    file_size: int | None = None
    mime_type: str | None = None


router = APIRouter(prefix="/tasks/{task_id}/attachments", tags=["attachments"])


@router.post("", response_model=schemas.AttachmentOut, status_code=201)
def add_attachment(task_id: int, data: AttachmentCreate, db: Session = Depends(get_db)):
    if not TaskRepository(db).get(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return AttachmentRepository(db).create(
        task_id, data.filename, data.file_path, data.file_size, data.mime_type
    )


@router.get("", response_model=list[schemas.AttachmentOut])
def list_attachments(task_id: int, db: Session = Depends(get_db)):
    if not TaskRepository(db).get(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return AttachmentRepository(db).list_for_task(task_id)