from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class SubjectGroup(Base):
    __tablename__ = "subject_groups"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)  # Subject = Course
    classroom_id = Column(Integer, ForeignKey("classrooms.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("course_id", "classroom_id", name="uq_course_classroom"),
    )

    course = relationship("Course", backref="subject_groups")
    classroom = relationship("Classroom", backref="subject_groups")
    teacher = relationship("User", backref="subject_groups")
