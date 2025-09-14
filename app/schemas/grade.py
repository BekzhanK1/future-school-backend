from datetime import datetime
from pydantic import BaseModel, field_validator
from typing import Optional


class GradeCreate(BaseModel):
    submission_id: int
    grade_value: int
    feedback: str | None = None

    @field_validator("grade_value")
    def validate_grade_value(cls, v: int) -> int:
        if not (0 <= v <= 100):
            raise ValueError("Grade value must be between 0 and 100.")
        return v

    @field_validator("feedback")
    def validate_feedback(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            return None
        return v.strip() if v else v


class GradeUpdate(BaseModel):
    grade_value: Optional[int] = None
    feedback: Optional[str] = None

    @field_validator("grade_value")
    def validate_grade_value(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and not (0 <= v <= 100):
            raise ValueError("Grade value must be between 0 and 100.")
        return v

    @field_validator("feedback")
    def validate_feedback(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            return None
        return v.strip() if v else v


class GradeOut(BaseModel):
    id: int
    submission_id: int
    graded_by: int
    grade_value: int
    feedback: str | None = None
    graded_at: datetime

    class Config:
        from_attributes = True


class GradeWithSubmission(GradeOut):
    submission: dict

    class Config:
        from_attributes = True


