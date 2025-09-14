from pydantic import BaseModel, field_validator
from typing import Optional, List


class CourseBase(BaseModel):
    course_code: str
    name: str
    grade: int
    description: Optional[str] = None

    @field_validator("grade")
    def validate_grade(cls, v: int) -> int:
        if not (1 <= v <= 12):
            raise ValueError("Grade must be between 1 and 12.")
        return v

    @field_validator("course_code")
    def validate_course_code(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Course code cannot be empty.")
        return v.strip().upper()

    @field_validator("name")
    def validate_name(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Course name cannot be empty.")
        return v.strip()


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    course_code: Optional[str] = None
    name: Optional[str] = None
    grade: Optional[int] = None
    description: Optional[str] = None

    @field_validator("grade")
    def validate_grade(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and not (1 <= v <= 12):
            raise ValueError("Grade must be between 1 and 12.")
        return v

    @field_validator("course_code")
    def validate_course_code(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("Course code cannot be empty.")
        return v.strip().upper() if v else v

    @field_validator("name")
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("Course name cannot be empty.")
        return v.strip() if v else v


class CourseOut(CourseBase):
    id: int

    class Config:
        from_attributes = True


class BulkCourseCreate(BaseModel):
    courses: List[CourseCreate]

    @field_validator("courses")
    def validate_courses(cls, v: List[CourseCreate]) -> List[CourseCreate]:
        if not v:
            raise ValueError("Courses list cannot be empty.")
        if len(v) > 50:  # Reasonable limit for bulk operations
            raise ValueError("Cannot create more than 50 courses at once.")
        return v
