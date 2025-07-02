from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    CheckConstraint,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Classroom(Base):
    __tablename__ = "classrooms"

    __table_args__ = (
        CheckConstraint("grade BETWEEN 0 AND 12", name="check_grade_range"),
        UniqueConstraint(
            "school_id", "grade", "letter", name="uq_classroom_per_school"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    grade = Column(
        Integer,
        nullable=False,
        comment="Grade level of the classroom, e.g., 1 for Grade 1",
    )
    letter = Column(
        String(1),
        nullable=False,
        comment="Letter designation of the classroom, e.g., 'A' for Grade 1A",
    )
    language = Column(
        String(50),
        nullable=False,
        comment="Primary language of instruction in the classroom",
    )

    kundelik_id = Column(
        String(50),
        unique=True,
        nullable=True,
        index=True,
        comment="Unique identifier for the classroom in the Kundelik system",
    )

    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    school = relationship("School", backref="classrooms")
