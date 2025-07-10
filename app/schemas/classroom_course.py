from pydantic import BaseModel
from typing import Optional
from app.schemas.course import CourseOut
from app.schemas.classroom import ClassroomOut


class ClassroomCourseBase(BaseModel):
    classroom_id: int
    course_id: int


class ClassroomCourseCreate(ClassroomCourseBase):
    pass


class ClassroomCourseUpdate(BaseModel):
    classroom_id: Optional[int] = None
    course_id: Optional[int] = None


class ClassroomCourseOut(ClassroomCourseBase):
    id: int
    classroom: ClassroomOut
    course: CourseOut

    class Config:
        from_attributes = True
