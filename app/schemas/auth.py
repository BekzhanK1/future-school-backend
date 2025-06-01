from pydantic import BaseModel


class LoginInput(BaseModel):
    username: str
    password: str


class RefreshTokenInput(BaseModel):
    refresh_token: str
