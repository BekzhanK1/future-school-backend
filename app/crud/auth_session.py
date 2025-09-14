from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.auth_session import AuthSession


class CRUDSession:
    async def create(
        self,
        db: AsyncSession,
        *,
        user_id: int,
        refresh_token: str,
        user_agent: str,
        ip_address: str
    ) -> AuthSession:
        # Сначала деактивируем все существующие сессии для этого пользователя
        existing_sessions = await self.list_by_user(db, user_id)
        for existing_session in existing_sessions:
            if existing_session.is_active:
                await self.deactivate(db, existing_session)
        
        session = AuthSession(
            user_id=user_id,
            refresh_token=refresh_token,
            user_agent=user_agent,
            ip_address=ip_address,
        )
        db.add(session)
        await db.commit()
        await db.refresh(session)
        return session

    async def get_by_refresh_token(
        self, db: AsyncSession, token: str
    ) -> AuthSession | None:
        result = await db.execute(
            select(AuthSession).where(AuthSession.refresh_token == token)
        )
        return result.scalars().first()

    async def deactivate(self, db: AsyncSession, session: AuthSession):
        session.is_active = False
        await db.commit()
        await db.refresh(session)

    async def list_by_user(self, db: AsyncSession, user_id: int):
        result = await db.execute(
            select(AuthSession)
            .where(AuthSession.user_id == user_id)
            .order_by(AuthSession.created_at.desc())
        )
        return result.scalars().all()

    async def get_by_id(self, db: AsyncSession, session_id: int) -> AuthSession | None:
        return await db.get(AuthSession, session_id)

    async def delete_by_id(self, db: AsyncSession, session_id: int):
        session = await self.get_by_id(db, session_id)
        if session:
            await db.delete(session)
            await db.commit()
            return True
        return False


auth_session_crud = CRUDSession()
