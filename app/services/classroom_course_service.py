from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.classroom_course import classroom_course_crud
from app.schemas.classroom_course import ClassroomCourseCreate, ClassroomCourseUpdate


async def create_classroom_course(obj_in: ClassroomCourseCreate, db: AsyncSession):
    """
    Create new classroom-course association.

    :param obj_in: Data to create.
    :param db: Database session.
    :return: Created object.
    """
    return await classroom_course_crud.create(db, obj_in)


async def get_classroom_course_by_id(obj_id: int, db: AsyncSession):
    """
    Get classroom-course association by ID.

    :param obj_id: ID of association.
    :param db: Database session.
    :return: Object or None.
    """
    return await classroom_course_crud.get_by_id(db, obj_id)


async def list_all_classroom_courses(db: AsyncSession):
    """
    List all classroom-course associations.

    :param db: Database session.
    :return: List of objects.
    """
    return await classroom_course_crud.list_all(db)


async def update_classroom_course_by_id(
    obj_id: int, obj_in: ClassroomCourseUpdate, db: AsyncSession
):
    """
    Update classroom-course association by ID.

    :param obj_id: ID to update.
    :param obj_in: Update data.
    :param db: Database session.
    :return: Updated object or None.
    """
    return await classroom_course_crud.update_by_id(db, obj_id, obj_in)


async def delete_classroom_course_by_id(obj_id: int, db: AsyncSession):
    """
    Delete classroom-course association by ID.

    :param obj_id: ID to delete.
    :param db: Database session.
    :return: True if deleted, False otherwise.
    """
    return await classroom_course_crud.delete_by_id(db, obj_id)
