from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.dependencies.auth import get_current_user, require_roles
from app.models.user import UserRole
from app.schemas.teacher_course import (
    TeacherCourseCreate,
    TeacherCourseUpdate,
    TeacherCourseOut,
)
from app.services.teacher_course_service import (
    create_teacher_course,
    get_teacher_course_by_id,
    list_all_teacher_courses,
    update_teacher_course_by_id,
    delete_teacher_course_by_id,
)

router = APIRouter()


@router.post("/", response_model=TeacherCourseOut)
async def create(
    obj_in: TeacherCourseCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_roles(UserRole.SUPERADMIN, UserRole.SCHOOLADMIN)),
):
    teacher_course = await create_teacher_course(obj_in, db)
    return TeacherCourseOut.model_validate(teacher_course)


@router.get("/", response_model=list[TeacherCourseOut])
async def list_all(
    db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)
):
    records = await list_all_teacher_courses(db)
    return [TeacherCourseOut.model_validate(obj) for obj in records]


@router.get("/{obj_id}", response_model=TeacherCourseOut)
async def get_by_id(
    obj_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    record = await get_teacher_course_by_id(obj_id, db)
    if not record:
        raise HTTPException(status_code=404, detail="TeacherCourse not found")
    return TeacherCourseOut.model_validate(record)


@router.put("/{obj_id}", response_model=TeacherCourseOut)
async def update(
    obj_id: int,
    obj_in: TeacherCourseUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_roles(UserRole.SUPERADMIN, UserRole.SCHOOLADMIN)),
):
    updated = await update_teacher_course_by_id(obj_id, obj_in, db)
    if not updated:
        raise HTTPException(status_code=404, detail="TeacherCourse not found")
    return TeacherCourseOut.model_validate(updated)


@router.delete("/{obj_id}", response_model=dict)
async def delete(
    obj_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_roles(UserRole.SUPERADMIN, UserRole.SCHOOLADMIN)),
):
    deleted = await delete_teacher_course_by_id(obj_id, db)
    if not deleted:
        raise HTTPException(status_code=404, detail="TeacherCourse not found")
    return {"detail": "TeacherCourse deleted successfully."}
