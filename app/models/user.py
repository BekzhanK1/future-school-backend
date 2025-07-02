import enum

from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class UserRole(enum.Enum):
    SUPERADMIN = "superadmin"
    SCHOOLADMIN = "schooladmin"
    TEACHER = "teacher"
    STUDENT = "student"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.STUDENT, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    kundelik_id = Column(String, unique=True, nullable=True, index=True)

    school_id = Column(Integer, ForeignKey("schools.id"), nullable=True)
    school = relationship("School", backref="users")
