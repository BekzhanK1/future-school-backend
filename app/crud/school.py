from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_

from app.models.school import School
from app.schemas.school import SchoolCreate, SchoolUpdate


class CRUDSchool:
    async def create(self, db: AsyncSession, school_in: SchoolCreate) -> School:
        """
        Create a new school in the database.

        :param school_in: SchoolCreate schema containing school details.
        :param db: Database session.
        :return: The created School object.
        """
        school = School(**school_in.model_dump())
        db.add(school)
        await db.commit()
        await db.refresh(school)
        return school

    async def get_by_id(self, db: AsyncSession, school_id: int) -> School | None:
        """
        Retrieve a school by its ID.

        :param school_id: The ID of the school to retrieve.
        :param db: Database session.
        :return: The School object if found, otherwise None.
        """
        return await db.get(School, school_id)

    async def get_by_kundelik_id(
        self, db: AsyncSession, kundelik_id: str
    ) -> School | None:
        """
        Retrieve a school by its Kundelik ID.

        :param kundelik_id: The Kundelik ID of the school to retrieve.
        :param db: Database session.
        :return: The School object if found, otherwise None.
        """

        result = await db.execute(
            select(School).where(School.kundelik_id == kundelik_id)
        )
        return result.scalars().first()

    async def list_all(self, db: AsyncSession) -> list[School]:
        """
        Retrieve all schools from the database.

        :param db: Database session.
        :return: A list of School objects representing all schools.
        """
        result = await db.execute(select(School))
        return result.scalars().all()

    async def list_filtered(
        self,
        db: AsyncSession,
        name: str | None = None,
        city: str | None = None,
        country: str | None = None,
    ) -> list[School]:
        """
        Retrieve schools filtered by optional parameters.

        :param name: Filter by school name (optional)
        :param city: Filter by city (optional)
        :param kundelik_id: Filter by Kundelik ID (optional)
        :return: List of matching School objects
        """
        query = select(School)
        filters = []

        if name:
            filters.append(School.name.ilike(f"%{name}%"))
        if city:
            filters.append(School.city.ilike(f"%{city}%"))
        if country:
            filters.append(School.country.ilike(f"%{country}%"))

        if filters:
            query = query.where(and_(*filters))

        result = await db.execute(query)
        return result.scalars().all()

    async def update(
        self, db: AsyncSession, school_id: int, school_in: SchoolUpdate
    ) -> School | None:
        """
        Update an existing school.

        :param school_id: The ID of the school to update.
        :param school_in: SchoolUpdate schema containing updated school details.
        :param db: Database session.
        :return: The updated School object if successful, otherwise None.
        """
        school = await self.get_by_id(db, school_id)
        if not school:
            return None

        for key, value in school_in.model_dump().items():
            setattr(school, key, value)

        db.add(school)
        await db.commit()
        await db.refresh(school)
        return school

    async def delete(self, db: AsyncSession, school_id: int) -> bool:
        """
        Delete a school by its ID.
        :param school_id: The ID of the school to delete.
        :param db: Database session.
        :return: True if deletion was successful, otherwise False.
        """
        school = await self.get_by_id(db, school_id)
        if not school:
            return False

        await db.delete(school)
        await db.commit()
        return True


school_crud = CRUDSchool()
