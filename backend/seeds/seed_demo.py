#!/usr/bin/env python3
"""
Seed script for Project Manager demo data.
Creates admin user, projects hierarchy, tasks, comments, tags, time entries, activity logs, dependencies.
"""
import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.core.security import get_password_hash
from app.models import User, Project, Task, Comment, TimeEntry, ActivityLog, Tag, TaskDependency
from app.models.project import ProjectStatus, Priority as ProjectPriority
from app.models.task import TaskStatus, Priority as TaskPriority

# Use SQLite for demo (no PG running)
DATABASE_URL = "sqlite:///./projectmanager.db"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

def seed_data():
    """Create all tables and seed demo data."""
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        print("Seeding demo data...")
        
        # 1. Create demo user (admin/admin)
        admin = User(
            email="admin@example.com",
            hashed_password=get_password_hash("admin")
        )
        db.add(admin)
        db.flush()
        print(f"✓ Created user: {admin.email}")
        
        # 2. Create tags
        tags = {
            "kubernetes": Tag(name="kubernetes", color="#326CE5"),
            "docker": Tag(name="docker", color="#2496ED"),
            "database": Tag(name="database", color="#336791"),
            "network": Tag(name="network", color="#FF6B6B"),
            "security": Tag(name="security", color="#F59E0B")
        }
        for tag in tags.values():
            db.add(tag)
        db.flush()
        print(f"✓ Created {len(tags)} tags")
        
        # 3. Create project hierarchy: NAVIX ONE (parent)
        navix_one = Project(
            name="NAVIX ONE",
            description="Main platform for navigation and mapping services",
            status=ProjectStatus.ACTIVE,
            priority=ProjectPriority.HIGH,
            created_by=admin.id,
            start_date=datetime.now() - timedelta(days=180)
        )
        db.add(navix_one)
        db.flush()
        
        # MAPIC (child of NAVIX ONE)
        mapic = Project(
            name="MAPIC",
            description="Mapping and cartography service",
            parent_id=navix_one.id,
            status=ProjectStatus.ACTIVE,
            priority=ProjectPriority.HIGH,
            created_by=admin.id,
            start_date=datetime.now() - timedelta(days=150)
        )
        db.add(mapic)
        db.flush()
        
        # MAPIC environments
        mapic_dev = Project(
            name="MAPIC - DEV",
            description="Development environment for MAPIC",
            parent_id=mapic.id,
            status=ProjectStatus.ACTIVE,
            priority=ProjectPriority.MEDIUM,
            created_by=admin.id
        )
        mapic_uat = Project(
            name="MAPIC - UAT",
            description="UAT environment for MAPIC",
            parent_id=mapic.id,
            status=ProjectStatus.ACTIVE,
            priority=ProjectPriority.MEDIUM,
            created_by=admin.id
        )
        db.add_all([mapic_dev, mapic_uat])
        db.flush()
        
        # MICROSERVICES (child of NAVIX ONE)
        microservices = Project(
            name="MICROSERVICES",
            description="Microservices architecture for NAVIX ONE",
            parent_id=navix_one.id,
            status=ProjectStatus.ACTIVE,
            priority=ProjectPriority.URGENT,
            created_by=admin.id,
            start_date=datetime.now() - timedelta(days=120)
        )
        db.add(microservices)
        db.flush()
        
        # Microservice projects
        ms_projects = [
            ("CORE", "Core microservice - business logic"),
            ("AUTHSERVICE", "Authentication and authorization service"),
            ("MCSVC-DATABASE", "Database management service"),
            ("MCSVC-MAILER", "Email notification service"),
            ("MCSVC-REPORT", "Reporting and analytics service"),
            ("MCSVC-STORAGE", "File storage service")
        ]
        
        for name, desc in ms_projects:
            proj = Project(
                name=name,
                description=desc,
                parent_id=microservices.id,
                status=ProjectStatus.ACTIVE,
                priority=ProjectPriority.HIGH,
                created_by=admin.id
            )
            db.add(proj)
        db.flush()
        
        # MCSVC-DATABASE environments
        mcsvc_db = db.query(Project).filter_by(name="MCSVC-DATABASE").first()
        mcsvc_db_dev = Project(
            name="MCSVC-DATABASE - DEV",
            description="Dev environment for database service",
            parent_id=mcsvc_db.id,
            status=ProjectStatus.ACTIVE,
            priority=ProjectPriority.MEDIUM,
            created_by=admin.id
        )
        mcsvc_db_uat = Project(
            name="MCSVC-DATABASE - UAT",
            description="UAT environment for database service",
            parent_id=mcsvc_db.id,
            status=ProjectStatus.ACTIVE,
            priority=ProjectPriority.MEDIUM,
            created_by=admin.id
        )
        db.add_all([mcsvc_db_dev, mcsvc_db_uat])
        db.flush()
        
        # Other standalone projects
        standalone = [
            ("SUPERAPP", "Super application platform", ProjectStatus.ACTIVE, ProjectPriority.HIGH),
            ("SCHEDULAR", "Task scheduling and orchestration", ProjectStatus.ACTIVE, ProjectPriority.MEDIUM),
            ("GELORA", "Sports management system", ProjectStatus.PLANNED, ProjectPriority.MEDIUM),
            ("TERESA", "HR and employee management", ProjectStatus.ACTIVE, ProjectPriority.LOW),
            ("PROMISE", "Promise tracking system", ProjectStatus.ON_HOLD, ProjectPriority.LOW),
            ("PRISMA", "Data visualization platform", ProjectStatus.ACTIVE, ProjectPriority.MEDIUM),
            ("CLARA", "Customer relationship assistant", ProjectStatus.PLANNED, ProjectPriority.HIGH)
        ]
        
        for name, desc, status, priority in standalone:
            proj = Project(
                name=name,
                description=desc,
                status=status,
                priority=priority,
                created_by=admin.id,
                start_date=datetime.now() - timedelta(days=90)
            )
            db.add(proj)
        db.flush()
        
        project_count = db.query(Project).count()
        print(f"✓ Created {project_count} projects")
        
        # 4. Create tasks for various projects
        all_projects = db.query(Project).all()
        task_templates = [
            ("Check endpoint", "Verify API endpoint responds correctly", TaskStatus.DONE, TaskPriority.HIGH, ["network"]),
            ("Check login", "Test authentication flow", TaskStatus.DONE, TaskPriority.URGENT, ["security"]),
            ("Check database", "Verify database connection and queries", TaskStatus.IN_PROGRESS, TaskPriority.HIGH, ["database"]),
            ("Check DNS", "Verify DNS resolution", TaskStatus.BLOCKED, TaskPriority.MEDIUM, ["network"]),
            ("Regression testing", "Run full regression test suite", TaskStatus.TODO, TaskPriority.MEDIUM, ["kubernetes", "docker"]),
            ("Documentation", "Update project documentation", TaskStatus.TODO, TaskPriority.LOW, [])
        ]
        
        created_tasks = []
        for i, project in enumerate(all_projects[:10]):  # Add tasks to first 10 projects
            for j, (title, desc, status, priority, tag_names) in enumerate(task_templates):
                if j > i % 4:  # Vary number of tasks per project
                    break
                    
                task = Task(
                    project_id=project.id,
                    title=title,
                    description=desc,
                    status=status,
                    priority=priority,
                    created_by=admin.id,
                    assignee_id=admin.id if status != TaskStatus.TODO else None,
                    estimated_minutes=120 + (j * 30),
                    spent_minutes=60 if status in [TaskStatus.DONE, TaskStatus.IN_PROGRESS] else 0,
                    progress=100.0 if status == TaskStatus.DONE else (50.0 if status == TaskStatus.IN_PROGRESS else 0.0),
                    created_at=datetime.now() - timedelta(days=30-i),
                    completed_at=datetime.now() - timedelta(days=i) if status == TaskStatus.DONE else None
                )
                db.add(task)
                db.flush()
                
                # Add tags
                for tag_name in tag_names:
                    if tag_name in tags:
                        task.tags.append(tags[tag_name])
                
                created_tasks.append(task)
        
        db.flush()
        task_count = db.query(Task).count()
        print(f"✓ Created {task_count} tasks")
        
        # 5. Create task dependencies
        if len(created_tasks) >= 3:
            dep1 = TaskDependency(
                task_id=created_tasks[2].id,
                depends_on_task_id=created_tasks[0].id
            )
            dep2 = TaskDependency(
                task_id=created_tasks[3].id,
                depends_on_task_id=created_tasks[1].id
            )
            db.add_all([dep1, dep2])
            print(f"✓ Created 2 task dependencies")
        
        # 6. Create comments
        comment_texts = [
            "Started working on this task",
            "Need to review the requirements",
            "Blocked by infrastructure issue",
            "Completed successfully",
            "Found some issues, need follow-up"
        ]
        
        comment_count = 0
        for task in created_tasks[:8]:  # Add comments to first 8 tasks
            for i in range((task.id % 3) + 1):
                comment = Comment(
                    task_id=task.id,
                    author_id=admin.id,
                    content=comment_texts[i % len(comment_texts)],
                    created_at=datetime.now() - timedelta(days=10-i)
                )
                db.add(comment)
                comment_count += 1
        
        db.flush()
        print(f"✓ Created {comment_count} comments")
        
        # 7. Create time entries
        time_entry_count = 0
        for task in created_tasks:
            if task.spent_minutes > 0:
                # Split spent time into 1-3 entries
                entries = 2 if task.spent_minutes > 60 else 1
                minutes_per_entry = task.spent_minutes // entries
                
                for i in range(entries):
                    entry = TimeEntry(
                        task_id=task.id,
                        user_id=admin.id,
                        minutes=minutes_per_entry,
                        description=f"Work session {i+1}",
                        logged_at=datetime.now() - timedelta(days=5+i)
                    )
                    db.add(entry)
                    time_entry_count += 1
        
        db.flush()
        print(f"✓ Created {time_entry_count} time entries")
        
        # 8. Create activity logs
        activity_count = 0
        for task in created_tasks:
            # Task created
            log = ActivityLog(
                task_id=task.id,
                user_id=admin.id,
                action="created",
                details=f"Task created in project",
                created_at=task.created_at
            )
            db.add(log)
            activity_count += 1
            
            # Status changes
            if task.status in [TaskStatus.IN_PROGRESS, TaskStatus.DONE]:
                log = ActivityLog(
                    task_id=task.id,
                    user_id=admin.id,
                    action="status_change",
                    details=f"Status changed to IN_PROGRESS",
                    created_at=task.created_at + timedelta(hours=2)
                )
                db.add(log)
                activity_count += 1
            
            if task.status == TaskStatus.DONE:
                log = ActivityLog(
                    task_id=task.id,
                    user_id=admin.id,
                    action="status_change",
                    details=f"Status changed to DONE",
                    created_at=task.completed_at
                )
                db.add(log)
                activity_count += 1
        
        db.flush()
        print(f"✓ Created {activity_count} activity logs")
        
        # Commit everything
        db.commit()
        print("\n✅ Seed complete!")
        
        # Print summary
        print("\n📊 Summary:")
        print(f"  Users: {db.query(User).count()}")
        print(f"  Projects: {db.query(Project).count()}")
        print(f"  Tasks: {db.query(Task).count()}")
        print(f"  Tags: {db.query(Tag).count()}")
        print(f"  Comments: {db.query(Comment).count()}")
        print(f"  Time Entries: {db.query(TimeEntry).count()}")
        print(f"  Activity Logs: {db.query(ActivityLog).count()}")
        print(f"  Task Dependencies: {db.query(TaskDependency).count()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = seed_data()
    sys.exit(0 if success else 1)
