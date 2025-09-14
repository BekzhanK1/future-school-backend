from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.dependencies.auth import get_current_user, require_roles
from app.models.user import User, UserRole
from app.schemas.assignment import AssignmentCreate, AssignmentOut, AssignmentUpdate, AssignmentWithSubmissions
from app.services.assignment_service import (
    create_assignment,
    get_assignment_by_id,
    get_assignments_by_course,
    get_assignments_by_teacher,
    update_assignment,
    delete_assignment,
    get_assignment_with_submissions,
)

router = APIRouter()


@router.post("/", response_model=AssignmentOut)
async def create_assignment_endpoint(
    assignment_in: AssignmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.TEACHER)),
):
    """Create a new assignment"""
    try:
        assignment = await create_assignment(assignment_in, current_user.id, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return AssignmentOut.model_validate(assignment)


@router.get("/{assignment_id}", response_model=AssignmentOut)
async def get_assignment(
    assignment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific assignment by ID"""
    assignment = await get_assignment_by_id(assignment_id, db)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return AssignmentOut.model_validate(assignment)


@router.get("/{assignment_id}/with-submissions", response_model=AssignmentWithSubmissions)
async def get_assignment_with_submissions_endpoint(
    assignment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.TEACHER)),
):
    """Get an assignment with all its submissions (teacher only)"""
    assignment = await get_assignment_with_submissions(assignment_id, db)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return AssignmentWithSubmissions.model_validate(assignment)


@router.get("/course/{course_id}", response_model=list[AssignmentOut])
async def get_assignments_by_course_endpoint(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all assignments for a specific course"""
    assignments = await get_assignments_by_course(course_id, db)
    return [AssignmentOut.model_validate(assignment) for assignment in assignments]


@router.get("/teacher/my-assignments", response_model=list[AssignmentOut])
async def get_my_assignments(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.TEACHER)),
):
    """Get all assignments created by the current teacher"""
    assignments = await get_assignments_by_teacher(current_user.id, db)
    return [AssignmentOut.model_validate(assignment) for assignment in assignments]


@router.put("/{assignment_id}", response_model=AssignmentOut)
async def update_assignment_endpoint(
    assignment_id: int,
    assignment_update: AssignmentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.TEACHER)),
):
    """Update an assignment"""
    try:
        assignment = await update_assignment(assignment_id, assignment_update, current_user.id, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return AssignmentOut.model_validate(assignment)


@router.delete("/{assignment_id}")
async def delete_assignment_endpoint(
    assignment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.TEACHER)),
):
    """Delete an assignment"""
    try:
        deleted = await delete_assignment(assignment_id, current_user.id, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not deleted:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return {"detail": "Assignment deleted successfully"}
