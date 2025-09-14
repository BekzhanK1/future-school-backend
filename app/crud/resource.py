from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.resource import Resource, ResourceType
from app.schemas.resource import ResourceCreate, ResourceUpdate


class CRUDResource:
    async def create(self, db: AsyncSession, obj_in: ResourceCreate) -> Resource:
        data = obj_in.model_dump()
        # Конвертируем строку в enum
        data['type'] = ResourceType(data['type'])
        obj = Resource(**data)
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def get_by_id(self, db: AsyncSession, obj_id: int) -> Resource | None:
        return await db.get(Resource, obj_id)

    async def list_by_section(self, db: AsyncSession, section_id: int) -> list[Resource]:
        result = await db.execute(
            select(Resource).where(Resource.course_section_id == section_id).order_by(Resource.position)
        )
        return result.scalars().all()

    async def update_by_id(
        self, db: AsyncSession, obj_id: int, obj_in: ResourceUpdate
    ) -> Resource | None:
        obj = await self.get_by_id(db, obj_id)
        if not obj:
            return None
        data = obj_in.model_dump(exclude_unset=True)
        for k, v in data.items():
            setattr(obj, k, v)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def delete_by_id(self, db: AsyncSession, obj_id: int) -> bool:
        obj = await self.get_by_id(db, obj_id)
        if not obj:
            return False
        await db.delete(obj)
        await db.commit()
        return True


resource_crud = CRUDResource()



