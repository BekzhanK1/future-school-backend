from pydantic import BaseModel, field_validator
from typing import Optional
from app.models.resource import ResourceType


class ResourceCreate(BaseModel):
    course_section_id: int
    type: str  # Принимаем строку, конвертируем в enum
    title: str
    description: str | None = None
    url: str | None = None
    position: int | None = 0

    @field_validator("type")
    def validate_type(cls, v: str) -> str:
        if v not in ["file", "link"]:
            raise ValueError("Type must be 'file' or 'link'.")
        return v

    @field_validator("title")
    def validate_title(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Resource title cannot be empty.")
        return v.strip()

    @field_validator("url")
    def validate_url(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            return None
        return v.strip() if v else v

    @field_validator("position")
    def validate_position(cls, v: int | None) -> int:
        if v is not None and v < 0:
            raise ValueError("Position must be non-negative.")
        return v or 0

    def model_post_init(self, __context) -> None:
        if self.type == ResourceType.FILE and not self.url:
            raise ValueError("File resources must have a URL.")
        if self.type == ResourceType.LINK and not self.url:
            raise ValueError("Link resources must have a URL.")


class ResourceUpdate(BaseModel):
    type: ResourceType | None = None
    title: str | None = None
    description: str | None = None
    url: str | None = None
    position: int | None = None

    @field_validator("title")
    def validate_title(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError("Resource title cannot be empty.")
        return v.strip() if v else v

    @field_validator("url")
    def validate_url(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            return None
        return v.strip() if v else v

    @field_validator("position")
    def validate_position(cls, v: int | None) -> int | None:
        if v is not None and v < 0:
            raise ValueError("Position must be non-negative.")
        return v


class ResourceOut(BaseModel):
    id: int
    course_section_id: int
    type: ResourceType
    title: str
    description: str | None = None
    url: str | None = None
    position: int

    class Config:
        from_attributes = True



