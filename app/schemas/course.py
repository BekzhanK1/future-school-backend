from pydantic import BaseModel
from typing import Optional


class CourseBase(BaseModel):
    course_code: str
    name: str
    grade: int
    description: Optional[str] = None


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    course_code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None


class CourseOut(CourseBase):
    id: int

    class Config:
        from_attributes = True
