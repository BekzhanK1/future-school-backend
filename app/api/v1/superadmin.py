from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.db.session import get_db
from app.dependencies.auth import require_roles
from app.models.user import User, UserRole
from app.models.user import User as UserModel
from app.models.school import School
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.assignment import Assignment
from app.models.submission import Submission
from app.models.grade import Grade
from app.schemas.school import SchoolCreate, SchoolOut
from app.services.school_service import create_school, list_all_schools
from app.core.security import create_access_token, create_refresh_token
from app.crud.auth_session import auth_session_crud
from app.crud.user import user_crud


router = APIRouter()


@router.get("/institutions", response_model=list[SchoolOut])
async def institutions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SUPERADMIN)),
):
    schools = await list_all_schools(db)
    return [SchoolOut.model_validate(s) for s in schools]


@router.post("/institutions", response_model=SchoolOut)
async def add_institution(
    payload: SchoolCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SUPERADMIN)),
):
    school = await create_school(payload, db)
    return SchoolOut.model_validate(school)


@router.get("/metrics")
async def metrics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SUPERADMIN)),
):
    async def count(model):
        result = await db.execute(select(func.count()).select_from(model))
        return int(result.scalar() or 0)

    return {
        "users": await count(UserModel),
        "schools": await count(School),
        "courses": await count(Course),
        "lessons": await count(Lesson),
        "assignments": await count(Assignment),
        "submissions": await count(Submission),
        "grades": await count(Grade),
    }


@router.post("/impersonate/{user_id}")
async def impersonate(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SUPERADMIN)),
):
    user = await user_crud.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    refresh_token = create_refresh_token({"sub": str(user.id)})
    session = await auth_session_crud.create(
        db,
        user_id=user.id,
        refresh_token=refresh_token,
        user_agent=f"impersonated_by={current_user.id}",
        ip_address="127.0.0.1",
    )
    access_token = create_access_token({"sub": str(user.id)}, session_id=session.id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {"id": user.id, "username": user.username, "role": user.role.value},
    }



