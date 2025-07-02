from pydantic import BaseModel, field_validator
import re


class ClassroomCreate(BaseModel):
    grade: int
    letter: str
    language: str
    school_id: int

    @field_validator("grade")
    def validate_grade(cls, value: int) -> int:
        if not (0 <= value <= 12):
            raise ValueError("Grade must be between 0 and 12.")
        return value

    @field_validator("letter")
    def validate_letter(cls, v):
        allowed_pattern = r"^[A-ZА-ЯӘІҢҒҮҰҚӨҺ]{1,2}$"
        if not re.match(allowed_pattern, v.upper()):
            raise ValueError(
                "Letter must be 1–2 chars from A-Z or Cyrillic (incl. Kazakh)"
            )
        return v.upper()

    @field_validator("language")
    def validate_language(cls, v: str) -> str:
        allowed_languages = ["kz", "ru", "en"]
        if v not in allowed_languages:
            raise ValueError(f"Language must be one of {allowed_languages}.")
        return v.lower()


class ClassroomOut(BaseModel):
    id: int
    grade: int
    letter: str
    language: str
    kundelik_id: str | None = None
    school_id: int

    class Config:
        from_attributes = True


class ClassroomUpdate(BaseModel):
    grade: int | None = None
    letter: str | None = None
