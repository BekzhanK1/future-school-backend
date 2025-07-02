# app/crud/classroom_user.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.classroom_user import ClassroomUser
from app.schemas.classroom_user import ClassroomUserCreate


class CRUDClassroomUser:

    async def create(
        self, db: AsyncSession, obj_in: ClassroomUserCreate
    ) -> ClassroomUser:
        classroom_user = ClassroomUser(**obj_in.model_dump())
        db.add(classroom_user)
        await db.commit()
        await db.refresh(classroom_user)
        return classroom_user

    async def list_by_classroom(
        self, db: AsyncSession, classroom_id: int
    ) -> list[ClassroomUser]:
        result = await db.execute(
            select(ClassroomUser)
            .options(
                selectinload(ClassroomUser.user), selectinload(ClassroomUser.classroom)
            )
            .where(ClassroomUser.classroom_id == classroom_id)
        )
        return result.scalars().all()

    async def list_by_user(self, db: AsyncSession, user_id: int) -> list[ClassroomUser]:
        result = await db.execute(
            select(ClassroomUser)
            .options(
                selectinload(ClassroomUser.user), selectinload(ClassroomUser.classroom)
            )
            .where(ClassroomUser.user_id == user_id)
        )
        return result.scalars().all()

    async def delete(self, db: AsyncSession, classroom_id: int, user_id: int) -> bool:
        result = await db.execute(
            select(ClassroomUser).where(
                ClassroomUser.classroom_id == classroom_id,
                ClassroomUser.user_id == user_id,
            )
        )
        instance = result.scalars().first()
        if instance:
            await db.delete(instance)
            await db.commit()
            return True
        return False


classroom_user_crud = CRUDClassroomUser()
