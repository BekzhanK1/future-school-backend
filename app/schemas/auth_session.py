from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AuthSessionOut(BaseModel):
    id: int
    user_agent: Optional[str]
    ip_address: Optional[str]
    is_active: bool
    is_current: bool
    created_at: datetime
    expires_at: datetime

    class Config:
        from_attributes = True
