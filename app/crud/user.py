from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate


class CRUDUser:
    async def create(self, db: AsyncSession, user_in: UserCreate) -> User:
        user = User(**user_in.model_dump())
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def get_by_email(self, db: AsyncSession, email: str) -> User:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def get_by_username(self, db: AsyncSession, username: str) -> User:
        result = await db.execute(select(User).where(User.username == username))
        return result.scalars().first()

    async def get_by_id(self, db: AsyncSession, user_id: int) -> User:
        return await db.get(User, user_id)


user_crud = CRUDUser()
