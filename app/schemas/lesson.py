from datetime import datetime
from pydantic import BaseModel


class LessonCreate(BaseModel):
    course_id: int
    starts_at: datetime
    ends_at: datetime
    topic: str
    description: str | None = None


class LessonOut(BaseModel):
    id: int
    course_id: int
    teacher_id: int
    starts_at: datetime
    ends_at: datetime
    topic: str
    description: str | None = None
    meeting_link: str | None = None

    class Config:
        from_attributes = True


