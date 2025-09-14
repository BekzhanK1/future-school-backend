from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.classroom_user import classroom_user_crud
from app.crud.user import user_crud
from app.schemas.classroom_user import ClassroomUserCreate, BulkStudentEnrollment, BulkStudentCreate
from app.schemas.user import UserCreate
from app.models.user import UserRole
from app.services.user_service import create_user


async def add_user_to_classroom(obj_in: ClassroomUserCreate, db: AsyncSession):
    """
    Add a user to a classroom.
    :param obj_in: ClassroomUserCreate schema containing user and classroom details.
    :param db: Database session.
    :return: The created ClassroomUser object.
    """
    if not obj_in.classroom_id or not obj_in.user_id:
        raise ValueError("Both classroom_id and user_id must be provided.")

    user = await user_crud.get_by_id(db, obj_in.user_id)
    if not user:
        raise ValueError(f"User with ID {obj_in.user_id} does not exist.")

    return await classroom_user_crud.create(db, obj_in)


async def get_users_for_classroom(classroom_id: int, db: AsyncSession):
    """
    Retrieve all users associated with a specific classroom.
    :param classroom_id: The ID of the classroom to retrieve users for.
    :param db: Database session.
    :return: A list of ClassroomUser objects associated with the classroom.
    """
    return await classroom_user_crud.list_by_classroom(db, classroom_id)


async def get_classrooms_for_user(user_id: int, db: AsyncSession):
    """
    Retrieve all classrooms associated with a specific user.
    :param user_id: The ID of the user to retrieve classrooms for.
    :param db: Database session.
    :return: A list of ClassroomUser objects associated with the user.
    """
    return await classroom_user_crud.list_by_user(db, user_id)


async def remove_user_from_classroom(classroom_id: int, user_id: int, db: AsyncSession):
    """
    Remove a user from a classroom.
    :param classroom_id: The ID of the classroom from which to remove the user.
    :param user_id: The ID of the user to remove.
    :param db: Database session.
    :return: The ClassroomUser object that was deleted.
    """
    return await classroom_user_crud.delete(db, classroom_id, user_id)


async def bulk_enroll_students(
    bulk_enrollment: BulkStudentEnrollment, db: AsyncSession
) -> list:
    """
    Enroll multiple students in a classroom.
    
    :param bulk_enrollment: BulkStudentEnrollment schema containing classroom and student IDs.
    :param db: Database session.
    :return: List of created ClassroomUser objects.
    """
    enrolled_students = []
    
    for student_id in bulk_enrollment.student_ids:
        # Verify the user exists and is a student
        user = await user_crud.get_by_id(db, student_id)
        if not user:
            raise ValueError(f"User with ID {student_id} does not exist.")
        
        if user.role != UserRole.STUDENT:
            raise ValueError(f"User with ID {student_id} is not a student.")
        
        # Create classroom user relationship
        classroom_user_data = ClassroomUserCreate(
            classroom_id=bulk_enrollment.classroom_id,
            user_id=student_id
        )
        
        try:
            classroom_user = await classroom_user_crud.create(db, classroom_user_data)
            enrolled_students.append(classroom_user)
        except Exception as e:
            # If user is already enrolled, skip them
            if "uq_classroom_user_classroom_id_user_id" in str(e):
                continue
            raise e
    
    return enrolled_students


async def bulk_create_students_in_classroom(
    bulk_create: BulkStudentCreate, db: AsyncSession
) -> list:
    """
    Create multiple students and enroll them in a classroom with default password.
    
    :param bulk_create: BulkStudentCreate schema containing classroom and student data.
    :param db: Database session.
    :return: List of created ClassroomUser objects.
    """
    created_students = []
    default_password = "qwerty123"
    
    for student_data in bulk_create.students:
        # Create username from first_name and last_name
        username = f"{student_data['first_name'].lower()}.{student_data['last_name'].lower()}"
        
        # Create user data
        user_data = UserCreate(
            username=username,
            email=student_data['email'],
            role=UserRole.STUDENT,
            password=default_password,
            is_active=True
        )
        
        try:
            # Create the user
            user = await create_user(user_data, db)
            
            # Enroll in classroom
            classroom_user_data = ClassroomUserCreate(
                classroom_id=bulk_create.classroom_id,
                user_id=user.id
            )
            
            classroom_user = await classroom_user_crud.create(db, classroom_user_data)
            created_students.append(classroom_user)
            
        except Exception as e:
            # If user already exists, try to enroll them
            if "uq_users_username" in str(e) or "uq_users_email" in str(e):
                # Find existing user by email
                existing_user = await user_crud.get_by_email(db, student_data['email'])
                if existing_user and existing_user.role == UserRole.STUDENT:
                    try:
                        classroom_user_data = ClassroomUserCreate(
                            classroom_id=bulk_create.classroom_id,
                            user_id=existing_user.id
                        )
                        classroom_user = await classroom_user_crud.create(db, classroom_user_data)
                        created_students.append(classroom_user)
                    except Exception as enroll_error:
                        if "uq_classroom_user_classroom_id_user_id" not in str(enroll_error):
                            raise enroll_error
                        # User already enrolled, skip
                        continue
                else:
                    raise e
            else:
                raise e
    
    return created_students
