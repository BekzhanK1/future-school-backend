from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.assignment import Assignment
from app.models.course import Course
from app.models.user import User, UserRole
from app.schemas.assignment import AssignmentCreate, AssignmentUpdate
from app.crud.assignment import assignment_crud


async def create_assignment(
    assignment_in: AssignmentCreate, 
    teacher_id: int, 
    db: AsyncSession
) -> Assignment:
    """
    Create a new assignment.
    
    :param assignment_in: AssignmentCreate schema containing assignment details.
    :param teacher_id: ID of the teacher creating the assignment.
    :param db: Database session.
    :return: The created Assignment object.
    """
    # Verify the course exists
    course = await db.get(Course, assignment_in.course_id)
    if not course:
        raise ValueError(f"Course with ID {assignment_in.course_id} does not exist.")
    
    # Verify the teacher exists and has the correct role
    teacher = await db.get(User, teacher_id)
    if not teacher:
        raise ValueError(f"Teacher with ID {teacher_id} does not exist.")
    
    if teacher.role != UserRole.TEACHER:
        raise ValueError(f"User with ID {teacher_id} is not a teacher.")
    
    return await assignment_crud.create(db, assignment_in, teacher_id)


async def get_assignment_by_id(
    assignment_id: int, db: AsyncSession
) -> Assignment | None:
    """
    Retrieve an assignment by its ID.
    
    :param assignment_id: The ID of the assignment to retrieve.
    :param db: Database session.
    :return: The Assignment object if found, otherwise None.
    """
    return await assignment_crud.get_by_id(db, assignment_id)


async def get_assignments_by_course(
    course_id: int, db: AsyncSession
) -> list[Assignment]:
    """
    Retrieve all assignments for a specific course.
    
    :param course_id: The ID of the course to filter assignments.
    :param db: Database session.
    :return: A list of Assignment objects for the specified course.
    """
    return await assignment_crud.list_by_course(db, course_id)


async def get_assignments_by_teacher(
    teacher_id: int, db: AsyncSession
) -> list[Assignment]:
    """
    Retrieve all assignments created by a specific teacher.
    
    :param teacher_id: The ID of the teacher to filter assignments.
    :param db: Database session.
    :return: A list of Assignment objects for the specified teacher.
    """
    return await assignment_crud.list_by_teacher(db, teacher_id)


async def update_assignment(
    assignment_id: int, 
    assignment_update: AssignmentUpdate, 
    teacher_id: int,
    db: AsyncSession
) -> Assignment | None:
    """
    Update an assignment by its ID.
    
    :param assignment_id: The ID of the assignment to update.
    :param assignment_update: AssignmentUpdate schema containing updated details.
    :param teacher_id: ID of the teacher updating the assignment.
    :param db: Database session.
    :return: The updated Assignment object if successful, otherwise None.
    """
    # Verify the assignment exists and belongs to the teacher
    assignment = await get_assignment_by_id(assignment_id, db)
    if not assignment:
        return None
    
    if assignment.teacher_id != teacher_id:
        raise ValueError("You can only update your own assignments.")
    
    return await assignment_crud.update_by_id(db, assignment_id, assignment_update)


async def delete_assignment(
    assignment_id: int, 
    teacher_id: int,
    db: AsyncSession
) -> bool:
    """
    Delete an assignment by its ID.
    
    :param assignment_id: The ID of the assignment to delete.
    :param teacher_id: ID of the teacher deleting the assignment.
    :param db: Database session.
    :return: True if deleted successfully, otherwise False.
    """
    # Verify the assignment exists and belongs to the teacher
    assignment = await get_assignment_by_id(assignment_id, db)
    if not assignment:
        return False
    
    if assignment.teacher_id != teacher_id:
        raise ValueError("You can only delete your own assignments.")
    
    return await assignment_crud.delete_by_id(db, assignment_id)


async def get_assignment_with_submissions(
    assignment_id: int, db: AsyncSession
) -> Assignment | None:
    """
    Retrieve an assignment with its submissions.
    
    :param assignment_id: The ID of the assignment to retrieve.
    :param db: Database session.
    :return: The Assignment object with submissions if found, otherwise None.
    """
    result = await db.execute(
        select(Assignment)
        .options(selectinload(Assignment.submissions))
        .where(Assignment.id == assignment_id)
    )
    return result.scalar_one_or_none()
