from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.course_section import CourseSection
from app.schemas.course_section import CourseSectionCreate, CourseSectionUpdate


class CRUDCourseSection:
    async def create(self, db: AsyncSession, obj_in: CourseSectionCreate) -> CourseSection:
        obj = CourseSection(**obj_in.model_dump())
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def get_by_id(self, db: AsyncSession, obj_id: int) -> CourseSection | None:
        return await db.get(CourseSection, obj_id)

    async def list_by_course(self, db: AsyncSession, course_id: int) -> list[CourseSection]:
        result = await db.execute(
            select(CourseSection).where(CourseSection.course_id == course_id).order_by(CourseSection.position)
        )
        return result.scalars().all()

    async def update_by_id(
        self, db: AsyncSession, obj_id: int, obj_in: CourseSectionUpdate
    ) -> CourseSection | None:
        obj = await self.get_by_id(db, obj_id)
        if not obj:
            return None
        data = obj_in.model_dump(exclude_unset=True)
        for k, v in data.items():
            setattr(obj, k, v)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def delete_by_id(self, db: AsyncSession, obj_id: int) -> bool:
        obj = await self.get_by_id(db, obj_id)
        if not obj:
            return False
        await db.delete(obj)
        await db.commit()
        return True


course_section_crud = CRUDCourseSection()



