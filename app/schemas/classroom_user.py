from pydantic import BaseModel
from app.schemas.classroom import ClassroomOut
from app.schemas.user import UserOut


class ClassroomUserBase(BaseModel):
    classroom_id: int
    user_id: int


class ClassroomUserCreate(ClassroomUserBase):
    pass


class ClassroomUserOut(BaseModel):
    id: int
    classroom: ClassroomOut
    user: UserOut

    class Config:
        from_attributes = True
        # allow_population_by_field_name = True
