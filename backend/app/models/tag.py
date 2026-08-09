from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

task_tags = Table(
    'task_tags',
    Base.metadata,
    Column('task_id', Integer, ForeignKey('tasks.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

project_tags = Table(
    'project_tags',
    Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    color = Column(String)

    # Relationships
    tasks = relationship("Task", secondary=task_tags, backref="tags")
    projects = relationship("Project", secondary=project_tags, backref="tags")

class TaskTag(Base):
    __tablename__ = "task_tags"
    __table_args__ = {'extend_existing': True}
    task_id = Column(Integer, ForeignKey('tasks.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)

class ProjectTag(Base):
    __tablename__ = "project_tags"
    __table_args__ = {'extend_existing': True}
    project_id = Column(Integer, ForeignKey('projects.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)
