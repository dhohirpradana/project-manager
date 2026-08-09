#!/usr/bin/env python3
"""Raw SQL seed bypass SQLAlchemy ORM metadata cache bug."""
import psycopg2
from datetime import datetime, timedelta
import bcrypt
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@postgres:5432/project_db")
# Convert SQLAlchemy URL format to psycopg2
db_url = DATABASE_URL.replace("postgresql+psycopg2://", "postgresql://").replace("@localhost:", "@postgres:")

conn = psycopg2.connect(db_url)
cur = conn.cursor()

# Hash passwords
admin_hash = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode()
user_hash = bcrypt.hashpw("user123".encode(), bcrypt.gensalt()).decode()

# Insert users
cur.execute("""
    INSERT INTO users (email, hashed_password, is_active, is_superuser, created_at)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING id
""", ("admin@pm.local", admin_hash, True, True, datetime.utcnow()))
admin_id = cur.fetchone()[0]

cur.execute("""
    INSERT INTO users (email, hashed_password, is_active, is_superuser, created_at)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING id
""", ("user@pm.local", user_hash, True, False, datetime.utcnow()))
user_id = cur.fetchone()[0]

# Insert tags
cur.execute("""
    INSERT INTO tags (name, color) VALUES
    ('backend', '#3b82f6'),
    ('frontend', '#10b981'),
    ('urgent', '#ef4444'),
    ('bug', '#f59e0b')
    RETURNING id
""")
tag_ids = [row[0] for row in cur.fetchall()]

# Insert project
cur.execute("""
    INSERT INTO projects (name, description, status, created_by, created_at)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING id
""", ("MVP Development", "Project Manager MVP", "active", admin_id, datetime.utcnow()))
project_id = cur.fetchone()[0]

# Insert tasks
cur.execute("""
    INSERT INTO tasks (title, description, status, priority, project_id, created_by, assignee_id, created_at, due_date)
    VALUES 
    (%s, %s, %s, %s, %s, %s, %s, %s, %s),
    (%s, %s, %s, %s, %s, %s, %s, %s, %s),
    (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id
""", (
    "Backend API", "Build REST API", "in_progress", "high", project_id, admin_id, admin_id, datetime.utcnow(), datetime.utcnow() + timedelta(days=7),
    "Frontend UI", "Build Vue dashboard", "todo", "high", project_id, admin_id, user_id, datetime.utcnow(), datetime.utcnow() + timedelta(days=14),
    "Docker Setup", "Compose stack", "done", "medium", project_id, admin_id, admin_id, datetime.utcnow() - timedelta(days=2), datetime.utcnow() - timedelta(days=1)
))
task_ids = [row[0] for row in cur.fetchall()]

# Insert comment
cur.execute("""
    INSERT INTO comments (content, task_id, author_id, created_at)
    VALUES (%s, %s, %s, %s)
""", ("Passlib bcrypt bug fixed, using pure bcrypt now", task_ids[0], admin_id, datetime.utcnow()))

# Insert time entry
cur.execute("""
    INSERT INTO time_entries (task_id, user_id, start_time, end_time, duration_seconds, description)
    VALUES (%s, %s, %s, %s, %s, %s)
""", (task_ids[0], admin_id, datetime.utcnow() - timedelta(hours=2), datetime.utcnow(), 7200, "Fixed backend bcrypt import"))

conn.commit()
cur.close()
conn.close()

print("✅ Seed complete:")
print(f"   Users: admin@pm.local (admin123), user@pm.local (user123)")
print(f"   Project: MVP Development")
print(f"   Tasks: 3 (1 done, 1 in_progress, 1 todo)")
print(f"   Tags: 4 (backend, frontend, urgent, bug)")
