from fastapi import APIRouter
from . import items, auth

router = APIRouter()
router.include_router(items.router, prefix="/items")
router.include_router(auth.router, prefix="/auth")
