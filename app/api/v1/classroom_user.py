from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.auth import get_current_user, require_roles
from app.models.user import User, UserRole
from app.schemas.classroom_user import ClassroomUserCreate, ClassroomUserOut, BulkStudentEnrollment, BulkStudentCreate
from app.services.classroom_user_service import (
    add_user_to_classroom,
    bulk_enroll_students,
    bulk_create_students_in_classroom,
    get_users_for_classroom,
    get_classrooms_for_user,
    remove_user_from_classroom,
)
from app.db.session import get_db

router = APIRouter()


@router.post("/", response_model=ClassroomUserOut)
async def assign_user_to_classroom(
    body: ClassroomUserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SUPERADMIN)),
):
    try:
        res = await add_user_to_classroom(body, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return ClassroomUserOut.model_validate(res)


@router.post("/bulk-enroll", response_model=list[ClassroomUserOut])
async def bulk_enroll_students_in_classroom(
    body: BulkStudentEnrollment,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SUPERADMIN)),
):
    """
    Enroll multiple students in a classroom at once.
    """
    try:
        res = await bulk_enroll_students(body, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return [ClassroomUserOut.model_validate(item) for item in res]


@router.post("/bulk-create-students", response_model=list[ClassroomUserOut])
async def bulk_create_students_in_classroom_endpoint(
    body: BulkStudentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SUPERADMIN, UserRole.SCHOOLADMIN)),
):
    """
    Create multiple students and enroll them in a classroom with default password (qwerty123).
    """
    try:
        res = await bulk_create_students_in_classroom(body, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return [ClassroomUserOut.model_validate(item) for item in res]


@router.get("/by_classroom/{classroom_id}", response_model=list[ClassroomUserOut])
async def list_users_by_classroom(
    classroom_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SUPERADMIN)),
):
    try:
        res = await get_users_for_classroom(classroom_id, db)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    return res


@router.get("/by_user/{user_id}", response_model=list[ClassroomUserOut])
async def list_classrooms_by_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SUPERADMIN)),
):
    try:
        res = await get_classrooms_for_user(user_id, db)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    return res


@router.delete("/", response_model=dict)
async def remove_user_classroom_relation(
    classroom_id: int,
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SUPERADMIN)),
):
    success = await remove_user_from_classroom(classroom_id, user_id, db)
    if not success:
        raise HTTPException(status_code=404, detail="Relation not found")
    return {"detail": "User removed from classroom"}
