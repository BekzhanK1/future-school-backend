from pydantic import BaseModel
from typing import Optional


class TeacherCourseBase(BaseModel):
    teacher_id: int
    course_id: int


class TeacherCourseCreate(TeacherCourseBase):
    pass


class TeacherCourseUpdate(BaseModel):
    teacher_id: Optional[int] = None
    course_id: Optional[int] = None


class TeacherCourseOut(TeacherCourseBase):
    id: int

    class Config:
        from_attributes = True
