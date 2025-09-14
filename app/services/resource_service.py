from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.resource import Resource, ResourceType
from app.models.course_section import CourseSection
from app.models.user import User, UserRole
from app.schemas.resource import ResourceCreate, ResourceUpdate
from app.crud.resource import resource_crud


async def create_resource(
    resource_in: ResourceCreate, 
    teacher_id: int, 
    db: AsyncSession
) -> Resource:
    """
    Create a new resource.
    
    :param resource_in: ResourceCreate schema containing resource details.
    :param teacher_id: ID of the teacher creating the resource.
    :param db: Database session.
    :return: The created Resource object.
    """
    # Verify the course section exists
    section = await db.get(CourseSection, resource_in.course_section_id)
    if not section:
        raise ValueError(f"Course section with ID {resource_in.course_section_id} does not exist.")
    
    # Verify the teacher exists and has the correct role
    teacher = await db.get(User, teacher_id)
    if not teacher:
        raise ValueError(f"Teacher with ID {teacher_id} does not exist.")
    
    if teacher.role != UserRole.TEACHER:
        raise ValueError(f"User with ID {teacher_id} is not a teacher.")
    
    return await resource_crud.create(db, resource_in)


async def get_resource_by_id(
    resource_id: int, db: AsyncSession
) -> Resource | None:
    """
    Retrieve a resource by its ID.
    
    :param resource_id: The ID of the resource to retrieve.
    :param db: Database session.
    :return: The Resource object if found, otherwise None.
    """
    return await resource_crud.get_by_id(db, resource_id)


async def get_resources_by_section(
    section_id: int, db: AsyncSession
) -> list[Resource]:
    """
    Retrieve all resources for a specific course section.
    
    :param section_id: The ID of the section to filter resources.
    :param db: Database session.
    :return: A list of Resource objects for the specified section.
    """
    return await resource_crud.list_by_section(db, section_id)


async def get_resources_by_course(
    course_id: int, db: AsyncSession
) -> list[Resource]:
    """
    Retrieve all resources for a specific course (across all sections).
    
    :param course_id: The ID of the course to filter resources.
    :param db: Database session.
    :return: A list of Resource objects for the specified course.
    """
    return await resource_crud.list_by_course(db, course_id)


async def update_resource(
    resource_id: int, 
    resource_update: ResourceUpdate, 
    teacher_id: int,
    db: AsyncSession
) -> Resource | None:
    """
    Update a resource by its ID.
    
    :param resource_id: The ID of the resource to update.
    :param resource_update: ResourceUpdate schema containing updated details.
    :param teacher_id: ID of the teacher updating the resource.
    :param db: Database session.
    :return: The updated Resource object if successful, otherwise None.
    """
    # Verify the resource exists
    resource = await get_resource_by_id(resource_id, db)
    if not resource:
        return None
    
    # Note: In a real system, you might want to verify that the teacher
    # has permission to modify this resource
    
    return await resource_crud.update_by_id(db, resource_id, resource_update)


async def delete_resource(
    resource_id: int, 
    teacher_id: int,
    db: AsyncSession
) -> bool:
    """
    Delete a resource by its ID.
    
    :param resource_id: The ID of the resource to delete.
    :param teacher_id: ID of the teacher deleting the resource.
    :param db: Database session.
    :return: True if deleted successfully, otherwise False.
    """
    # Verify the resource exists
    resource = await get_resource_by_id(resource_id, db)
    if not resource:
        return False
    
    # Note: In a real system, you might want to verify that the teacher
    # has permission to delete this resource
    
    return await resource_crud.delete_by_id(db, resource_id)


async def reorder_resources_in_section(
    section_id: int, 
    resource_orders: dict[int, int], 
    teacher_id: int,
    db: AsyncSession
) -> list[Resource]:
    """
    Reorder resources within a course section.
    
    :param section_id: The ID of the course section.
    :param resource_orders: Dictionary mapping resource_id to new position.
    :param teacher_id: ID of the teacher reordering resources.
    :param db: Database session.
    :return: List of updated Resource objects.
    """
    resources = await get_resources_by_section(section_id, db)
    updated_resources = []
    
    for resource in resources:
        if resource.id in resource_orders:
            resource.position = resource_orders[resource.id]
            updated_resources.append(resource)
    
    await db.commit()
    return updated_resources


async def get_resources_by_type(
    section_id: int, 
    resource_type: ResourceType, 
    db: AsyncSession
) -> list[Resource]:
    """
    Retrieve resources of a specific type within a section.
    
    :param section_id: The ID of the section to filter resources.
    :param resource_type: The type of resources to retrieve.
    :param db: Database session.
    :return: A list of Resource objects of the specified type.
    """
    return await resource_crud.list_by_section_and_type(db, section_id, resource_type)
