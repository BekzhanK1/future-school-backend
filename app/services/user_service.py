from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.crud.user import user_crud
from app.models.classroom import Classroom
from app.models.school import School
from app.schemas.user import UserCreate


async def create_user(user_in: UserCreate, db: AsyncSession):
    # Optional: validate school and classroom if assigned
    if user_in.school_id:
        school = await db.get(School, user_in.school_id)
        if not school:
            raise ValueError("School does not exist")

    if user_in.classroom_id:
        classroom = await db.get(Classroom, user_in.classroom_id)
        if not classroom:
            raise ValueError("Classroom does not exist")

    user_in.password = hash_password(user_in.password)
    return await user_crud.create(db, user_in)
