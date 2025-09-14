from pydantic import BaseModel, field_validator
from typing import List
from app.schemas.classroom import ClassroomOut
from app.schemas.user import UserOut, UserMinimalOut


class ClassroomUserBase(BaseModel):
    classroom_id: int
    user_id: int


class ClassroomUserCreate(ClassroomUserBase):
    pass


class BulkStudentEnrollment(BaseModel):
    classroom_id: int
    student_ids: List[int]

    @field_validator("student_ids")
    def validate_student_ids(cls, v: List[int]) -> List[int]:
        if not v:
            raise ValueError("Student IDs list cannot be empty.")
        if len(v) > 50:  # Reasonable limit for bulk operations
            raise ValueError("Cannot enroll more than 50 students at once.")
        return v


class BulkStudentCreate(BaseModel):
    classroom_id: int
    students: List[dict]  # [{"first_name": "John", "last_name": "Doe", "email": "john@example.com"}]

    @field_validator("students")
    def validate_students(cls, v: List[dict]) -> List[dict]:
        if not v:
            raise ValueError("Students list cannot be empty.")
        if len(v) > 50:
            raise ValueError("Cannot create more than 50 students at once.")
        
        for student in v:
            required_fields = ["first_name", "last_name", "email"]
            for field in required_fields:
                if field not in student or not student[field]:
                    raise ValueError(f"Each student must have {field}")
        
        return v


class ClassroomUserOut(BaseModel):
    id: int
    classroom: ClassroomOut
    user: UserMinimalOut

    class Config:
        from_attributes = True
