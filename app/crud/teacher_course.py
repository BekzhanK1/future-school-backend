from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.teacher_course import TeacherCourse
from app.schemas.teacher_course import TeacherCourseCreate, TeacherCourseUpdate


class CRUDTeacherCourse:
    async def create(
        self, db: AsyncSession, obj_in: TeacherCourseCreate
    ) -> TeacherCourse:
        """
        Create a new TeacherCourse.

        :param db: Database session.
        :param obj_in: Data to create.
        :return: Created object.
        """
        obj = TeacherCourse(**obj_in.model_dump())
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def get_by_id(self, db: AsyncSession, obj_id: int) -> TeacherCourse | None:
        """
        Get TeacherCourse by ID.

        :param db: Database session.
        :param obj_id: ID to get.
        :return: Object or None.
        """
        return await db.get(TeacherCourse, obj_id)

    async def list_all(self, db: AsyncSession) -> list[TeacherCourse]:
        """
        List all TeacherCourses.

        :param db: Database session.
        :return: List of objects.
        """
        result = await db.execute(select(TeacherCourse))
        return result.scalars().all()

    async def update_by_id(
        self, db: AsyncSession, obj_id: int, obj_in: TeacherCourseUpdate
    ) -> TeacherCourse | None:
        """
        Update TeacherCourse by ID.

        :param db: Database session.
        :param obj_id: ID to update.
        :param obj_in: Update data.
        :return: Updated object or None.
        """
        obj = await self.get_by_id(db, obj_id)
        if not obj:
            return None
        update_data = obj_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(obj, key, value)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def delete_by_id(self, db: AsyncSession, obj_id: int) -> bool:
        """
        Delete TeacherCourse by ID.

        :param db: Database session.
        :param obj_id: ID to delete.
        :return: True if deleted, False otherwise.
        """
        obj = await self.get_by_id(db, obj_id)
        if not obj:
            return False
        await db.delete(obj)
        await db.commit()
        return True


teacher_course_crud = CRUDTeacherCourse()
