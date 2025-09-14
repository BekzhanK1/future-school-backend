from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.dependencies.auth import get_current_user, require_roles, require_course_teacher_or_admin
from app.models.user import User, UserRole
from app.schemas.course_section import (
    CourseSectionCreate, 
    CourseSectionOut, 
    CourseSectionUpdate, 
    CourseSectionWithResources
)
from app.services.course_section_service import (
    create_course_section,
    get_course_section_by_id,
    get_course_sections_by_course,
    get_course_section_with_resources,
    update_course_section,
    delete_course_section,
    reorder_course_sections,
)

router = APIRouter()


@router.post("/", response_model=CourseSectionOut)
async def create_course_section_endpoint(
    section_in: CourseSectionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new course section"""
    # Check permissions
    if current_user.role not in [UserRole.SUPERADMIN, UserRole.SCHOOLADMIN]:
        if current_user.role == UserRole.TEACHER:
            from app.crud.subject_group import subject_group_crud
            subject_groups = await subject_group_crud.list_by_teacher_and_course(db, current_user.id, section_in.course_id)
            if not subject_groups:
                raise HTTPException(status_code=403, detail="You don't have permission to manage this course")
        else:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    try:
        section = await create_course_section(section_in, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return CourseSectionOut.model_validate(section)


@router.get("/{section_id}", response_model=CourseSectionOut)
async def get_course_section(
    section_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific course section by ID"""
    section = await get_course_section_by_id(section_id, db)
    if not section:
        raise HTTPException(status_code=404, detail="Course section not found")
    return CourseSectionOut.model_validate(section)


@router.get("/{section_id}/with-resources", response_model=CourseSectionWithResources)
async def get_course_section_with_resources_endpoint(
    section_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a course section with all its resources"""
    section = await get_course_section_with_resources(section_id, db)
    if not section:
        raise HTTPException(status_code=404, detail="Course section not found")
    return CourseSectionWithResources.model_validate(section)


@router.get("/course/{course_id}", response_model=list[CourseSectionOut])
async def get_course_sections_by_course_endpoint(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all sections for a specific course"""
    sections = await get_course_sections_by_course(course_id, db)
    return [CourseSectionOut.model_validate(section) for section in sections]


@router.put("/{section_id}", response_model=CourseSectionOut)
async def update_course_section_endpoint(
    section_id: int,
    section_update: CourseSectionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.TEACHER)),
):
    """Update a course section"""
    try:
        section = await update_course_section(section_id, section_update, current_user.id, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not section:
        raise HTTPException(status_code=404, detail="Course section not found")
    return CourseSectionOut.model_validate(section)


@router.delete("/{section_id}")
async def delete_course_section_endpoint(
    section_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.TEACHER)),
):
    """Delete a course section"""
    try:
        deleted = await delete_course_section(section_id, current_user.id, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not deleted:
        raise HTTPException(status_code=404, detail="Course section not found")
    return {"detail": "Course section deleted successfully"}


@router.put("/course/{course_id}/reorder")
async def reorder_course_sections_endpoint(
    course_id: int,
    section_orders: dict[int, int],
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.TEACHER)),
):
    """Reorder sections within a course"""
    try:
        sections = await reorder_course_sections(course_id, section_orders, current_user.id, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return [CourseSectionOut.model_validate(section) for section in sections]
