from pydantic import BaseModel


class LoginInput(BaseModel):
    username: str
    password: str


class RefreshTokenInput(BaseModel):
    refresh_token: str


class ForgotPasswordInput(BaseModel):
    email: str


class ResetPasswordInput(BaseModel):
    token: str
    new_password: str
