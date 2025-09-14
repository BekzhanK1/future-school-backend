from datetime import datetime
from pydantic import BaseModel, field_validator
from typing import Optional


class SubmissionCreate(BaseModel):
    assignment_id: int
    text: str | None = None
    file_url: str | None = None

    @field_validator("text", "file_url")
    def validate_content(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            return None
        return v.strip() if v else v

    def model_post_init(self, __context) -> None:
        if not self.text and not self.file_url:
            raise ValueError("Either text or file_url must be provided.")


class SubmissionUpdate(BaseModel):
    text: Optional[str] = None
    file_url: Optional[str] = None

    @field_validator("text", "file_url")
    def validate_content(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            return None
        return v.strip() if v else v

    def model_post_init(self, __context) -> None:
        if not self.text and not self.file_url:
            raise ValueError("Either text or file_url must be provided.")


class SubmissionOut(BaseModel):
    id: int
    assignment_id: int
    student_id: int
    submitted_at: datetime
    text: str | None = None
    file_url: str | None = None
    grade: Optional[dict] = None

    class Config:
        from_attributes = True


class SubmissionWithGrade(SubmissionOut):
    grade: Optional[dict] = None

    class Config:
        from_attributes = True


