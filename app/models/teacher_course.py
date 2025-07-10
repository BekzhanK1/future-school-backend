from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class TeacherCourse(Base):
    __tablename__ = "teacher_courses"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)

    teacher = relationship("User", backref="teacher_courses")
    course = relationship("Course", backref="teacher_courses")
