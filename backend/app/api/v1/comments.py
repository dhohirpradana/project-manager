from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repositories.task_repo import TaskRepository
from app.repositories.comment_repo import CommentRepository
from app.schemas import comment as schemas

router = APIRouter(prefix="/tasks/{task_id}/comments", tags=["comments"])


@router.post("", response_model=schemas.CommentOut, status_code=201)
def add_comment(task_id: int, data: schemas.CommentBase, author_id: int = 1, db: Session = Depends(get_db)):
    if not TaskRepository(db).get(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return CommentRepository(db).create(schemas.CommentCreate(task_id=task_id, content=data.content), author_id=author_id)


@router.get("", response_model=list[schemas.CommentOut])
def list_comments(task_id: int, db: Session = Depends(get_db)):
    if not TaskRepository(db).get(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return CommentRepository(db).list_for_task(task_id)


@router.delete("/{comment_id}", status_code=204)
def delete_comment(task_id: int, comment_id: int, db: Session = Depends(get_db)):
    repo = CommentRepository(db)
    comment = repo.get(comment_id)
    if not comment or comment.task_id != task_id:
        raise HTTPException(status_code=404, detail="Comment not found")
    repo.delete(comment)