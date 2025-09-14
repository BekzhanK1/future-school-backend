from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.grade import Grade
from app.models.submission import Submission
from app.models.user import User, UserRole
from app.schemas.grade import GradeCreate, GradeUpdate
from app.crud.grade import grade_crud


async def create_grade(
    grade_in: GradeCreate, 
    teacher_id: int, 
    db: AsyncSession
) -> Grade:
    """
    Create a new grade for a submission.
    
    :param grade_in: GradeCreate schema containing grade details.
    :param teacher_id: ID of the teacher grading.
    :param db: Database session.
    :return: The created Grade object.
    """
    # Verify the submission exists
    submission = await db.get(Submission, grade_in.submission_id)
    if not submission:
        raise ValueError(f"Submission with ID {grade_in.submission_id} does not exist.")
    
    # Verify the teacher exists and has the correct role
    teacher = await db.get(User, teacher_id)
    if not teacher:
        raise ValueError(f"Teacher with ID {teacher_id} does not exist.")
    
    if teacher.role != UserRole.TEACHER:
        raise ValueError(f"User with ID {teacher_id} is not a teacher.")
    
    # Check if submission is already graded
    existing_grade = await grade_crud.get_by_submission(db, grade_in.submission_id)
    if existing_grade:
        raise ValueError("This submission has already been graded.")
    
    # Create grade with teacher_id
    grade_data = grade_in.model_dump()
    grade_data["graded_by"] = teacher_id
    
    return await grade_crud.create(db, GradeCreate(**grade_data))


async def get_grade_by_id(
    grade_id: int, db: AsyncSession
) -> Grade | None:
    """
    Retrieve a grade by its ID.
    
    :param grade_id: The ID of the grade to retrieve.
    :param db: Database session.
    :return: The Grade object if found, otherwise None.
    """
    return await grade_crud.get_by_id(db, grade_id)


async def get_grades_by_submission(
    submission_id: int, db: AsyncSession
) -> Grade | None:
    """
    Retrieve the grade for a specific submission.
    
    :param submission_id: The ID of the submission to filter grades.
    :param db: Database session.
    :return: The Grade object for the specified submission, or None if not graded.
    """
    return await grade_crud.get_by_submission(db, submission_id)


async def get_grades_by_teacher(
    teacher_id: int, db: AsyncSession
) -> list[Grade]:
    """
    Retrieve all grades given by a specific teacher.
    
    :param teacher_id: The ID of the teacher to filter grades.
    :param db: Database session.
    :return: A list of Grade objects for the specified teacher.
    """
    return await grade_crud.list_by_teacher(db, teacher_id)


async def update_grade(
    grade_id: int, 
    grade_update: GradeUpdate, 
    teacher_id: int,
    db: AsyncSession
) -> Grade | None:
    """
    Update a grade by its ID.
    
    :param grade_id: The ID of the grade to update.
    :param grade_update: GradeUpdate schema containing updated details.
    :param teacher_id: ID of the teacher updating the grade.
    :param db: Database session.
    :return: The updated Grade object if successful, otherwise None.
    """
    # Verify the grade exists and belongs to the teacher
    grade = await get_grade_by_id(grade_id, db)
    if not grade:
        return None
    
    if grade.graded_by != teacher_id:
        raise ValueError("You can only update your own grades.")
    
    return await grade_crud.update_by_id(db, grade_id, grade_update)


async def delete_grade(
    grade_id: int, 
    teacher_id: int,
    db: AsyncSession
) -> bool:
    """
    Delete a grade by its ID.
    
    :param grade_id: The ID of the grade to delete.
    :param teacher_id: ID of the teacher deleting the grade.
    :param db: Database session.
    :return: True if deleted successfully, otherwise False.
    """
    # Verify the grade exists and belongs to the teacher
    grade = await get_grade_by_id(grade_id, db)
    if not grade:
        return False
    
    if grade.graded_by != teacher_id:
        raise ValueError("You can only delete your own grades.")
    
    return await grade_crud.delete_by_id(db, grade_id)


async def get_grade_with_submission(
    grade_id: int, db: AsyncSession
) -> Grade | None:
    """
    Retrieve a grade with its submission details.
    
    :param grade_id: The ID of the grade to retrieve.
    :param db: Database session.
    :return: The Grade object with submission if found, otherwise None.
    """
    result = await db.execute(
        select(Grade)
        .options(selectinload(Grade.submission))
        .where(Grade.id == grade_id)
    )
    return result.scalar_one_or_none()


async def get_ungraded_submissions(
    teacher_id: int, db: AsyncSession
) -> list[Submission]:
    """
    Retrieve all ungraded submissions for assignments created by a teacher.
    
    :param teacher_id: The ID of the teacher.
    :param db: Database session.
    :return: A list of ungraded Submission objects.
    """
    return await grade_crud.list_ungraded_submissions_by_teacher(db, teacher_id)
