from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Classroom(Base):
    __tablename__ = "classrooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    school = relationship("School", backref="classrooms")
