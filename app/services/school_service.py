from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.school import school_crud
from app.models.school import School
from app.schemas.school import SchoolCreate, SchoolOut, SchoolUpdate


async def create_school(school_in: SchoolCreate, db: AsyncSession) -> School:
    """
    Create a new school in the database.

    :param school_in: SchoolCreate schema containing school details.
    :param db: Database session.
    :return: The created School object.
    """
    return await school_crud.create(db, school_in)


async def get_school_by_id(school_id: int, db: AsyncSession) -> School | None:
    """
    Retrieve a school by its ID.

    :param school_id: The ID of the school to retrieve.
    :param db: Database session.
    :return: The School object if found, otherwise None.
    """
    return await school_crud.get_by_id(db, school_id)


async def get_school_by_kundelik_id(
    kundelik_id: str, db: AsyncSession
) -> School | None:
    """
    Retrieve a school by its Kundelik ID.

    :param kundelik_id: The Kundelik ID of the school to retrieve.
    :param db: Database session.
    :return: The School object if found, otherwise None.
    """


async def list_all_schools(db: AsyncSession) -> list[School]:
    """
    Retrieve all schools from the database.

    :param db: Database session.
    :return: A list of School objects representing all schools.
    """
    return await school_crud.list_all(db)


async def list_filtered_schools(
    db: AsyncSession, filters: dict[str, str]
) -> list[School]:
    """
    Retrieve schools based on filtering criteria.

    :param db: Database session.
    :param filters: Dictionary containing filter criteria.
    :return: A list of School objects matching the filters.
    """
    name = filters.get("name")
    city = filters.get("city")
    country = filters.get("country")
    return await school_crud.list_filtered(db, name=name, city=city, country=country)


async def update_school_by_id(
    school_id: int, school_in: SchoolUpdate, db: AsyncSession
) -> School | None:
    """
    Update an existing school.

    :param school_id: The ID of the school to update.
    :param school_in: SchoolUpdate schema containing updated school details.
    :param db: Database session.
    :return: The updated School object if successful, otherwise None.
    """
    return await school_crud.update(db, school_id, school_in)


async def delete_school_by_id(school_id: int, db: AsyncSession) -> bool:
    """
    Delete a school by its ID.

    :param school_id: The ID of the school to delete.
    :param db: Database session.
    :return: True if the school was deleted successfully, otherwise False.
    """
    return await school_crud.delete(db, school_id)
