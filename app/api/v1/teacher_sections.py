from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.auth import require_roles
from app.models.user import User, UserRole
from app.schemas.course_section import (
    CourseSectionCreate,
    CourseSectionUpdate,
    CourseSectionOut,
)
from app.schemas.resource import ResourceCreate, ResourceUpdate, ResourceOut
from app.crud.course_section import course_section_crud
from app.crud.resource import resource_crud
from app.services.storage_service import save_upload
from app.models.resource import ResourceType


router = APIRouter()


@router.post("/sections", response_model=CourseSectionOut)
async def create_section(
    payload: CourseSectionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.TEACHER)),
):
    section = await course_section_crud.create(db, payload)
    return CourseSectionOut.model_validate(section)


@router.get("/sections", response_model=list[CourseSectionOut])
async def list_sections(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.TEACHER)),
):
    sections = await course_section_crud.list_by_course(db, course_id)
    return [CourseSectionOut.model_validate(s) for s in sections]


@router.put("/sections/{section_id}", response_model=CourseSectionOut)
async def update_section(
    section_id: int,
    payload: CourseSectionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.TEACHER)),
):
    updated = await course_section_crud.update_by_id(db, section_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Section not found")
    return CourseSectionOut.model_validate(updated)


@router.delete("/sections/{section_id}")
async def delete_section(
    section_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.TEACHER)),
):
    if not await course_section_crud.delete_by_id(db, section_id):
        raise HTTPException(status_code=404, detail="Section not found")
    return {"detail": "Section deleted"}


@router.post("/resources", response_model=ResourceOut)
async def create_resource(
    payload: ResourceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.TEACHER)),
):
    res = await resource_crud.create(db, payload)
    return ResourceOut.model_validate(res)


@router.post("/resources/upload", response_model=ResourceOut)
async def upload_resource_file(
    course_section_id: int,
    title: str,
    db: AsyncSession = Depends(get_db),
    file: UploadFile = File(...),
    current_user: User = Depends(require_roles(UserRole.TEACHER)),
):
    path = await save_upload(file, subdir=f"section_{course_section_id}")
    res = await resource_crud.create(
        db,
        ResourceCreate(
            course_section_id=course_section_id,
            type=ResourceType.FILE,
            title=title,
            url=path,
        ),
    )
    return ResourceOut.model_validate(res)


@router.get("/resources", response_model=list[ResourceOut])
async def list_resources(
    course_section_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.TEACHER)),
):
    items = await resource_crud.list_by_section(db, course_section_id)
    return [ResourceOut.model_validate(i) for i in items]


@router.put("/resources/{resource_id}", response_model=ResourceOut)
async def update_resource(
    resource_id: int,
    payload: ResourceUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.TEACHER)),
):
    updated = await resource_crud.update_by_id(db, resource_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Resource not found")
    return ResourceOut.model_validate(updated)


@router.delete("/resources/{resource_id}")
async def delete_resource(
    resource_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.TEACHER)),
):
    if not await resource_crud.delete_by_id(db, resource_id):
        raise HTTPException(status_code=404, detail="Resource not found")
    return {"detail": "Resource deleted"}



