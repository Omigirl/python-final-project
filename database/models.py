from sqlalchemy import Column, Integer, String, ForeignKey, Date
from database.db import Base, SessionLocal
from enum import Enum


session = SessionLocal()


class TaskStatuses(Enum):
    TODO: str = "To do"
    DOING: str = "Doing"
    DONE: str = "Done"


def save_obj(obj):
    session.add(obj)
    session.commit()
    session.refresh(obj)


class User(Base):
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(500), nullable=False)
    session_id = Column(String(100), nullable=True)

    def __repr__(self):
        return f"{self.id}. {self.username}"


class Project(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    admin = Column(Integer, ForeignKey("user.id"))


class ProjectMember(Base):
    id = Column(Integer, primary_key=True)
    project = Column(Integer, ForeignKey("project.id"), nullable=False)
    user = Column(Integer, ForeignKey("user.id"), nullable=False)


class Task(Base):
    id = Column(Integer, primary_key=True)
    text = Column(String(500), nullable=False)
    user = Column(Integer, ForeignKey("project_member.id"), nullable=False)
    deadline = Column(Date, nullable=False)
    status = Column(String, nullable=False)
