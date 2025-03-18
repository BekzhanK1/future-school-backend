from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from enum import Enum
from app.models.school_class import SchoolClass


class UserRole(str, Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    CURATOR = "curator"
    ADMIN = "admin"


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(index=True)
    username: str = Field(index=True, unique=True)
    role: UserRole = Field(default=UserRole.USER)
    school_class_id: int | None = Field(default=None, foreign_key="schoolclass.id")
    school_class: SchoolClass | None = None
