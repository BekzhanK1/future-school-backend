from sqlalchemy import Column, Integer, ForeignKey, String, Enum, Text
from sqlalchemy.orm import relationship
import enum

from app.db.base_class import Base


class ResourceType(enum.Enum):
    FILE = "file"
    LINK = "link"


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    course_section_id = Column(Integer, ForeignKey("course_sections.id"), nullable=False)
    type = Column(Enum(ResourceType), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    url = Column(String, nullable=True)  # file path or external link
    position = Column(Integer, nullable=False, default=0)

    section = relationship("CourseSection", backref="resources")



