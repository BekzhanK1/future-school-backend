from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.teacher_course import teacher_course_crud
from app.schemas.teacher_course import TeacherCourseCreate, TeacherCourseUpdate


async def create_teacher_course(obj_in: TeacherCourseCreate, db: AsyncSession):
    """
    Create a new teacher-course association.

    :param obj_in: Data to create.
    :param db: Database session.
    :return: Created object.
    """
    return await teacher_course_crud.create(db, obj_in)


async def get_teacher_course_by_id(obj_id: int, db: AsyncSession):
    """
    Get teacher-course association by ID.

    :param obj_id: ID to get.
    :param db: Database session.
    :return: Object or None.
    """
    return await teacher_course_crud.get_by_id(db, obj_id)


async def list_all_teacher_courses(db: AsyncSession):
    """
    List all teacher-course associations.

    :param db: Database session.
    :return: List of objects.
    """
    return await teacher_course_crud.list_all(db)


async def update_teacher_course_by_id(
    obj_id: int, obj_in: TeacherCourseUpdate, db: AsyncSession
):
    """
    Update teacher-course association by ID.

    :param obj_id: ID to update.
    :param obj_in: Update data.
    :param db: Database session.
    :return: Updated object or None.
    """
    return await teacher_course_crud.update_by_id(db, obj_id, obj_in)


async def delete_teacher_course_by_id(obj_id: int, db: AsyncSession):
    """
    Delete teacher-course association by ID.

    :param obj_id: ID to delete.
    :param db: Database session.
    :return: True if deleted, False otherwise.
    """
    return await teacher_course_crud.delete_by_id(db, obj_id)
