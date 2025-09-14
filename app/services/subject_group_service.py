from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.subject_group import subject_group_crud
from app.models.subject_group import SubjectGroup
from app.schemas.subject_group import SubjectGroupCreate, SubjectGroupUpdate, BulkSubjectGroupCreate
from app.models.user import UserRole
from app.crud.user import user_crud


async def create_subject_group(
    subject_group_in: SubjectGroupCreate, db: AsyncSession
) -> SubjectGroup:
    """
    Create a new subject group (course-classroom-teacher assignment).
    
    :param subject_group_in: SubjectGroupCreate schema containing assignment details.
    :param db: Database session.
    :return: The created SubjectGroup object.
    """
    # Verify the teacher exists and has the correct role
    teacher = await user_crud.get_by_id(db, subject_group_in.teacher_id)
    if not teacher:
        raise ValueError(f"Teacher with ID {subject_group_in.teacher_id} does not exist.")
    
    if teacher.role != UserRole.TEACHER:
        raise ValueError(f"User with ID {subject_group_in.teacher_id} is not a teacher.")
    
    return await subject_group_crud.create(db, subject_group_in)


async def get_subject_group_by_id(
    subject_group_id: int, db: AsyncSession
) -> SubjectGroup | None:
    """
    Retrieve a subject group by its ID.
    
    :param subject_group_id: The ID of the subject group to retrieve.
    :param db: Database session.
    :return: The SubjectGroup object if found, otherwise None.
    """
    return await subject_group_crud.get_by_id(db, subject_group_id)


async def list_subject_groups_by_classroom(
    classroom_id: int, db: AsyncSession
) -> list[SubjectGroup]:
    """
    Retrieve all subject groups for a specific classroom.
    
    :param classroom_id: The ID of the classroom to filter subject groups.
    :param db: Database session.
    :return: A list of SubjectGroup objects for the specified classroom.
    """
    return await subject_group_crud.list_by_classroom(db, classroom_id)


async def list_subject_groups_by_teacher(
    teacher_id: int, db: AsyncSession
) -> list[SubjectGroup]:
    """
    Retrieve all subject groups for a specific teacher.
    
    :param teacher_id: The ID of the teacher to filter subject groups.
    :param db: Database session.
    :return: A list of SubjectGroup objects for the specified teacher.
    """
    return await subject_group_crud.list_by_teacher(db, teacher_id)


async def update_subject_group(
    subject_group_id: int, 
    subject_group_update: SubjectGroupUpdate, 
    db: AsyncSession
) -> SubjectGroup | None:
    """
    Update a subject group by its ID.
    
    :param subject_group_id: The ID of the subject group to update.
    :param subject_group_update: SubjectGroupUpdate schema containing updated details.
    :param db: Database session.
    :return: The updated SubjectGroup object if successful, otherwise None.
    """
    if subject_group_update.teacher_id:
        # Verify the new teacher exists and has the correct role
        teacher = await user_crud.get_by_id(db, subject_group_update.teacher_id)
        if not teacher:
            raise ValueError(f"Teacher with ID {subject_group_update.teacher_id} does not exist.")
        
        if teacher.role != UserRole.TEACHER:
            raise ValueError(f"User with ID {subject_group_update.teacher_id} is not a teacher.")
    
    return await subject_group_crud.update_by_id(db, subject_group_id, subject_group_update)


async def delete_subject_group(
    subject_group_id: int, db: AsyncSession
) -> bool:
    """
    Delete a subject group by its ID.
    
    :param subject_group_id: The ID of the subject group to delete.
    :param db: Database session.
    :return: True if deleted successfully, otherwise False.
    """
    return await subject_group_crud.delete_by_id(db, subject_group_id)


async def create_bulk_subject_groups(
    bulk_create: BulkSubjectGroupCreate, db: AsyncSession
) -> list[SubjectGroup]:
    """
    Create multiple subject groups in bulk.
    
    :param bulk_create: BulkSubjectGroupCreate schema containing assignments to create.
    :param db: Database session.
    :return: List of created SubjectGroup objects.
    """
    subject_groups = []
    
    for assignment in bulk_create.assignments:
        try:
            subject_group = await create_subject_group(assignment, db)
            subject_groups.append(subject_group)
        except Exception as e:
            # If assignment already exists, skip it
            if "uq_course_classroom" in str(e):
                continue
            raise e
    
    return subject_groups
