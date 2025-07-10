from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, or_

from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate


class CRUDCourse:
    async def create(self, db: AsyncSession, course_in: CourseCreate) -> Course:
        """
        Create a new course in the database.

        :param course_in: CourseCreate schema containing course details.
        :param db: Database session.
        :return: The created Course object.
        """
        print(course_in.model_dump())
        course = Course(**course_in.model_dump())
        db.add(course)
        await db.commit()
        await db.refresh(course)
        return course

    async def get_by_id(self, db: AsyncSession, course_id: int) -> Course | None:
        """
        Retrieve a course by its ID.

        :param course_id: The ID of the course to retrieve.
        :param db: Database session.
        :return: The Course object if found, otherwise None.
        """
        return await db.get(Course, course_id)

    async def get_by_course_code(
        self, db: AsyncSession, course_code: str
    ) -> Course | None:
        """
        Retrieve a course by its course code.

        :param course_code: The course code of the course to retrieve.
        :param db: Database session.
        :return: The Course object if found, otherwise None.
        """
        result = await db.execute(
            select(Course).where(Course.course_code == course_code)
        )
        return result.scalars().first()

    async def list_all(self, db: AsyncSession) -> list[Course]:
        """
        Retrieve all courses from the database.

        :param db: Database session.
        :return: A list of all Course objects.
        """
        result = await db.execute(select(Course))
        return result.scalars().all()

    async def search_courses(
        self,
        db: AsyncSession,
        query: str | None = None,
        grade: int | None = None,
    ) -> list[Course]:
        """
        Flexible course search.

        :param db: Database session.
        :param query: Optional search text for name or code.
        :param classroom_id: Optional classroom filter.
        :return: List of Course objects.
        """
        stmt = select(Course)

        filters = []

        if query:
            filters.append(
                or_(
                    Course.name.ilike(f"%{query}%"),
                    Course.course_code.ilike(f"%{query}%"),
                )
            )

        if grade is not None:
            filters.append(Course.grade == grade)

        if filters:
            stmt = stmt.where(and_(*filters))

        result = await db.execute(stmt)
        return result.scalars().all()

    async def update_by_id(
        self, db: AsyncSession, course_id: int, course_update: CourseUpdate
    ) -> Course | None:
        """
        Update a course by its ID.

        :param course_id: The ID of the course to update.
        :param course_update: CourseUpdate schema containing updated details.
        :param db: Database session.
        :return: The updated Course object if found and updated, otherwise None.
        """
        course = await self.get_by_id(db, course_id)
        if not course:
            return None

        # Only update non-None fields
        update_data = course_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(course, key, value)

        await db.commit()
        await db.refresh(course)
        return course

    async def delete_by_id(self, db: AsyncSession, course_id: int) -> bool:
        """
        Delete a course by its ID.

        :param course_id: The ID of the course to delete.
        :param db: Database session.
        :return: True if deleted successfully, otherwise False.
        """
        course = await self.get_by_id(db, course_id)
        if not course:
            return False
        await db.delete(course)
        await db.commit()
        return True


course_crud = CRUDCourse()
