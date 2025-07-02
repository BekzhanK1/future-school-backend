from fastapi import APIRouter

from . import auth
from . import schools
from . import classroom
from . import classroom_user

router = APIRouter()
# router.include_router(items.router, prefix="/items")
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(schools.router, prefix="/schools", tags=["Schools"])
router.include_router(classroom.router, prefix="/classrooms", tags=["Classrooms"])
router.include_router(
    classroom_user.router, prefix="/classroom_users", tags=["Classrooms-Users"]
)
