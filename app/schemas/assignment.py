from datetime import datetime
from pydantic import BaseModel, field_validator
from typing import Optional


class AssignmentCreate(BaseModel):
    course_id: int
    title: str
    description: str | None = None
    due_at: datetime

    @field_validator("title")
    def validate_title(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Assignment title cannot be empty.")
        return v.strip()

    @field_validator("due_at")
    def validate_due_at(cls, v: datetime) -> datetime:
        if v <= datetime.now():
            raise ValueError("Due date must be in the future.")
        return v


class AssignmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_at: Optional[datetime] = None

    @field_validator("title")
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("Assignment title cannot be empty.")
        return v.strip() if v else v

    @field_validator("due_at")
    def validate_due_at(cls, v: Optional[datetime]) -> Optional[datetime]:
        if v is not None and v <= datetime.now():
            raise ValueError("Due date must be in the future.")
        return v


class AssignmentOut(BaseModel):
    id: int
    course_id: int
    teacher_id: int
    title: str
    description: str | None = None
    due_at: datetime
    created_at: datetime | None = None

    class Config:
        from_attributes = True


class AssignmentWithSubmissions(AssignmentOut):
    submissions: list = []

    class Config:
        from_attributes = True


