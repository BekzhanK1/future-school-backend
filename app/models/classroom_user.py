from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class ClassroomUser(Base):
    __tablename__ = "classroom_users"
    id = Column(Integer, primary_key=True, index=True)
    classroom_id = Column(Integer, ForeignKey("classrooms.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("classroom_id", "user_id", name="_class_user_uc"),
    )

    classroom = relationship("Classroom", backref="classroom_users")
    user = relationship("User", backref="classroom_users")
