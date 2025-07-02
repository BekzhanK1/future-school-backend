from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.auth import get_current_session, get_current_user
from app.models.user import User
from app.schemas import LoginInput, RefreshTokenInput, UserOut
from app.schemas.auth_session import AuthSessionOut
from app.services.auth_service import (
    get_user_sessions,
    login_user,
    logout_all_sessions,
    logout_by_refresh_token,
    refresh_user_token,
    deactivate_session,
)

from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

router = APIRouter()


@router.get("/sessions", response_model=list[AuthSessionOut])
async def list_sessions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_session: AuthSessionOut = Depends(get_current_session),
):
    return await get_user_sessions(db, current_user.id, current_session.id)


@router.get("/me", response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_user)):
    """
    Get the current authenticated user.
    """
    return current_user


@router.post("/login")
@limiter.limit("5/minute")
async def login(
    input: LoginInput, request: Request, db: AsyncSession = Depends(get_db)
):
    user_out, access_token, refresh_token = await login_user(input, request, db)
    return respond_with_tokens(user_out, access_token, refresh_token)


@router.post("/refresh")
async def refresh_token(
    request: Request,
    data: RefreshTokenInput = None,
    db: AsyncSession = Depends(get_db),
):
    refresh_token = data.refresh_token if data else request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    user_out, new_access_token, new_refresh_token = await refresh_user_token(
        refresh_token, db
    )
    return respond_with_tokens(user_out, new_access_token, new_refresh_token)


@router.post("/logout")
async def logout(
    data: RefreshTokenInput,
    db: AsyncSession = Depends(get_db),
):
    await logout_by_refresh_token(db, data.refresh_token)

    response = JSONResponse(content={"detail": "Logged out successfully."})
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response


@router.post("/logout-cookie")
async def logout_cookie(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    await logout_by_refresh_token(db, refresh_token)

    response = JSONResponse(content={"detail": "Logged out successfully."})
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response


@router.post("/logout-all")
async def logout_all(
    db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
):
    await logout_all_sessions(db, current_user.id)

    response = JSONResponse(content={"detail": "All sessions logged out successfully."})
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response


@router.post("/logout-all-cookie")
async def logout_all_cookie(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await logout_all_sessions(db, current_user.id)

    response = JSONResponse(content={"detail": "All sessions logged out successfully."})
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response


@router.post("/terminate-session/{session_id}")
async def terminate_session(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Terminate a specific user session by ID.
    """
    return await deactivate_session(db, session_id, current_user.id)


def respond_with_tokens(user: UserOut, access_token: str, refresh_token: str):
    response = JSONResponse(
        content={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": user.dict(),
        }
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=900,  # 15 minutes
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=604800,  # 7 days
    )

    return response
