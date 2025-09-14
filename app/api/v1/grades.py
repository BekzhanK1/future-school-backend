from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.dependencies.auth import get_current_user, require_roles
from app.models.user import User, UserRole
from app.schemas.grade import GradeCreate, GradeOut, GradeUpdate, GradeWithSubmission
from app.services.grading_service import (
    create_grade,
    get_grade_by_id,
    get_grades_by_submission,
    get_grades_by_teacher,
    update_grade,
    delete_grade,
    get_grade_with_submission,
    get_ungraded_submissions,
)

router = APIRouter()


@router.post("/", response_model=GradeOut)
async def create_grade_endpoint(
    grade_in: GradeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.TEACHER)),
):
    """Grade a submission"""
    try:
        grade = await create_grade(grade_in, current_user.id, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return GradeOut.model_validate(grade)


@router.get("/{grade_id}", response_model=GradeOut)
async def get_grade(
    grade_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific grade by ID"""
    grade = await get_grade_by_id(grade_id, db)
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    return GradeOut.model_validate(grade)


@router.get("/{grade_id}/with-submission", response_model=GradeWithSubmission)
async def get_grade_with_submission_endpoint(
    grade_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.TEACHER)),
):
    """Get a grade with its submission details (teacher only)"""
    grade = await get_grade_with_submission(grade_id, db)
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    return GradeWithSubmission.model_validate(grade)


@router.get("/submission/{submission_id}", response_model=GradeOut | None)
async def get_grade_by_submission(
    submission_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get the grade for a specific submission"""
    grade = await get_grades_by_submission(submission_id, db)
    if not grade:
        return None
    return GradeOut.model_validate(grade)


@router.get("/teacher/my-grades", response_model=list[GradeOut])
async def get_my_grades(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.TEACHER)),
):
    """Get all grades given by the current teacher"""
    grades = await get_grades_by_teacher(current_user.id, db)
    return [GradeOut.model_validate(grade) for grade in grades]


@router.get("/teacher/ungraded-submissions", response_model=list[dict])
async def get_ungraded_submissions_endpoint(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.TEACHER)),
):
    """Get all ungraded submissions for assignments created by the current teacher"""
    submissions = await get_ungraded_submissions(current_user.id, db)
    return [
        {
            "submission_id": submission.id,
            "assignment_id": submission.assignment_id,
            "student_id": submission.student_id,
            "submitted_at": submission.submitted_at,
            "assignment_title": submission.assignment.title if submission.assignment else None
        }
        for submission in submissions
    ]


@router.put("/{grade_id}", response_model=GradeOut)
async def update_grade_endpoint(
    grade_id: int,
    grade_update: GradeUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.TEACHER)),
):
    """Update a grade"""
    try:
        grade = await update_grade(grade_id, grade_update, current_user.id, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    return GradeOut.model_validate(grade)


@router.delete("/{grade_id}")
async def delete_grade_endpoint(
    grade_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.TEACHER)),
):
    """Delete a grade"""
    try:
        deleted = await delete_grade(grade_id, current_user.id, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not deleted:
        raise HTTPException(status_code=404, detail="Grade not found")
    return {"detail": "Grade deleted successfully"}
