from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.assignment import Assignment
from app.schemas.assignment import AssignmentCreate, AssignmentUpdate


class AssignmentCRUD:
    async def create(self, db: AsyncSession, obj_in: AssignmentCreate, teacher_id: int) -> Assignment:
        assignment_data = obj_in.model_dump()
        assignment_data['teacher_id'] = teacher_id
        assignment = Assignment(**assignment_data)
        db.add(assignment)
        await db.commit()
        await db.refresh(assignment)
        return assignment

    async def get_by_id(self, db: AsyncSession, assignment_id: int) -> Assignment | None:
        result = await db.execute(select(Assignment).where(Assignment.id == assignment_id))
        return result.scalar_one_or_none()

    async def list_by_course(self, db: AsyncSession, course_id: int) -> list[Assignment]:
        result = await db.execute(
            select(Assignment)
            .where(Assignment.course_id == course_id)
            .order_by(Assignment.due_at)
        )
        return result.scalars().all()

    async def list_by_teacher(self, db: AsyncSession, teacher_id: int) -> list[Assignment]:
        result = await db.execute(
            select(Assignment)
            .where(Assignment.teacher_id == teacher_id)
            .order_by(Assignment.due_at)
        )
        return result.scalars().all()

    async def update_by_id(
        self, db: AsyncSession, assignment_id: int, obj_in: AssignmentUpdate
    ) -> Assignment | None:
        assignment = await self.get_by_id(db, assignment_id)
        if not assignment:
            return None
        
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(assignment, field, value)
        
        await db.commit()
        await db.refresh(assignment)
        return assignment

    async def delete_by_id(self, db: AsyncSession, assignment_id: int) -> bool:
        assignment = await self.get_by_id(db, assignment_id)
        if not assignment:
            return False
        
        await db.delete(assignment)
        await db.commit()
        return True


assignment_crud = AssignmentCRUD()
