from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.dependencies.auth import get_current_user, require_roles
from app.models.user import User, UserRole
from app.models.classroom import Classroom
from app.schemas.classroom import ClassroomCreate, ClassroomOut, ClassroomUpdate, BulkClassroomCreate
from app.services.classroom_service import (
    create_classroom,
    create_bulk_classrooms,
    get_classroom_by_id,
    get_classroom_by_kundelik_id,
    list_all_for_school,
    update_classroom_by_id,
)

router = APIRouter()


@router.post("/", response_model=ClassroomOut)
async def create(
    classroom_in: ClassroomCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SUPERADMIN)),
):
    """
    Create a new classroom.
    """
    return ClassroomOut.model_validate(await create_classroom(classroom_in, db))


@router.post("/bulk", response_model=list[ClassroomOut])
async def create_bulk(
    bulk_create: BulkClassroomCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SUPERADMIN)),
):
    """
    Create multiple classrooms for a school in bulk (e.g., 1A, 2B, etc. for grades 1-12).
    """
    classrooms = await create_bulk_classrooms(bulk_create, db)
    return [ClassroomOut.model_validate(classroom) for classroom in classrooms]


@router.get("/", response_model=list[ClassroomOut])
async def list_classrooms_for_school(
    school_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SUPERADMIN)),
):
    """
    List all classrooms for a specific school.
    """
    classrooms = await list_all_for_school(school_id, db)
    return [ClassroomOut.model_validate(classroom) for classroom in classrooms]


@router.get("/{classroom_id}", response_model=ClassroomOut)
async def get_by_id(
    classroom_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SUPERADMIN)),
):
    """
    Retrieve a classroom by its ID.
    """
    classroom = await get_classroom_by_id(classroom_id, db)
    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")
    return ClassroomOut.model_validate(classroom)


@router.get("/kundelik/{kundelik_id}", response_model=ClassroomOut)
async def get_by_kundelik_id(
    kundelik_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SUPERADMIN)),
):
    """
    Retrieve a classroom by its Kundelik ID.
    """
    classroom = await get_classroom_by_kundelik_id(kundelik_id, db)
    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")
    return ClassroomOut.model_validate(classroom)


@router.put("/{classroom_id}", response_model=ClassroomOut)
async def update_classroom(
    classroom_id: int,
    classroom_update: ClassroomUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SUPERADMIN)),
):
    """
    Update a classroom by its ID.
    """
    updated_classroom = await update_classroom_by_id(classroom_id, classroom_update, db)
    if not updated_classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")
    return ClassroomOut.model_validate(updated_classroom)


@router.delete("/{classroom_id}", response_model=dict)
async def delete_classroom(
    classroom_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SUPERADMIN)),
):
    """
    Delete a classroom by its ID.
    """
    classroom = await get_classroom_by_id(classroom_id, db)
    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")

    await db.delete(classroom)
    await db.commit()

    return {"detail": "Classroom deleted successfully."}
