from fastapi import APIRouter, HTTPException, Depends, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.user import UserOut
from app.schemas.auth_session import AuthSessionOut, RefreshTokenInput
from app.core.security import verify_password, create_access_token, create_refresh_token
from app.crud.user import user_crud
from app.crud.auth_session import auth_session_crud
from app.core.security import decode_token
from datetime import datetime

router = APIRouter()


@router.post("/login")
async def login(request: Request, db: AsyncSession = Depends(get_db)):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")

    user = await user_crud.get_by_username(db, username)
    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    user_agent = request.headers.get("user-agent")
    ip_address = request.client.host

    await auth_session_crud.create(
        db,
        user_id=user.id,
        refresh_token=refresh_token,
        user_agent=user_agent,
        ip_address=ip_address,
    )

    return respond_with_tokens(UserOut.from_orm(user), access_token, refresh_token)


@router.post("/refresh")
async def refresh_token(
    data: RefreshTokenInput,
    db: AsyncSession = Depends(get_db),
):
    payload = decode_token(data.refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user_id = int(payload.get("sub"))
    session = await auth_session_crud.get_by_refresh_token(db, data.refresh_token)

    if not session or not session.is_active:
        raise HTTPException(status_code=401, detail="Session not active")

    if session.expires_at < datetime.utcnow():
        await auth_session_crud.deactivate(db, session)
        raise HTTPException(status_code=401, detail="Session expired")

    # rotate refresh token
    new_refresh_token = create_refresh_token({"sub": str(user_id)})
    session.refresh_token = new_refresh_token
    await db.commit()

    new_access_token = create_access_token({"sub": str(user_id)})

    user = await user_crud.get_by_id(db, user_id)
    user_out = UserOut.from_orm(user)
    return respond_with_tokens(user_out, new_access_token, new_refresh_token)


def respond_with_tokens(user, access_token: str, refresh_token: str):
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
