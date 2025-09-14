from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.course_section import CourseSection
from app.models.course import Course
from app.models.user import User, UserRole
from app.schemas.course_section import CourseSectionCreate, CourseSectionUpdate
from app.crud.course_section import course_section_crud


async def create_course_section(
    section_in: CourseSectionCreate, 
    db: AsyncSession
) -> CourseSection:
    """
    Create a new course section.
    
    :param section_in: CourseSectionCreate schema containing section details.
    :param db: Database session.
    :return: The created CourseSection object.
    """
    # Verify the course exists
    course = await db.get(Course, section_in.course_id)
    if not course:
        raise ValueError(f"Course with ID {section_in.course_id} does not exist.")
    
    return await course_section_crud.create(db, section_in)


async def get_course_section_by_id(
    section_id: int, db: AsyncSession
) -> CourseSection | None:
    """
    Retrieve a course section by its ID.
    
    :param section_id: The ID of the section to retrieve.
    :param db: Database session.
    :return: The CourseSection object if found, otherwise None.
    """
    return await course_section_crud.get_by_id(db, section_id)


async def get_course_sections_by_course(
    course_id: int, db: AsyncSession
) -> list[CourseSection]:
    """
    Retrieve all sections for a specific course.
    
    :param course_id: The ID of the course to filter sections.
    :param db: Database session.
    :return: A list of CourseSection objects for the specified course.
    """
    return await course_section_crud.list_by_course(db, course_id)


async def get_course_section_with_resources(
    section_id: int, db: AsyncSession
) -> CourseSection | None:
    """
    Retrieve a course section with its resources.
    
    :param section_id: The ID of the section to retrieve.
    :param db: Database session.
    :return: The CourseSection object with resources if found, otherwise None.
    """
    result = await db.execute(
        select(CourseSection)
        .options(selectinload(CourseSection.resources))
        .where(CourseSection.id == section_id)
    )
    return result.scalar_one_or_none()


async def update_course_section(
    section_id: int, 
    section_update: CourseSectionUpdate, 
    teacher_id: int,
    db: AsyncSession
) -> CourseSection | None:
    """
    Update a course section by its ID.
    
    :param section_id: The ID of the section to update.
    :param section_update: CourseSectionUpdate schema containing updated details.
    :param teacher_id: ID of the teacher updating the section.
    :param db: Database session.
    :return: The updated CourseSection object if successful, otherwise None.
    """
    # Verify the section exists
    section = await get_course_section_by_id(section_id, db)
    if not section:
        return None
    
    # Note: In a real system, you might want to verify that the teacher
    # has permission to modify this section (e.g., they teach the course)
    
    return await course_section_crud.update_by_id(db, section_id, section_update)


async def delete_course_section(
    section_id: int, 
    teacher_id: int,
    db: AsyncSession
) -> bool:
    """
    Delete a course section by its ID.
    
    :param section_id: The ID of the section to delete.
    :param teacher_id: ID of the teacher deleting the section.
    :param db: Database session.
    :return: True if deleted successfully, otherwise False.
    """
    # Verify the section exists
    section = await get_course_section_by_id(section_id, db)
    if not section:
        return False
    
    # Note: In a real system, you might want to verify that the teacher
    # has permission to delete this section
    
    return await course_section_crud.delete_by_id(db, section_id)


async def reorder_course_sections(
    course_id: int, 
    section_orders: dict[int, int], 
    teacher_id: int,
    db: AsyncSession
) -> list[CourseSection]:
    """
    Reorder sections within a course.
    
    :param course_id: The ID of the course.
    :param section_orders: Dictionary mapping section_id to new position.
    :param teacher_id: ID of the teacher reordering sections.
    :param db: Database session.
    :return: List of updated CourseSection objects.
    """
    sections = await get_course_sections_by_course(course_id, db)
    updated_sections = []
    
    for section in sections:
        if section.id in section_orders:
            section.position = section_orders[section.id]
            updated_sections.append(section)
    
    await db.commit()
    return updated_sections
