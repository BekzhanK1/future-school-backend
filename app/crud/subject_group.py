from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.subject_group import SubjectGroup
from app.schemas.subject_group import SubjectGroupCreate


class CRUDSubjectGroup:
    async def create(self, db: AsyncSession, obj_in: SubjectGroupCreate) -> SubjectGroup:
        obj = SubjectGroup(**obj_in.model_dump())
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        # Eager load relations
        result = await db.execute(
            select(SubjectGroup)
            .options(
                selectinload(SubjectGroup.course),
                selectinload(SubjectGroup.classroom),
                selectinload(SubjectGroup.teacher),
            )
            .where(SubjectGroup.id == obj.id)
        )
        return result.scalars().first()

    async def get_by_id(self, db: AsyncSession, obj_id: int) -> SubjectGroup | None:
        return await db.get(SubjectGroup, obj_id)

    async def list_by_classroom(self, db: AsyncSession, classroom_id: int) -> list[SubjectGroup]:
        result = await db.execute(
            select(SubjectGroup)
            .options(
                selectinload(SubjectGroup.course),
                selectinload(SubjectGroup.classroom),
                selectinload(SubjectGroup.teacher),
            )
            .where(SubjectGroup.classroom_id == classroom_id)
        )
        return result.scalars().all()

    async def list_by_teacher(self, db: AsyncSession, teacher_id: int) -> list[SubjectGroup]:
        result = await db.execute(
            select(SubjectGroup)
            .options(
                selectinload(SubjectGroup.course),
                selectinload(SubjectGroup.classroom),
                selectinload(SubjectGroup.teacher),
            )
            .where(SubjectGroup.teacher_id == teacher_id)
        )
        return result.scalars().all()

    async def list_by_teacher_and_course(self, db: AsyncSession, teacher_id: int, course_id: int) -> list[SubjectGroup]:
        result = await db.execute(
            select(SubjectGroup)
            .options(
                selectinload(SubjectGroup.course),
                selectinload(SubjectGroup.classroom),
                selectinload(SubjectGroup.teacher),
            )
            .where(
                SubjectGroup.teacher_id == teacher_id,
                SubjectGroup.course_id == course_id
            )
        )
        return result.scalars().all()

    async def delete_by_id(self, db: AsyncSession, obj_id: int) -> bool:
        obj = await self.get_by_id(db, obj_id)
        if not obj:
            return False
        await db.delete(obj)
        await db.commit()
        return True


subject_group_crud = CRUDSubjectGroup()
