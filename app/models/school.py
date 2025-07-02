from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class School(Base):
    __tablename__ = "schools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False, default="Kazakhstan")
    logo_url = Column(String, nullable=True)
    contact_email = Column(String, nullable=True)
    contact_phone = Column(String, nullable=True)
    kundelik_id = Column(String, unique=True, nullable=True, index=True)
