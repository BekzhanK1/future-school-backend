from pydantic import BaseModel, field_validator
from typing import Optional, List


class CourseSectionCreate(BaseModel):
    course_id: int
    title: str
    position: int | None = 0

    @field_validator("title")
    def validate_title(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Section title cannot be empty.")
        return v.strip()

    @field_validator("position")
    def validate_position(cls, v: int | None) -> int:
        if v is not None and v < 0:
            raise ValueError("Position must be non-negative.")
        return v or 0


class CourseSectionUpdate(BaseModel):
    title: str | None = None
    position: int | None = None

    @field_validator("title")
    def validate_title(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError("Section title cannot be empty.")
        return v.strip() if v else v

    @field_validator("position")
    def validate_position(cls, v: int | None) -> int | None:
        if v is not None and v < 0:
            raise ValueError("Position must be non-negative.")
        return v


class CourseSectionOut(BaseModel):
    id: int
    course_id: int
    title: str
    position: int
    resources: List[dict] = []

    class Config:
        from_attributes = True

    @classmethod
    def model_validate(cls, obj, **kwargs):
        # Создаем словарь из объекта, исключая resources
        data = {
            "id": obj.id,
            "course_id": obj.course_id,
            "title": obj.title,
            "position": obj.position,
            "resources": []
        }
        return cls(**data)


class CourseSectionWithResources(CourseSectionOut):
    resources: List[dict] = []

    class Config:
        from_attributes = True



