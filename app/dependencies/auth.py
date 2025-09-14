from datetime import datetime
from typing import Literal

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token
from app.crud.auth_session import auth_session_crud
from app.crud.user import user_crud
from app.crud.subject_group import subject_group_crud
from app.db.session import get_db
from app.models.user import User, UserRole


def extract_token(request: Request) -> str:
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header.split(" ")[1]

    token = request.cookies.get("access_token")
    if token:
        return token

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing access token",
    )


def validate_token_payload(token: str) -> dict:
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        )

    if "sub" not in payload or "sid" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    return payload


async def get_current_user(
    request: Request, db: AsyncSession = Depends(get_db)
) -> User:
    token = extract_token(request)
    payload = validate_token_payload(token)

    user_id = int(payload["sub"])
    session_id = int(payload["sid"])

    user = await user_crud.get_by_id(db, user_id)
    session = await auth_session_crud.get_by_id(db, session_id)

    if (
        not user
        or not session
        or not session.is_active
        or session.expires_at < datetime.utcnow()
    ):
        raise HTTPException(status_code=401, detail="Session invalid or expired")

    return user


async def get_current_session(request: Request, db: AsyncSession = Depends(get_db)):
    token = extract_token(request)
    payload = validate_token_payload(token)

    session_id = int(payload["sid"])
    session = await auth_session_crud.get_by_id(db, session_id)

    if not session or not session.is_active or session.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Session invalid or expired")

    return session


def require_roles(*roles: UserRole, logic: Literal["or", "and"] = "or"):
    async def role_checker(user: User = Depends(get_current_user)):
        user_roles = {user.role}

        if logic == "or":
            if not any(role in user_roles for role in roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions (OR check failed)",
                )

        elif logic == "and":
            if not all(role in user_roles for role in roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions (AND check failed)",
                )

        return user

    return role_checker


async def require_course_teacher_or_admin(
    course_id: int, 
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Check if user is a teacher assigned to the course or admin/superadmin.
    """
    # Superadmin and schooladmin can always access
    if user.role in [UserRole.SUPERADMIN, UserRole.SCHOOLADMIN]:
        return user
    
    # For teachers, check if they are assigned to this course
    if user.role == UserRole.TEACHER:
        subject_groups = await subject_group_crud.list_by_teacher_and_course(db, user.id, course_id)
        if subject_groups:
            return user
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You don't have permission to manage this course"
    )
