from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.auth import require_roles
from app.models.user import User, UserRole
from app.models.lesson import Lesson
from app.schemas.lesson import LessonCreate, LessonOut
from app.services.integrations.live_class import live_class_service
from app.services.storage_service import save_upload


router = APIRouter()


@router.post("/lessons", response_model=LessonOut)
async def create_lesson(
    payload: LessonCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.TEACHER)),
):
    meeting_link = await live_class_service.create_meeting(payload.topic)
    lesson = Lesson(
        course_id=payload.course_id,
        teacher_id=current_user.id,
        starts_at=payload.starts_at,
        ends_at=payload.ends_at,
        topic=payload.topic,
        description=payload.description,
        meeting_link=meeting_link,
    )
    db.add(lesson)
    await db.commit()
    await db.refresh(lesson)
    return LessonOut.model_validate(lesson)


@router.post("/courses/{course_id}/materials")
async def upload_materials(
    course_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(require_roles(UserRole.TEACHER)),
):
    path = await save_upload(file, subdir=f"course_{course_id}")
    return {"detail": "Uploaded", "path": path, "course_id": course_id}




