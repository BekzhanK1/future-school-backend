from typing import Optional

from pydantic import BaseModel, EmailStr

from app.models.user import UserRole


class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole
    is_active: bool = True
    school_id: Optional[int] = None
    kundelik_id: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True
        use_enum_values = True
