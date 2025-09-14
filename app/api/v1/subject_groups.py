from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.auth import require_roles
from app.models.user import User, UserRole
from app.schemas.subject_group import SubjectGroupCreate, SubjectGroupOut, BulkSubjectGroupCreate, SubjectGroupUpdate
from app.services.subject_group_service import (
    create_subject_group,
    create_bulk_subject_groups,
    get_subject_group_by_id,
    list_subject_groups_by_classroom,
    list_subject_groups_by_teacher,
    update_subject_group,
    delete_subject_group,
)


router = APIRouter()


@router.post("/", response_model=SubjectGroupOut)
async def create_subject_group_endpoint(
    payload: SubjectGroupCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SUPERADMIN, UserRole.SCHOOLADMIN)),
):
    """Create a subject group: assign a course to a classroom with a teacher"""
    try:
        group = await create_subject_group(payload, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return SubjectGroupOut.model_validate(group)


@router.post("/bulk", response_model=list[SubjectGroupOut])
async def create_bulk_subject_groups_endpoint(
    payload: BulkSubjectGroupCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SUPERADMIN, UserRole.SCHOOLADMIN)),
):
    """Create multiple subject groups in bulk: assign courses to classrooms with teachers"""
    try:
        groups = await create_bulk_subject_groups(payload, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return [SubjectGroupOut.model_validate(group) for group in groups]


@router.get("/classroom/{classroom_id}", response_model=list[SubjectGroupOut])
async def list_classroom_subjects(
    classroom_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SUPERADMIN, UserRole.SCHOOLADMIN, UserRole.TEACHER)),
):
    """List all subjects for a classroom"""
    groups = await list_subject_groups_by_classroom(classroom_id, db)
    return [SubjectGroupOut.model_validate(g) for g in groups]


@router.get("/teacher/{teacher_id}", response_model=list[SubjectGroupOut])
async def list_teacher_subjects(
    teacher_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SUPERADMIN, UserRole.SCHOOLADMIN)),
):
    """List all subjects taught by a teacher"""
    groups = await list_subject_groups_by_teacher(teacher_id, db)
    return [SubjectGroupOut.model_validate(g) for g in groups]


@router.get("/{group_id}", response_model=SubjectGroupOut)
async def get_subject_group(
    group_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SUPERADMIN, UserRole.SCHOOLADMIN, UserRole.TEACHER)),
):
    """Get a specific subject group by ID"""
    group = await get_subject_group_by_id(group_id, db)
    if not group:
        raise HTTPException(status_code=404, detail="Subject group not found")
    return SubjectGroupOut.model_validate(group)


@router.put("/{group_id}", response_model=SubjectGroupOut)
async def update_subject_group_endpoint(
    group_id: int,
    payload: SubjectGroupUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SUPERADMIN, UserRole.SCHOOLADMIN)),
):
    """Update a subject group (e.g., change teacher assignment)"""
    try:
        group = await update_subject_group(group_id, payload, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not group:
        raise HTTPException(status_code=404, detail="Subject group not found")
    return SubjectGroupOut.model_validate(group)


@router.delete("/{group_id}")
async def delete_subject_group_endpoint(
    group_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SUPERADMIN, UserRole.SCHOOLADMIN)),
):
    """Delete a subject group"""
    if not await delete_subject_group(group_id, db):
        raise HTTPException(status_code=404, detail="Subject group not found")
    return {"detail": "Subject group deleted"}
