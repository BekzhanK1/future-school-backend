from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_

from app.models.classroom import Classroom
from app.schemas.classroom import ClassroomCreate, ClassroomUpdate


class CRUDClassroom:
    async def create(
        self, db: AsyncSession, classroom_in: ClassroomCreate
    ) -> Classroom:
        """
        Create a new classroom in the database.

        :param classroom_in: ClassroomCreate schema containing classroom details.
        :param db: Database session.
        :return: The created Classroom object.
        """
        print(classroom_in.model_dump())
        classroom = Classroom(**classroom_in.model_dump())
        db.add(classroom)
        await db.commit()
        await db.refresh(classroom)
        return classroom

    async def get_by_id(self, db: AsyncSession, classroom_id: int) -> Classroom | None:
        """
        Retrieve a classroom by its ID.

        :param classroom_id: The ID of the classroom to retrieve.
        :param db: Database session.
        :return: The Classroom object if found, otherwise None.
        """
        return await db.get(Classroom, classroom_id)

    async def get_by_kundelik_id(
        self, db: AsyncSession, kundelik_id: str
    ) -> Classroom | None:
        """
        Retrieve a classroom by its Kundelik ID.

        :param kundelik_id: The Kundelik ID of the classroom to retrieve.
        :param db: Database session.
        :return: The Classroom object if found, otherwise None.
        """
        result = await db.execute(
            select(Classroom).where(Classroom.kundelik_id == kundelik_id)
        )
        return result.scalars().first()

    async def list_all_for_school(
        self, db: AsyncSession, school_id: int
    ) -> list[Classroom]:
        """
        Retrieve all classrooms for a specific school.

        :param school_id: The ID of the school to filter classrooms.
        :param db: Database session.
        :return: A list of Classroom objects for the specified school.
        """
        result = await db.execute(
            select(Classroom).where(Classroom.school_id == school_id)
        )
        return result.scalars().all()

    async def update_by_id(
        self, db: AsyncSession, classroom_id: int, classroom_update: ClassroomUpdate
    ) -> Classroom | None:
        """
        Update a classroom by its ID.

        :param classroom_id: The ID of the classroom to update.
        :param classroom_update: ClassroomUpdate schema containing updated details.
        :param db: Database session.
        :return: The updated Classroom object if found and updated, otherwise None.
        """
        classroom = await self.get_by_id(db, classroom_id)
        if not classroom:
            return None
        for key, value in classroom_update.model_dump().items():
            setattr(classroom, key, value)
        await db.commit()
        await db.refresh(classroom)
        return classroom

    async def delete_by_id(self, db: AsyncSession, classroom_id: int) -> bool:
        """
        Delete a classroom by its ID.

        :param classroom_id: The ID of the classroom to delete.
        :param db: Database session.
        :return: True if deleted successfully, otherwise False.
        """
        classroom = await self.get_by_id(db, classroom_id)
        if not classroom:
            return False
        await db.delete(classroom)
        await db.commit()
        return True


classroom_crud = CRUDClassroom()
