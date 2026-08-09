from sqlalchemy.orm import Session
from app.repositories.task_repo import TaskRepository
from app.repositories.time_entry_repo import TimeEntryRepository
from app.repositories.dependency_repo import DependencyRepository
from app.repositories.activity_log_repo import ActivityLogRepository
from app.models.task import TaskStatus
from app.schemas.time_entry import TimeEntryCreate
from app.schemas.dependency import DependencyCreate


class TaskService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = TaskRepository(db)
        self.time_repo = TimeEntryRepository(db)
        self.dep_repo = DependencyRepository(db)
        self.activity_repo = ActivityLogRepository(db)

    def _iter_subtree(self, task_id: int) -> list[object]:
        """Collect a task and all its descendants (BFS)."""
        result = []
        queue = [task_id]
        while queue:
            current = queue.pop(0)
            task = self.repo.get(current)
            if task is None:
                continue
            result.append(task)
            queue.extend(st.id for st in self.repo.get_subtasks(current))
        return result

    def recalc_progress(self, task_id: int) -> float:
        """Auto-calculate progress from subtasks.

        If a task has subtasks, progress = weighted average of subtitle progress
        (weighted by estimated_minutes, or equal weight if none). Leaf tasks keep
        their own progress value.

        Returns the calculated progress and persists it.
        """
        task = self.repo.get(task_id)
        if task is None:
            return 0.0
        subtasks = self.repo.get_subtasks(task_id)
        if not subtasks:
            return task.progress

        total = 0.0
        weight = 0.0
        for st in subtasks:
            st_progress = self.recalc_progress(st.id)
            w = st.estimated_minutes or 1
            total += st_progress * w
            weight += w
        progress = round(total / weight, 2) if weight else 0.0

        task.progress = progress
        if all(st.status == TaskStatus.DONE for st in subtasks):
            task.status = TaskStatus.DONE
        self.db.commit()
        return progress

    def log_time(self, task_id: int, user_id: int, minutes: int, description: str | None = None):
        entry = self.time_repo.create(
            TimeEntryCreate(task_id=task_id, minutes=minutes, description=description),
            user_id=user_id,
        )
        total = self.time_repo.total_minutes_for_task(task_id)
        task = self.repo.get(task_id)
        if task:
            task.spent_minutes = total
            self.db.commit()
        return entry

    def check_circular_dependency(self, task_id: int, depends_on_task_id: int) -> bool:
        """Return True if adding dependency task_id -> depends_on_task_id creates a cycle.

        A cycle exists if depends_on_task_id (transitively) already depends on task_id.
        """
        if task_id == depends_on_task_id:
            return True
        # BFS from depends_on_task_id through its dependencies
        visited = set()
        queue = [depends_on_task_id]
        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            if current == task_id:
                return True
            for dep in self.dep_repo.list_for_task(current):
                queue.append(dep.depends_on_task_id)
        return False

    def add_dependency(self, task_id: int, depends_on_task_id: int):
        if self.check_circular_dependency(task_id, depends_on_task_id):
            raise ValueError("Circular dependency would be created")
        if self.dep_repo.exists(task_id, depends_on_task_id):
            raise ValueError("Dependency already exists")
        return self.dep_repo.create(
            DependencyCreate(task_id=task_id, depends_on_task_id=depends_on_task_id)
        )