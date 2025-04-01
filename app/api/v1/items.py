from fastapi import APIRouter, Depends, HTTPException
from app.crud.item import create_item, get_item, get_items, update_item
from app.schemas.item import ItemCreate, ItemRead, ItemUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db

router = APIRouter()


@router.post("/items/", response_model=ItemRead)
async def create_item_router(item: ItemCreate, db: AsyncSession = Depends(get_db)):
    return await create_item(item, db)


@router.get("/items/", response_model=list[ItemRead])
async def read_items_router(db: AsyncSession = Depends(get_db)):
    return await get_items(db)


@router.get("/items/{item_id}", response_model=ItemRead)
async def read_item_router(item_id: int, db: AsyncSession = Depends(get_db)):
    item = await get_item(item_id, db)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.patch("/items/{item_id}", response_model=ItemRead)
async def update_item_router(
    item_id: int, item: ItemUpdate, db: AsyncSession = Depends(get_db)
):

    item = await update_item(item_id, item, db)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
