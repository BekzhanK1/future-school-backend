from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.course import course_crud
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseOut, CourseUpdate, BulkCourseCreate


async def create_course(course_in: CourseCreate, db: AsyncSession) -> Course:
    """
    Create a new course in the database.

    :param course_in: CourseCreate schema containing course details.
    :param db: Database session.
    :return: The created Course object.
    """
    return await course_crud.create(db, course_in)


async def get_course_by_id(course_id: int, db: AsyncSession) -> Course | None:
    """
    Retrieve a course by its ID.

    :param course_id: The ID of the course to retrieve.
    :param db: Database session.
    :return: The Course object if found, otherwise None.
    """
    return await course_crud.get_by_id(db, course_id)


async def get_course_by_course_code(
    course_code: str, db: AsyncSession
) -> Course | None:
    """
    Retrieve a course by its course code.

    :param course_code: The course code of the course to retrieve.
    :param db: Database session.
    :return: The Course object if found, otherwise None.
    """
    return await course_crud.get_by_course_code(db, course_code)


async def list_all_courses(db: AsyncSession) -> list[Course]:
    """
    Retrieve all courses from the database.

    :param db: Database session.
    :return: A list of all Course objects.
    """
    return await course_crud.list_all(db)


async def search_courses(
    db: AsyncSession,
    query: str | None = None,
    grade: int | None = None,
):
    """
    Flexible service search.

    :param db: Database session.
    :param query: Search text.
    :param classroom_id: Optional classroom ID.
    :return: List of courses.
    """
    return await course_crud.search_courses(db, query, grade)


async def update_course_by_id(
    course_id: int, course_update: CourseUpdate, db: AsyncSession
) -> Course | None:
    """
    Update a course by its ID.

    :param course_id: The ID of the course to update.
    :param course_update: CourseUpdate schema containing updated course details.
    :param db: Database session.
    :return: The updated Course object if successful, otherwise None.
    """
    return await course_crud.update_by_id(db, course_id, course_update)


async def delete_course_by_id(course_id: int, db: AsyncSession) -> bool:
    """
    Delete a course by its ID.

    :param course_id: The ID of the course to delete.
    :param db: Database session.
    :return: True if deleted successfully, otherwise False.
    """
    return await course_crud.delete_by_id(db, course_id)


async def create_bulk_courses(
    bulk_create: BulkCourseCreate, db: AsyncSession
) -> list[Course]:
    """
    Create multiple courses in bulk.
    
    :param bulk_create: BulkCourseCreate schema containing courses to create.
    :param db: Database session.
    :return: List of created Course objects.
    """
    courses = []
    
    for course_data in bulk_create.courses:
        try:
            course = await course_crud.create(db, course_data)
            courses.append(course)
        except Exception as e:
            # If course code already exists, skip it
            if "uq_courses_course_code" in str(e):
                continue
            raise e
    
    return courses
