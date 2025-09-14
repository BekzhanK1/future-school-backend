from pydantic import BaseModel, field_validator
from typing import List
from app.schemas.course import CourseOut
from app.schemas.classroom import ClassroomOut
from app.schemas.user import UserMinimalOut


class SubjectGroupCreate(BaseModel):
    course_id: int
    classroom_id: int
    teacher_id: int

    @field_validator("course_id", "classroom_id", "teacher_id")
    def validate_ids(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("ID must be a positive integer.")
        return v


class SubjectGroupOut(BaseModel):
    id: int
    course: CourseOut
    classroom: ClassroomOut
    teacher: UserMinimalOut

    class Config:
        from_attributes = True


class BulkSubjectGroupCreate(BaseModel):
    assignments: List[SubjectGroupCreate]

    @field_validator("assignments")
    def validate_assignments(cls, v: List[SubjectGroupCreate]) -> List[SubjectGroupCreate]:
        if not v:
            raise ValueError("Assignments list cannot be empty.")
        if len(v) > 100:  # Reasonable limit for bulk operations
            raise ValueError("Cannot create more than 100 assignments at once.")
        return v


class SubjectGroupUpdate(BaseModel):
    teacher_id: int | None = None

    @field_validator("teacher_id")
    def validate_teacher_id(cls, v: int | None) -> int | None:
        if v is not None and v <= 0:
            raise ValueError("Teacher ID must be a positive integer.")
        return v
