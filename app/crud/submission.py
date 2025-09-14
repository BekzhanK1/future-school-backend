from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.submission import Submission
from app.schemas.submission import SubmissionCreate, SubmissionUpdate


class SubmissionCRUD:
    async def create(self, db: AsyncSession, obj_in: SubmissionCreate) -> Submission:
        submission = Submission(**obj_in.model_dump())
        db.add(submission)
        await db.commit()
        await db.refresh(submission)
        return submission

    async def get_by_id(self, db: AsyncSession, submission_id: int) -> Submission | None:
        result = await db.execute(select(Submission).where(Submission.id == submission_id))
        return result.scalar_one_or_none()

    async def get_by_assignment_and_student(
        self, db: AsyncSession, assignment_id: int, student_id: int
    ) -> Submission | None:
        result = await db.execute(
            select(Submission).where(
                Submission.assignment_id == assignment_id,
                Submission.student_id == student_id
            )
        )
        return result.scalar_one_or_none()

    async def list_by_assignment(self, db: AsyncSession, assignment_id: int) -> list[Submission]:
        result = await db.execute(
            select(Submission)
            .where(Submission.assignment_id == assignment_id)
            .order_by(Submission.submitted_at)
        )
        return result.scalars().all()

    async def list_by_student(self, db: AsyncSession, student_id: int) -> list[Submission]:
        result = await db.execute(
            select(Submission)
            .where(Submission.student_id == student_id)
            .order_by(Submission.submitted_at.desc())
        )
        return result.scalars().all()

    async def update_by_id(
        self, db: AsyncSession, submission_id: int, obj_in: SubmissionUpdate
    ) -> Submission | None:
        submission = await self.get_by_id(db, submission_id)
        if not submission:
            return None
        
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(submission, field, value)
        
        await db.commit()
        await db.refresh(submission)
        return submission

    async def delete_by_id(self, db: AsyncSession, submission_id: int) -> bool:
        submission = await self.get_by_id(db, submission_id)
        if not submission:
            return False
        
        await db.delete(submission)
        await db.commit()
        return True


submission_crud = SubmissionCRUD()
