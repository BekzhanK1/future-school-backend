from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.submission import Submission
from app.models.assignment import Assignment
from app.models.user import User, UserRole
from app.schemas.submission import SubmissionCreate, SubmissionUpdate
from app.crud.submission import submission_crud


async def create_submission(
    submission_in: SubmissionCreate, 
    student_id: int, 
    db: AsyncSession
) -> Submission:
    """
    Create a new submission.
    
    :param submission_in: SubmissionCreate schema containing submission details.
    :param student_id: ID of the student submitting.
    :param db: Database session.
    :return: The created Submission object.
    """
    # Verify the assignment exists
    assignment = await db.get(Assignment, submission_in.assignment_id)
    if not assignment:
        raise ValueError(f"Assignment with ID {submission_in.assignment_id} does not exist.")
    
    # Verify the student exists and has the correct role
    student = await db.get(User, student_id)
    if not student:
        raise ValueError(f"Student with ID {student_id} does not exist.")
    
    if student.role != UserRole.STUDENT:
        raise ValueError(f"User with ID {student_id} is not a student.")
    
    # Check if student already submitted for this assignment
    existing_submission = await submission_crud.get_by_assignment_and_student(
        db, submission_in.assignment_id, student_id
    )
    if existing_submission:
        raise ValueError("You have already submitted this assignment.")
    
    # Create submission with student_id
    submission_data = submission_in.model_dump()
    submission_data["student_id"] = student_id
    
    return await submission_crud.create(db, SubmissionCreate(**submission_data))


async def get_submission_by_id(
    submission_id: int, db: AsyncSession
) -> Submission | None:
    """
    Retrieve a submission by its ID.
    
    :param submission_id: The ID of the submission to retrieve.
    :param db: Database session.
    :return: The Submission object if found, otherwise None.
    """
    return await submission_crud.get_by_id(db, submission_id)


async def get_submissions_by_assignment(
    assignment_id: int, db: AsyncSession
) -> list[Submission]:
    """
    Retrieve all submissions for a specific assignment.
    
    :param assignment_id: The ID of the assignment to filter submissions.
    :param db: Database session.
    :return: A list of Submission objects for the specified assignment.
    """
    return await submission_crud.list_by_assignment(db, assignment_id)


async def get_submissions_by_student(
    student_id: int, db: AsyncSession
) -> list[Submission]:
    """
    Retrieve all submissions by a specific student.
    
    :param student_id: The ID of the student to filter submissions.
    :param db: Database session.
    :return: A list of Submission objects for the specified student.
    """
    return await submission_crud.list_by_student(db, student_id)


async def update_submission(
    submission_id: int, 
    submission_update: SubmissionUpdate, 
    student_id: int,
    db: AsyncSession
) -> Submission | None:
    """
    Update a submission by its ID.
    
    :param submission_id: The ID of the submission to update.
    :param submission_update: SubmissionUpdate schema containing updated details.
    :param student_id: ID of the student updating the submission.
    :param db: Database session.
    :return: The updated Submission object if successful, otherwise None.
    """
    # Verify the submission exists and belongs to the student
    submission = await get_submission_by_id(submission_id, db)
    if not submission:
        return None
    
    if submission.student_id != student_id:
        raise ValueError("You can only update your own submissions.")
    
    return await submission_crud.update_by_id(db, submission_id, submission_update)


async def delete_submission(
    submission_id: int, 
    student_id: int,
    db: AsyncSession
) -> bool:
    """
    Delete a submission by its ID.
    
    :param submission_id: The ID of the submission to delete.
    :param student_id: ID of the student deleting the submission.
    :param db: Database session.
    :return: True if deleted successfully, otherwise False.
    """
    # Verify the submission exists and belongs to the student
    submission = await get_submission_by_id(submission_id, db)
    if not submission:
        return False
    
    if submission.student_id != student_id:
        raise ValueError("You can only delete your own submissions.")
    
    return await submission_crud.delete_by_id(db, submission_id)


async def get_submission_with_grade(
    submission_id: int, db: AsyncSession
) -> Submission | None:
    """
    Retrieve a submission with its grade.
    
    :param submission_id: The ID of the submission to retrieve.
    :param db: Database session.
    :return: The Submission object with grade if found, otherwise None.
    """
    result = await db.execute(
        select(Submission)
        .options(selectinload(Submission.grade))
        .where(Submission.id == submission_id)
    )
    return result.scalar_one_or_none()
