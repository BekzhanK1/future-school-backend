from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.dependencies.auth import get_current_user, require_roles
from app.models.user import User, UserRole

from app.models.school import School
from app.schemas.school import SchoolCreate, SchoolOut, SchoolUpdate
from app.services.school_service import (
    create_school,
    get_school_by_id,
    list_all_schools,
    list_filtered_schools,
    get_school_by_kundelik_id,
    update_school_by_id,
    delete_school_by_id,
)


router = APIRouter()


@router.get("/search", response_model=list[SchoolOut])
async def search(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SUPERADMIN)),
    filters: dict[str, str] = {},
):
    """
    Search for schools based on filtering criteria.
    """
    schools = await list_filtered_schools(db, filters)
    return [SchoolOut.model_validate(school) for school in schools]


@router.post("/", response_model=SchoolOut)
async def create(
    school_in: SchoolCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SUPERADMIN)),
):
    """
    Create a new school.
    """
    return SchoolOut.model_validate(await create_school(school_in, db))


@router.get("/", response_model=list[SchoolOut])
async def list_all(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SUPERADMIN)),
):
    """
    List all schools.
    """
    return [SchoolOut.model_validate(school) for school in await list_all_schools(db)]


@router.get("/{school_id}", response_model=SchoolOut)
async def get_by_id(
    school_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SUPERADMIN)),
):
    """
    Get a school by its ID.
    """
    school = await get_school_by_id(school_id, db)
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    return SchoolOut.model_validate(school)


@router.get("/kundelik/{kundelik_id}", response_model=SchoolOut)
async def get_by_kundelik_id(
    kundelik_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SUPERADMIN)),
):
    """
    Get a school by its Kundelik ID.
    """
    school = await get_school_by_kundelik_id(kundelik_id, db)
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    return SchoolOut.model_validate(school)


@router.put("/{school_id}", response_model=SchoolOut)
async def update_school(
    school_id: int,
    school_in: SchoolUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SUPERADMIN)),
):
    """
    Update an existing school.
    """
    school = await update_school_by_id(school_id, school_in, db)
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    return SchoolOut.model_validate(school)


@router.delete("/{school_id}", response_model=None)
async def delete_school(
    school_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SUPERADMIN)),
):
    """
    Delete a school by its ID.
    """
    success = await delete_school_by_id(school_id, db)
    if not success:
        raise HTTPException(status_code=404, detail="School not found")
    return {"detail": "School deleted successfully"}
