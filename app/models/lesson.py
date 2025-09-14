from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    starts_at = Column(DateTime, nullable=False)
    ends_at = Column(DateTime, nullable=False)
    topic = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    meeting_link = Column(String, nullable=True)

    course = relationship("Course", backref="lessons")
    teacher = relationship("User", backref="lessons")



