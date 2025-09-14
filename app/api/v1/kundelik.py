from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.auth import require_roles
from app.models.user import User, UserRole
from app.services.integrations.kundelik_sync import sync_from_kundelik


router = APIRouter()


@router.post("/sync")
async def sync(
    school_id: int | None = None,
    scope: list[str] | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.SUPERADMIN, UserRole.SCHOOLADMIN)),
):
    return await sync_from_kundelik(db, school_id=school_id, scope=scope or [])



