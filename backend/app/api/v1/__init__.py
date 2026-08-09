from fastapi import APIRouter

api_router = APIRouter(prefix="/api/v1")

from app.api.v1 import auth, users, projects, tasks, comments, time_entries, dependencies, activity_logs, attachments, tags

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(projects.router)
api_router.include_router(tasks.router)
api_router.include_router(comments.router)
api_router.include_router(time_entries.router)
api_router.include_router(dependencies.router)
api_router.include_router(activity_logs.router)
api_router.include_router(attachments.router)
api_router.include_router(tags.router)