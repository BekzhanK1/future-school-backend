from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.classroom_user import classroom_user_crud
from app.crud.user import user_crud
from app.schemas.classroom_user import ClassroomUserCreate


async def add_user_to_classroom(obj_in: ClassroomUserCreate, db: AsyncSession):
    """
    Add a user to a classroom.
    :param obj_in: ClassroomUserCreate schema containing user and classroom details.
    :param db: Database session.
    :return: The created ClassroomUser object.
    """
    if not obj_in.classroom_id or not obj_in.user_id:
        raise ValueError("Both classroom_id and user_id must be provided.")

    user = user_crud.get_by_id(db, obj_in.user_id)
    if not user:
        raise ValueError(f"User with ID {obj_in.user_id} does not exist.")

    return await classroom_user_crud.create(db, obj_in)


async def get_users_for_classroom(classroom_id: int, db: AsyncSession):
    """
    Retrieve all users associated with a specific classroom.
    :param classroom_id: The ID of the classroom to retrieve users for.
    :param db: Database session.
    :return: A list of ClassroomUser objects associated with the classroom.
    """
    return await classroom_user_crud.list_by_classroom(db, classroom_id)


async def get_classrooms_for_user(user_id: int, db: AsyncSession):
    """
    Retrieve all classrooms associated with a specific user.
    :param user_id: The ID of the user to retrieve classrooms for.
    :param db: Database session.
    :return: A list of ClassroomUser objects associated with the user.
    """
    return await classroom_user_crud.list_by_user(db, user_id)


async def remove_user_from_classroom(classroom_id: int, user_id: int, db: AsyncSession):
    """
    Remove a user from a classroom.
    :param classroom_id: The ID of the classroom from which to remove the user.
    :param user_id: The ID of the user to remove.
    :param db: Database session.
    :return: The ClassroomUser object that was deleted.
    """
    return await classroom_user_crud.delete(db, classroom_id, user_id)
