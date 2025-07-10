from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.classroom_course import ClassroomCourse
from app.schemas.classroom_course import ClassroomCourseCreate, ClassroomCourseUpdate


class CRUDClassroomCourse:
    async def create(
        self, db: AsyncSession, obj_in: ClassroomCourseCreate
    ) -> ClassroomCourse:
        """
        Create a new ClassroomCourse.

        :param db: Database session.
        :param obj_in: ClassroomCourseCreate schema with data.
        :return: Created ClassroomCourse object.
        """
        obj = ClassroomCourse(**obj_in.model_dump())
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def get_by_id(self, db: AsyncSession, obj_id: int) -> ClassroomCourse | None:
        """
        Get a ClassroomCourse by its ID.

        :param db: Database session.
        :param obj_id: ID of the ClassroomCourse.
        :return: ClassroomCourse object if found, otherwise None.
        """
        return await db.get(ClassroomCourse, obj_id)

    async def list_all(self, db: AsyncSession) -> list[ClassroomCourse]:
        """
        List all ClassroomCourse records.

        :param db: Database session.
        :return: List of ClassroomCourse objects.
        """
        result = await db.execute(select(ClassroomCourse))
        return result.scalars().all()

    async def update_by_id(
        self, db: AsyncSession, obj_id: int, obj_in: ClassroomCourseUpdate
    ) -> ClassroomCourse | None:
        """
        Update a ClassroomCourse by ID.

        :param db: Database session.
        :param obj_id: ID to update.
        :param obj_in: Update schema.
        :return: Updated ClassroomCourse object or None.
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
        Delete a ClassroomCourse by ID.

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


classroom_course_crud = CRUDClassroomCourse()
