from app.db.base_class import Base
from app.models import Item, User, School, Classroom, AuthSession
from app.db.session import engine


import os
from app.schemas.user import UserCreate, UserRole
from app.services.user_service import create_user
from app.crud.user import user_crud


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def init_superadmin(db):
    email = os.getenv("SUPERADMIN_EMAIL")
    password = os.getenv("SUPERADMIN_PASSWORD")
    username = os.getenv("SUPERADMIN_USERNAME", "superadmin")

    existing = await user_crud.get_by_email(db, email)
    if existing:
        return  # already created

    superadmin = UserCreate(
        username=username,
        email=email,
        password=password,
        role=UserRole.superadmin,
        is_active=True,
    )

    await create_user(superadmin, db)
