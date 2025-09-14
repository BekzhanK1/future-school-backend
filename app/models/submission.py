from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text, String
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base_class import Base


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    text = Column(Text, nullable=True)
    file_url = Column(String, nullable=True)

    assignment = relationship("Assignment", backref="submissions")
    student = relationship("User", backref="submissions")



