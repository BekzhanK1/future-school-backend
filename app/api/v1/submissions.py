from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.dependencies.auth import get_current_user, require_roles
from app.models.user import User, UserRole
from app.schemas.submission import SubmissionCreate, SubmissionOut, SubmissionUpdate, SubmissionWithGrade
from app.services.submission_service import (
    create_submission,
    get_submission_by_id,
    get_submissions_by_assignment,
    get_submissions_by_student,
    update_submission,
    delete_submission,
    get_submission_with_grade,
)
from app.services.storage_service import save_upload

router = APIRouter()


@router.post("/", response_model=SubmissionOut)
async def create_submission_endpoint(
    submission_data: SubmissionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.STUDENT)),
):
    """Submit an assignment (text or file)"""
    print(f"🔍 DEBUG: current_user.id = {current_user.id}")
    print(f"🔍 DEBUG: submission_data = {submission_data}")
    try:
        submission = await create_submission(submission_data, current_user.id, db)
    except Exception as e:
        print(f"🔍 DEBUG: Error in create_submission: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    return SubmissionOut.model_validate(submission)


@router.get("/{submission_id}", response_model=SubmissionOut)
async def get_submission(
    submission_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific submission by ID"""
    submission = await get_submission_by_id(submission_id, db)
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    return SubmissionOut.model_validate(submission)


@router.get("/{submission_id}/with-grade", response_model=SubmissionWithGrade)
async def get_submission_with_grade_endpoint(
    submission_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a submission with its grade"""
    submission = await get_submission_with_grade(submission_id, db)
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    return SubmissionWithGrade.model_validate(submission)


@router.get("/assignment/{assignment_id}", response_model=list[SubmissionOut])
async def get_submissions_by_assignment_endpoint(
    assignment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.TEACHER)),
):
    """Get all submissions for a specific assignment (teacher only)"""
    submissions = await get_submissions_by_assignment(assignment_id, db)
    return [SubmissionOut.model_validate(submission) for submission in submissions]


@router.get("/student/my-submissions", response_model=list[SubmissionOut])
async def get_my_submissions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.STUDENT)),
):
    """Get all submissions by the current student"""
    submissions = await get_submissions_by_student(current_user.id, db)
    return [SubmissionOut.model_validate(submission) for submission in submissions]


@router.put("/{submission_id}", response_model=SubmissionOut)
async def update_submission_endpoint(
    submission_id: int,
    submission_update: SubmissionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.STUDENT)),
):
    """Update a submission"""
    try:
        submission = await update_submission(submission_id, submission_update, current_user.id, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    return SubmissionOut.model_validate(submission)


@router.delete("/{submission_id}")
async def delete_submission_endpoint(
    submission_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.STUDENT)),
):
    """Delete a submission"""
    try:
        deleted = await delete_submission(submission_id, current_user.id, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not deleted:
        raise HTTPException(status_code=404, detail="Submission not found")
    return {"detail": "Submission deleted successfully"}
