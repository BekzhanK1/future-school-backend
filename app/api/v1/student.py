from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.auth import require_roles
from app.models.user import User, UserRole
from app.schemas.course import CourseOut
from app.services.student_service import get_student_courses
from app.services.storage_service import save_upload
from app.models.submission import Submission
from app.crud.course_section import course_section_crud
from app.crud.resource import resource_crud
from app.schemas.course_section import CourseSectionOut
from app.schemas.resource import ResourceOut


router = APIRouter()


@router.get("/dashboard")
async def dashboard(current_user: User = Depends(require_roles(UserRole.STUDENT))):
    # TODO: aggregate schedule, calendar, pending assignments when models exist
    return {"message": "Student dashboard coming soon"}


@router.get("/courses", response_model=list[CourseOut])
async def list_my_courses(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.STUDENT)),
):
    courses = await get_student_courses(db, current_user.id)
    return [CourseOut.model_validate(c) for c in courses]


@router.get("/courses/{course_id}", response_model=CourseOut)
async def course_detail(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.STUDENT)),
):
    # For now just reuse course service when details are simple
    from app.services.course_service import get_course_by_id

    course = await get_course_by_id(course_id, db)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    # TODO: include lessons, assignments, recordings when models exist
    return CourseOut.model_validate(course)




@router.get("/courses/{course_id}/sections", response_model=list[CourseSectionOut])
async def get_course_sections(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.STUDENT)),
):
    sections = await course_section_crud.list_by_course(db, course_id)
    return [CourseSectionOut.model_validate(s) for s in sections]


@router.get("/sections/{section_id}/resources", response_model=list[ResourceOut])
async def get_section_resources(
    section_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.STUDENT)),
):
    items = await resource_crud.list_by_section(db, section_id)
    return [ResourceOut.model_validate(i) for i in items]


