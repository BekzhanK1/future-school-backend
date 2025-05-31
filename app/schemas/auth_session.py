from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AuthSessionBase(BaseModel):
    user_agent: Optional[str]
    ip_address: Optional[str]


class AuthSessionOut(AuthSessionBase):
    id: int
    is_active: bool
    created_at: datetime
    expires_at: datetime

    class Config:
        orm_mode = True


class RefreshTokenInput(BaseModel):
    refresh_token: str
