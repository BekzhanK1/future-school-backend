from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

# Placeholder imports; real integration would use KunAPI and map to local models
from .kundelik import KunAPI  # noqa: F401


async def sync_from_kundelik(
    db: AsyncSession,
    *,
    school_id: int | None = None,
    scope: Sequence[str] | None = None,
) -> dict:
    """
    Placeholder sync function. In production, this would:
    - Authenticate to Kundelik
    - Fetch entities per scope (journal, courses, calendar, users)
    - Upsert into local DB within a transaction
    """
    # TODO: implement actual sync logic
    return {
        "synced": False,
        "school_id": school_id,
        "scope": list(scope or []),
        "detail": "Kundelik sync not implemented yet",
    }



