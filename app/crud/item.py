from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Item
from app.schemas.item import ItemCreate, ItemUpdate


async def create_item(item_create: ItemCreate, db: AsyncSession):
    item = Item(
        name=item_create.name,
        description=item_create.description,
        price=item_create.price,
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


async def get_items(db: AsyncSession):
    result = await db.execute(select(Item))
    return result.scalars().all()


async def get_item(item_id: int, db: AsyncSession):
    result = await db.execute(select(Item).filter(Item.id == item_id))
    item = result.scalars().first()
    return item


async def update_item(item_id: int, item_update: ItemUpdate, db: AsyncSession):
    item = await get_item(item_id, db)
    if not item:
        return None
    if item_update.name is not None:
        item.name = item_update.name
    if item_update.description is not None:
        item.description = item_update.description
    if item_update.price is not None:
        item.price = item_update.price
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


async def delete_item(item_id: int, db: AsyncSession):
    item = await get_item(item_id, db)
    if not item:
        return None
    await db.delete(item)
    await db.commit()
    return item
