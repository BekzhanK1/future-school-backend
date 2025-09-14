from fastapi import APIRouter

from . import auth
from . import schools
from . import classroom
from . import classroom_user
from . import course
from . import student
from . import teacher
from . import admin
from . import superadmin
from . import kundelik
from . import teacher_sections
from . import subject_groups
from . import assignments
from . import submissions
from . import grades
from . import course_sections
from . import resources

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(schools.router, prefix="/schools", tags=["Schools"])
router.include_router(classroom.router, prefix="/classrooms", tags=["Classrooms"])
router.include_router(
    classroom_user.router, prefix="/classroom_users", tags=["Classrooms-Users"]
)
router.include_router(course.router, prefix="/courses", tags=["Courses"])
router.include_router(student.router, prefix="/student", tags=["Student"])
router.include_router(teacher.router, prefix="/teacher", tags=["Teacher"])
router.include_router(admin.router, prefix="/admin", tags=["Admin"])
router.include_router(superadmin.router, prefix="/superadmin", tags=["SuperAdmin"])
router.include_router(kundelik.router, prefix="/kundelik", tags=["Kundelik"])
router.include_router(teacher_sections.router, prefix="/teacher", tags=["Teacher-Sections"])
router.include_router(subject_groups.router, prefix="/subject-groups", tags=["Subject-Groups"])
router.include_router(assignments.router, prefix="/assignments", tags=["Assignments"])
router.include_router(submissions.router, prefix="/submissions", tags=["Submissions"])
router.include_router(grades.router, prefix="/grades", tags=["Grades"])
router.include_router(course_sections.router, prefix="/course-sections", tags=["Course-Sections"])
router.include_router(resources.router, prefix="/resources", tags=["Resources"])
