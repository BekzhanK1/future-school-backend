from datetime import datetime

from fastapi import HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_password,
)
from app.crud.auth_session import auth_session_crud
from app.crud.user import user_crud
from app.schemas import LoginInput, UserOut
from app.schemas.auth_session import AuthSessionOut
from app.schemas.auth import ForgotPasswordInput, ResetPasswordInput
from app.core.security import hash_password
from app.crud.password_reset import password_reset_crud
import secrets


async def login_user(input: LoginInput, request: Request, db: AsyncSession):
    user = await user_crud.get_by_username(db, input.username)
    if not user or not verify_password(input.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    refresh_token = create_refresh_token({"sub": str(user.id)})

    user_agent = request.headers.get("user-agent")
    ip_address = request.client.host

    session = await auth_session_crud.create(
        db,
        user_id=user.id,
        refresh_token=refresh_token,
        user_agent=user_agent,
        ip_address=ip_address,
    )
    if not session:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create session",
        )
    access_token = create_access_token({"sub": str(user.id)}, session_id=session.id)

    return UserOut.from_orm(user), access_token, refresh_token


async def refresh_user_token(refresh_token: str, db: AsyncSession):
    payload = decode_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user_id = int(payload.get("sub"))
    session = await auth_session_crud.get_by_refresh_token(db, refresh_token)

    if not session or not session.is_active:
        raise HTTPException(status_code=401, detail="Session not active")

    if session.expires_at < datetime.utcnow():
        await auth_session_crud.deactivate(db, session)
        raise HTTPException(status_code=401, detail="Session expired")

    # Rotate refresh token
    new_refresh_token = create_refresh_token({"sub": str(user_id)})
    session.refresh_token = new_refresh_token
    await db.commit()

    new_access_token = create_access_token({"sub": str(user_id)}, session_id=session.id)

    user = await user_crud.get_by_id(db, user_id)
    user_out = UserOut.model_validate(user)

    return user_out, new_access_token, new_refresh_token


async def logout_by_refresh_token(db: AsyncSession, refresh_token: str):
    payload = decode_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    session = await auth_session_crud.get_by_refresh_token(db, refresh_token)
    if not session or not session.is_active:
        raise HTTPException(status_code=401, detail="Session already inactive")

    await auth_session_crud.deactivate(db, session)


async def logout_all_sessions(db: AsyncSession, user_id: int):
    sessions = await auth_session_crud.list_by_user(db, user_id)
    for session in sessions:
        await auth_session_crud.deactivate(db, session)
    await db.commit()


async def get_user_sessions(
    db: AsyncSession, user_id: int, session_id
) -> list[AuthSessionOut]:
    sessions = await auth_session_crud.list_by_user(db, user_id)
    return [
        AuthSessionOut(**s.__dict__, is_current=(s.id == session_id)) for s in sessions
    ]


async def deactivate_session(
    db: AsyncSession, session_id: int, user_id: int
) -> AuthSessionOut:
    session = await auth_session_crud.get_by_id(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.user_id != user_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to deactivate this session"
        )

    if not session.is_active:
        raise HTTPException(status_code=400, detail="Session already inactive")

    await auth_session_crud.deactivate(db, session)
    return AuthSessionOut.model_validate(
        {**session.__dict__, "is_current": False}  # or True, depending on your logic
    )


async def request_password_reset(input: ForgotPasswordInput, db: AsyncSession) -> str:
    user = await user_crud.get_by_email(db, input.email)
    if not user:
        # Avoid leaking whether email exists
        return "ok"

    token = secrets.token_urlsafe(48)
    await password_reset_crud.create(db, user_id=user.id, token=token)
    # In production, send email here. For now, return token for testing.
    return token


async def perform_password_reset(input: ResetPasswordInput, db: AsyncSession) -> None:
    prt = await password_reset_crud.get_valid(db, input.token)
    if not prt:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = await user_crud.get_by_id(db, prt.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password = hash_password(input.new_password)
    await db.commit()
    await db.refresh(user)
    await password_reset_crud.mark_used(db, prt)
