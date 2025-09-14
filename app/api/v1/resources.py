from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.dependencies.auth import get_current_user, require_roles
from app.models.user import User, UserRole
from app.models.resource import ResourceType
from app.schemas.resource import ResourceCreate, ResourceOut, ResourceUpdate
from app.services.resource_service import (
    create_resource,
    get_resource_by_id,
    get_resources_by_section,
    get_resources_by_course,
    update_resource,
    delete_resource,
    reorder_resources_in_section,
    get_resources_by_type,
)
from app.services.storage_service import save_upload

router = APIRouter()


@router.post("/", response_model=ResourceOut)
async def create_resource_endpoint(
    resource_data: ResourceCreate,
    file: UploadFile | None = File(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.TEACHER)),
):
    """Create a new resource (file or link)"""
    file_url = None
    if file:
        file_url = await save_upload(file, subdir=f"section_{resource_data.course_section_id}")
        if not resource_data.url:
            resource_data.url = file_url
    
    try:
        resource = await create_resource(resource_data, current_user.id, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return ResourceOut.model_validate(resource)


@router.get("/{resource_id}", response_model=ResourceOut)
async def get_resource(
    resource_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific resource by ID"""
    resource = await get_resource_by_id(resource_id, db)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return ResourceOut.model_validate(resource)


@router.get("/section/{section_id}", response_model=list[ResourceOut])
async def get_resources_by_section_endpoint(
    section_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all resources for a specific course section"""
    resources = await get_resources_by_section(section_id, db)
    return [ResourceOut.model_validate(resource) for resource in resources]


@router.get("/course/{course_id}", response_model=list[ResourceOut])
async def get_resources_by_course_endpoint(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all resources for a specific course (across all sections)"""
    resources = await get_resources_by_course(course_id, db)
    return [ResourceOut.model_validate(resource) for resource in resources]


@router.get("/section/{section_id}/type/{resource_type}", response_model=list[ResourceOut])
async def get_resources_by_type_endpoint(
    section_id: int,
    resource_type: ResourceType,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get resources of a specific type within a section"""
    resources = await get_resources_by_type(section_id, resource_type, db)
    return [ResourceOut.model_validate(resource) for resource in resources]


@router.put("/{resource_id}", response_model=ResourceOut)
async def update_resource_endpoint(
    resource_id: int,
    resource_update: ResourceUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.TEACHER)),
):
    """Update a resource"""
    try:
        resource = await update_resource(resource_id, resource_update, current_user.id, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return ResourceOut.model_validate(resource)


@router.delete("/{resource_id}")
async def delete_resource_endpoint(
    resource_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.TEACHER)),
):
    """Delete a resource"""
    try:
        deleted = await delete_resource(resource_id, current_user.id, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not deleted:
        raise HTTPException(status_code=404, detail="Resource not found")
    return {"detail": "Resource deleted successfully"}


@router.put("/section/{section_id}/reorder")
async def reorder_resources_endpoint(
    section_id: int,
    resource_orders: dict[int, int],
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.TEACHER)),
):
    """Reorder resources within a course section"""
    try:
        resources = await reorder_resources_in_section(section_id, resource_orders, current_user.id, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return [ResourceOut.model_validate(resource) for resource in resources]
