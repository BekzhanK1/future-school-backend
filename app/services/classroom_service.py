from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.classroom import classroom_crud
from app.models.classroom import Classroom
from app.schemas.classroom import ClassroomCreate, ClassroomOut, ClassroomUpdate, BulkClassroomCreate


async def create_classroom(
    classroom_in: ClassroomCreate, db: AsyncSession
) -> Classroom:
    """
    Create a new classroom in the database.

    :param classroom_in: ClassroomCreate schema containing classroom details.
    :param db: Database session.
    :return: The created Classroom object.
    """
    return await classroom_crud.create(db, classroom_in)


async def get_classroom_by_id(classroom_id: int, db: AsyncSession) -> Classroom | None:
    """
    Retrieve a classroom by its ID.

    :param classroom_id: The ID of the classroom to retrieve.
    :param db: Database session.
    :return: The Classroom object if found, otherwise None.
    """
    return await classroom_crud.get_by_id(db, classroom_id)


async def get_classroom_by_kundelik_id(
    kundelik_id: str, db: AsyncSession
) -> Classroom | None:
    """
    Retrieve a classroom by its Kundelik ID.

    :param kundelik_id: The Kundelik ID of the classroom to retrieve.
    :param db: Database session.
    :return: The Classroom object if found, otherwise None.
    """
    return await classroom_crud.get_by_kundelik_id(db, kundelik_id)


async def list_all_for_school(school_id: int, db: AsyncSession) -> list[Classroom]:
    """
    Retrieve all classrooms for a specific school.

    :param school_id: The ID of the school to filter classrooms.
    :param db: Database session.
    :return: A list of Classroom objects for the specified school.
    """
    return await classroom_crud.list_all_for_school(db, school_id)


async def update_classroom_by_id(
    classroom_id: int, classroom_update: ClassroomUpdate, db: AsyncSession
) -> Classroom | None:
    """
    Update a classroom by its ID.

    :param classroom_id: The ID of the classroom to update.
    :param classroom_update: ClassroomCreate schema containing updated classroom details.
    :param db: Database session.
    :return: The updated Classroom object if successful, otherwise None.
    """
    return await classroom_crud.update_by_id(db, classroom_id, classroom_update)


async def create_bulk_classrooms(
    bulk_create: BulkClassroomCreate, db: AsyncSession
) -> list[Classroom]:
    """
    Create multiple classrooms for a school in bulk.
    
    :param bulk_create: BulkClassroomCreate schema containing bulk creation details.
    :param db: Database session.
    :return: List of created Classroom objects.
    """
    classrooms = []
    letters = ['A', 'B', 'C', 'D', 'E']  # Support up to 5 classes per grade
    
    for grade in bulk_create.grades:
        for i in range(bulk_create.letters_per_grade):
            letter = letters[i]
            classroom_data = ClassroomCreate(
                grade=grade,
                letter=letter,
                language=bulk_create.language,
                school_id=bulk_create.school_id
            )
            classroom = await classroom_crud.create(db, classroom_data)
            classrooms.append(classroom)
    
    return classrooms
