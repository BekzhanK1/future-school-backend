from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.dependencies.auth import get_current_user, require_roles
from app.models.user import UserRole
from app.schemas.classroom_course import (
    ClassroomCourseCreate,
    ClassroomCourseUpdate,
    ClassroomCourseOut,
)
from app.services.classroom_course_service import (
    create_classroom_course,
    get_classroom_course_by_id,
    list_all_classroom_courses,
    update_classroom_course_by_id,
    delete_classroom_course_by_id,
)

router = APIRouter()


@router.post("/", response_model=ClassroomCourseOut)
async def create(
    obj_in: ClassroomCourseCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_roles(UserRole.SUPERADMIN, UserRole.SCHOOLADMIN)),
):
    classroom_course = await create_classroom_course(obj_in, db)
    return ClassroomCourseOut.model_validate(classroom_course)


@router.get("/", response_model=list[ClassroomCourseOut])
async def list_all(
    db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)
):
    records = await list_all_classroom_courses(db)
    return [ClassroomCourseOut.model_validate(obj) for obj in records]


@router.get("/{obj_id}", response_model=ClassroomCourseOut)
async def get_by_id(
    obj_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    record = await get_classroom_course_by_id(obj_id, db)
    if not record:
        raise HTTPException(status_code=404, detail="ClassroomCourse not found")
    return ClassroomCourseOut.model_validate(record)


@router.put("/{obj_id}", response_model=ClassroomCourseOut)
async def update(
    obj_id: int,
    obj_in: ClassroomCourseUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_roles(UserRole.SUPERADMIN, UserRole.SCHOOLADMIN)),
):
    updated = await update_classroom_course_by_id(obj_id, obj_in, db)
    if not updated:
        raise HTTPException(status_code=404, detail="ClassroomCourse not found")
    return ClassroomCourseOut.model_validate(updated)


@router.delete("/{obj_id}", response_model=dict)
async def delete(
    obj_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_roles(UserRole.SUPERADMIN, UserRole.SCHOOLADMIN)),
):
    deleted = await delete_classroom_course_by_id(obj_id, db)
    if not deleted:
        raise HTTPException(status_code=404, detail="ClassroomCourse not found")
    return {"detail": "ClassroomCourse deleted successfully."}
