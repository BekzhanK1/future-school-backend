from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base_class import Base


class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"), nullable=False)
    graded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    grade_value = Column(Integer, nullable=False)
    feedback = Column(Text, nullable=True)
    graded_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    submission = relationship("Submission", backref="grade")
    teacher = relationship("User")



