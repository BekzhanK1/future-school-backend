from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class ClassroomCourse(Base):
    __tablename__ = "classroom_courses"

    id = Column(Integer, primary_key=True, index=True)
    classroom_id = Column(Integer, ForeignKey("classrooms.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)

    classroom = relationship("Classroom", backref="classroom_courses", lazy="joined")
    course = relationship("Course", backref="classroom_courses", lazy="joined")
