from sqlalchemy import CheckConstraint, Column, Integer, String
from app.db.base_class import Base


class Course(Base):
    __tablename__ = "courses"

    __table_args__ = (
        CheckConstraint("grade BETWEEN 0 AND 12", name="check_course_grade_range"),
    )

    id = Column(Integer, primary_key=True, index=True)
    course_code = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    grade = Column(
        Integer,
        nullable=True,
        comment="Grade level of the classroom, e.g., 1 for Grade 1",
    )
