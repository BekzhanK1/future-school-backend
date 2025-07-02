from pydantic import BaseModel, EmailStr, field_validator
import re


class SchoolCreate(BaseModel):
    name: str
    city: str
    country: str
    contact_email: EmailStr
    contact_phone: str
    logo_url: str | None = None
    kundelik_id: str | None = None

    @field_validator("name", "city", "country", mode="before")
    @classmethod
    def strip_and_non_empty(cls, v: str) -> str:
        if not isinstance(v, str) or not v.strip():
            raise ValueError("Field cannot be empty.")
        return v.strip()

    @field_validator("contact_phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        pattern = r"^\+?[0-9\s\-]{7,15}$"
        if not re.match(pattern, v):
            raise ValueError("Phone must be a valid format (7-15 digits).")
        return v.strip()

    @field_validator("contact_email", mode="before")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()

    class Config:
        from_attributes = True


class SchoolOut(BaseModel):
    id: int
    name: str
    city: str
    country: str
    logo_url: str | None = None
    contact_email: str | None = None
    contact_phone: str | None = None
    kundelik_id: str | None = None

    class Config:
        from_attributes = True


class SchoolUpdate(BaseModel):
    name: str | None = None
    city: str | None = None
    country: str | None = None
    contact_email: EmailStr | None = None
    contact_phone: str | None = None
    logo_url: str | None = None
    kundelik_id: str | None = None

    @field_validator(
        "name", "city", "country", "contact_email", "contact_phone", mode="before"
    )
    @classmethod
    def strip_optional_fields(cls, v: str | None) -> str | None:
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Field cannot be empty.")
        return v

    @field_validator("contact_phone")
    @classmethod
    def validate_optional_phone(cls, v: str | None) -> str | None:
        if v is None:
            return v
        pattern = r"^\+?[0-9\s\-]{7,15}$"
        if not re.match(pattern, v):
            raise ValueError("Phone must be a valid format (7-15 digits).")
        return v.strip()

    class Config:
        from_attributes = True
