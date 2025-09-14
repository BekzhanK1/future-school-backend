from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.password_reset import PasswordResetToken


class CRUDPasswordReset:
    async def create(self, db: AsyncSession, user_id: int, token: str) -> PasswordResetToken:
        prt = PasswordResetToken(user_id=user_id, token=token)
        db.add(prt)
        await db.commit()
        await db.refresh(prt)
        return prt

    async def get_valid(self, db: AsyncSession, token: str) -> PasswordResetToken | None:
        result = await db.execute(
            select(PasswordResetToken).where(PasswordResetToken.token == token)
        )
        prt = result.scalars().first()
        if not prt or prt.used or prt.expires_at < datetime.utcnow():
            return None
        return prt

    async def mark_used(self, db: AsyncSession, prt: PasswordResetToken) -> None:
        prt.used = True
        await db.commit()
        await db.refresh(prt)


password_reset_crud = CRUDPasswordReset()



