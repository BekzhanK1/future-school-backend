from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.dependencies.auth import get_current_user, require_roles
from app.models.user import User, UserRole
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseOut, CourseUpdate, BulkCourseCreate
from app.services.course_service import (
    create_course,
    create_bulk_courses,
    get_course_by_id,
    get_course_by_course_code,
    list_all_courses,
    search_courses,
    update_course_by_id,
    delete_course_by_id,
)

router = APIRouter()


@router.post("/", response_model=CourseOut)
async def create(
    course_in: CourseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.SUPERADMIN, UserRole.SCHOOLADMIN)
    ),
):
    """
    Create a new course.
    """
    return CourseOut.model_validate(await create_course(course_in, db))


@router.post("/bulk", response_model=list[CourseOut])
async def create_bulk(
    bulk_create: BulkCourseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.SUPERADMIN, UserRole.SCHOOLADMIN)
    ),
):
    """
    Create multiple courses in bulk (e.g., Math for grade 1, Kazakh language for grade 5, etc.).
    """
    courses = await create_bulk_courses(bulk_create, db)
    return [CourseOut.model_validate(course) for course in courses]


@router.get("/all", response_model=list[CourseOut])
async def list_all(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.SUPERADMIN, UserRole.SCHOOLADMIN)
    ),
):
    """
    List all courses in the system.
    """
    courses = await list_all_courses(db)
    return [CourseOut.model_validate(course) for course in courses]


@router.get("/search/", response_model=list[CourseOut])
async def search_courses_api(
    query: str | None = None,
    grade: int | None = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Flexible search endpoint for courses.
    """
    courses = await search_courses(db, query, grade)
    return [CourseOut.model_validate(c) for c in courses]


@router.get("/{course_id}", response_model=CourseOut)
async def get_by_id(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve a course by its ID.
    """
    course = await get_course_by_id(course_id, db)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return CourseOut.model_validate(course)


@router.get("/code/{course_code}", response_model=CourseOut)
async def get_by_course_code(
    course_code: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.SUPERADMIN, UserRole.SCHOOLADMIN)
    ),
):
    """
    Retrieve a course by its course code.
    """
    course = await get_course_by_course_code(course_code, db)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return CourseOut.model_validate(course)


@router.put("/{course_id}", response_model=CourseOut)
async def update_course(
    course_id: int,
    course_update: CourseUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.SUPERADMIN, UserRole.SCHOOLADMIN)
    ),
):
    """
    Update a course by its ID.
    """
    updated_course = await update_course_by_id(course_id, course_update, db)
    if not updated_course:
        raise HTTPException(status_code=404, detail="Course not found")
    return CourseOut.model_validate(updated_course)


@router.delete("/{course_id}", response_model=dict)
async def delete_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.SUPERADMIN, UserRole.SCHOOLADMIN)
    ),
):
    """
    Delete a course by its ID.
    """
    deleted = await delete_course_by_id(course_id, db)
    if not deleted:
        raise HTTPException(status_code=404, detail="Course not found")

    return {"detail": "Course deleted successfully."}
