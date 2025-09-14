from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.auth import require_roles
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserOut
from app.services.user_service import create_user
from app.crud.user import user_crud
from app.models.school import School


router = APIRouter()


@router.get("/users", response_model=list[UserOut])
async def list_users(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SUPERADMIN, UserRole.SCHOOLADMIN)),
):
    users = await user_crud.list_by_roles(db, [UserRole.TEACHER, UserRole.STUDENT])
    return [UserOut.model_validate(u) for u in users]


@router.post("/users", response_model=UserOut)
async def add_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SUPERADMIN, UserRole.SCHOOLADMIN)),
):
    created = await create_user(user_in, db)
    return UserOut.model_validate(created)


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SUPERADMIN, UserRole.SCHOOLADMIN)),
):
    if not await user_crud.delete_by_id(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}




