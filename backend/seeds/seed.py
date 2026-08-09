#!/usr/bin/env python3
"""Seed demo data for project manager."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import Base, SessionLocal, engine
from app.models import Project, Task, User, Tag, TaskTag, ProjectTag, Comment, TimeEntry, ActivityLog, TaskDependency
from app.core.security import get_password_hash
from datetime import datetime, timedelta

Base.metadata.create_all(bind=engine)

db = SessionLocal()

# User
admin = User(email="admin@pm.local", hashed_password=get_password_hash("admin"), is_active=True, is_superuser=True)
db.add(admin)
db.commit()
db.refresh(admin)

# Tags
tags = {
    "kubernetes": Tag(name="kubernetes"),
    "docker": Tag(name="docker"),
    "database": Tag(name="database"),
    "network": Tag(name="network"),
    "security": Tag(name="security"),
}
for t in tags.values():
    db.add(t)
db.commit()

# Projects
navix = Project(name="NAVIX ONE", description="Main platform", status="ACTIVE", priority="HIGH", created_by=admin.id)
db.add(navix)
db.commit()
db.refresh(navix)

mapic = Project(name="MAPIC", parent_id=navix.id, status="ACTIVE", priority="MEDIUM", created_by=admin.id)
db.add(mapic)
db.commit()
db.refresh(mapic)

mapic_dev = Project(name="DEV", parent_id=mapic.id, status="ACTIVE", priority="HIGH", created_by=admin.id)
mapic_uat = Project(name="UAT", parent_id=mapic.id, status="ACTIVE", priority="MEDIUM", created_by=admin.id)
db.add_all([mapic_dev, mapic_uat])
db.commit()

microservices = Project(name="MICROSERVICES", parent_id=navix.id, status="ACTIVE", priority="HIGH", created_by=admin.id)
db.add(microservices)
db.commit()
db.refresh(microservices)

core = Project(name="CORE", parent_id=microservices.id, status="ACTIVE", priority="HIGH", created_by=admin.id)
authservice = Project(name="AUTHSERVICE", parent_id=microservices.id, status="ACTIVE", priority="HIGH", created_by=admin.id)
mcsvc_db = Project(name="MCSVC-DATABASE", parent_id=microservices.id, status="ACTIVE", priority="URGENT", created_by=admin.id)
db.add_all([core, authservice, mcsvc_db])
db.commit()
db.refresh(mcsvc_db)

mcsvc_db_dev = Project(name="DEV", parent_id=mcsvc_db.id, status="ACTIVE", priority="URGENT", created_by=admin.id)
mcsvc_db_uat = Project(name="UAT", parent_id=mcsvc_db.id, status="ACTIVE", priority="MEDIUM", created_by=admin.id)
db.add_all([mcsvc_db_dev, mcsvc_db_uat])
db.commit()

for name in ["MCSVC-MAILER", "MCSVC-REPORT", "MCSVC-STORAGE"]:
    db.add(Project(name=name, parent_id=microservices.id, status="ACTIVE", priority="MEDIUM", created_by=admin.id))

for name in ["SUPERAPP", "SCHEDULAR", "GELORA", "TERESA", "PROMISE", "PRISMA", "CLARA"]:
    db.add(Project(name=name, parent_id=navix.id, status="ACTIVE", priority="MEDIUM", created_by=admin.id))

db.commit()

# Tasks
t1 = Task(title="Check endpoint", project_id=mapic_dev.id, status="DONE", priority="HIGH", environment="DEV", progress=100, created_by=admin.id, assignee_id=admin.id, estimated_minutes=30, spent_minutes=25)
t2 = Task(title="Check login", project_id=mapic_dev.id, status="DONE", priority="HIGH", environment="DEV", progress=100, created_by=admin.id, assignee_id=admin.id, estimated_minutes=20, spent_minutes=20)
t3 = Task(title="SQL Server connectivity", project_id=mcsvc_db_dev.id, status="BLOCKED", priority="URGENT", environment="DEV", progress=40, created_by=admin.id, assignee_id=admin.id, estimated_minutes=120, spent_minutes=200)
t4 = Task(title="Check DNS", parent_task_id=None, project_id=mcsvc_db_dev.id, status="DONE", priority="HIGH", environment="DEV", progress=100, created_by=admin.id, assignee_id=admin.id, estimated_minutes=15, spent_minutes=15)
t5 = Task(title="NIK validation", project_id=core.id, status="IN_PROGRESS", priority="HIGH", environment="DEV", progress=60, created_by=admin.id, assignee_id=admin.id, estimated_minutes=90, spent_minutes=75)
t6 = Task(title="Regression testing", project_id=mapic_uat.id, status="TODO", priority="MEDIUM", environment="UAT", progress=0, created_by=admin.id, assignee_id=admin.id, estimated_minutes=180)
t7 = Task(title="Documentation", project_id=navix.id, status="TODO", priority="LOW", environment="N/A", progress=0, created_by=admin.id, assignee_id=admin.id, estimated_minutes=240)

db.add_all([t1, t2, t3, t4, t5, t6, t7])
db.commit()
db.refresh(t3)
db.refresh(t4)

# Sub-task
t3_sub1 = Task(title="Check firewall", parent_task_id=t3.id, project_id=mcsvc_db_dev.id, status="DONE", priority="HIGH", environment="DEV", progress=100, created_by=admin.id, assignee_id=admin.id, estimated_minutes=20, spent_minutes=20)
t3_sub2 = Task(title="Check SQL Server", parent_task_id=t3.id, project_id=mcsvc_db_dev.id, status="IN_PROGRESS", priority="URGENT", environment="DEV", progress=50, created_by=admin.id, assignee_id=admin.id, estimated_minutes=60, spent_minutes=80)
db.add_all([t3_sub1, t3_sub2])
db.commit()

# Dependency
dep = TaskDependency(task_id=t3.id, depends_on_task_id=t4.id, dependency_type="DEPENDS_ON")
db.add(dep)
db.commit()

# Tags
db.add(TaskTag(task_id=t3.id, tag_id=tags["database"].id))
db.add(TaskTag(task_id=t4.id, tag_id=tags["network"].id))
db.add(TaskTag(task_id=t5.id, tag_id=tags["security"].id))
db.add(ProjectTag(project_id=mcsvc_db.id, tag_id=tags["database"].id))
db.add(ProjectTag(project_id=microservices.id, tag_id=tags["kubernetes"].id))
db.commit()

# Comments
c1 = Comment(task_id=t3.id, user_id=admin.id, content="SQL Server tidak bisa diakses. Port 11433 perlu dicek firewall.")
c2 = Comment(task_id=t3.id, user_id=admin.id, content="Firewall sudah OK. Issue di SQL Server credentials.")
db.add_all([c1, c2])
db.commit()

# Time entries
te1 = TimeEntry(task_id=t3.id, user_id=admin.id, started_at=datetime.utcnow()-timedelta(hours=5), ended_at=datetime.utcnow()-timedelta(hours=4, minutes=35), duration_minutes=25, description="Initial investigation")
te2 = TimeEntry(task_id=t3.id, user_id=admin.id, started_at=datetime.utcnow()-timedelta(hours=3), ended_at=datetime.utcnow()-timedelta(hours=2, minutes=15), duration_minutes=45, description="Firewall check")
te3 = TimeEntry(task_id=t3.id, user_id=admin.id, started_at=datetime.utcnow()-timedelta(hours=1), ended_at=datetime.utcnow()-timedelta(minutes=10), duration_minutes=50, description="SQL Server troubleshoot")
db.add_all([te1, te2, te3])
db.commit()

# Activity logs
al1 = ActivityLog(entity_type="task", entity_id=t3.id, action="status_change", user_id=admin.id, old_value="TODO", new_value="IN_PROGRESS")
al2 = ActivityLog(entity_type="task", entity_id=t3.id, action="status_change", user_id=admin.id, old_value="IN_PROGRESS", new_value="BLOCKED")
al3 = ActivityLog(entity_type="task", entity_id=t3.id, action="comment_added", user_id=admin.id)
al4 = ActivityLog(entity_type="task", entity_id=t3.id, action="time_added", user_id=admin.id, metadata={"duration_minutes": 50})
db.add_all([al1, al2, al3, al4])
db.commit()

print("✅ Seed complete")
print(f"Users: {db.query(User).count()}")
print(f"Projects: {db.query(Project).count()}")
print(f"Tasks: {db.query(Task).count()}")
print(f"Comments: {db.query(Comment).count()}")
print(f"Time entries: {db.query(TimeEntry).count()}")
print(f"Activity logs: {db.query(ActivityLog).count()}")
print(f"Tags: {db.query(Tag).count()}")

db.close()
