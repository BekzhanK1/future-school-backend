from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.classroom_user import ClassroomUser
from app.models.subject_group import SubjectGroup
from app.models.course import Course


async def get_student_courses(db: AsyncSession, student_id: int) -> list[Course]:
    stmt = (
        select(Course)
        .join(SubjectGroup, SubjectGroup.course_id == Course.id)
        .join(ClassroomUser, ClassroomUser.classroom_id == SubjectGroup.classroom_id)
        .where(ClassroomUser.user_id == student_id)
        .distinct()
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())



