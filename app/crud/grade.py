from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.grade import Grade
from app.models.submission import Submission
from app.schemas.grade import GradeCreate, GradeUpdate


class GradeCRUD:
    async def create(self, db: AsyncSession, obj_in: GradeCreate) -> Grade:
        grade = Grade(**obj_in.model_dump())
        db.add(grade)
        await db.commit()
        await db.refresh(grade)
        return grade

    async def get_by_id(self, db: AsyncSession, grade_id: int) -> Grade | None:
        result = await db.execute(select(Grade).where(Grade.id == grade_id))
        return result.scalar_one_or_none()

    async def get_by_submission(self, db: AsyncSession, submission_id: int) -> Grade | None:
        result = await db.execute(
            select(Grade).where(Grade.submission_id == submission_id)
        )
        return result.scalar_one_or_none()

    async def list_by_teacher(self, db: AsyncSession, teacher_id: int) -> list[Grade]:
        result = await db.execute(
            select(Grade)
            .where(Grade.graded_by == teacher_id)
            .order_by(Grade.graded_at.desc())
        )
        return result.scalars().all()

    async def list_ungraded_submissions_by_teacher(
        self, db: AsyncSession, teacher_id: int
    ) -> list[Submission]:
        # Get all submissions for assignments created by the teacher that don't have grades
        result = await db.execute(
            select(Submission)
            .join(Submission.assignment)
            .outerjoin(Grade, Grade.submission_id == Submission.id)
            .where(
                Submission.assignment.has(teacher_id=teacher_id),
                Grade.id.is_(None)
            )
            .order_by(Submission.submitted_at.desc())
        )
        return result.scalars().all()

    async def update_by_id(
        self, db: AsyncSession, grade_id: int, obj_in: GradeUpdate
    ) -> Grade | None:
        grade = await self.get_by_id(db, grade_id)
        if not grade:
            return None
        
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(grade, field, value)
        
        await db.commit()
        await db.refresh(grade)
        return grade

    async def delete_by_id(self, db: AsyncSession, grade_id: int) -> bool:
        grade = await self.get_by_id(db, grade_id)
        if not grade:
            return False
        
        await db.delete(grade)
        await db.commit()
        return True


grade_crud = GradeCRUD()
