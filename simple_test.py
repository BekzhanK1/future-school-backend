#!/usr/bin/env python3
"""
Упрощенный тест системы управления школой
"""

import requests
import json
import time

# Конфигурация
BASE_URL = "http://localhost:8000"
SUPERADMIN_USERNAME = "superadmin"
SUPERADMIN_PASSWORD = "superadmin"

def test_basic_functionality():
    """Тест основных функций"""
    print("🚀 Запуск упрощенного теста системы")
    print("=" * 50)
    
    session = requests.Session()
    
    # 1. Проверка доступности сервера
    print("1. Проверка доступности сервера...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Сервер доступен")
        else:
            print(f"❌ Сервер недоступен: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False
    
    # 2. Вход в систему
    print("\n2. Вход в систему...")
    login_data = {
        "username": SUPERADMIN_USERNAME,
        "password": SUPERADMIN_PASSWORD
    }
    
    response = session.post(f"{BASE_URL}/v1/auth/login", json=login_data)
    if response.status_code == 200:
        data = response.json()
        access_token = data.get('access_token')
        session.headers.update({'Authorization': f'Bearer {access_token}'})
        print("✅ Успешный вход в систему")
    else:
        print(f"❌ Ошибка входа: {response.status_code} - {response.text}")
        return False
    
    # 3. Создание школы
    print("\n3. Создание школы...")
    school_data = {
        "name": "Тестовая школа",
        "city": "Алматы",
        "country": "Казахстан",
        "contact_email": "test@school.kz",
        "contact_phone": "+7 777 123 4567"
    }
    
    response = session.post(f"{BASE_URL}/v1/schools/", json=school_data)
    if response.status_code == 200:
        school = response.json()
        school_id = school['id']
        print(f"✅ Школа создана: {school['name']} (ID: {school_id})")
    else:
        print(f"❌ Ошибка создания школы: {response.status_code} - {response.text}")
        return False
    
    # 4. Создание класса
    print("\n4. Создание класса...")
    classroom_data = {
        "grade": 1,
        "letter": "A",
        "language": "kz",
        "school_id": school_id
    }
    
    response = session.post(f"{BASE_URL}/v1/classrooms/", json=classroom_data)
    if response.status_code == 200:
        classroom = response.json()
        classroom_id = classroom['id']
        print(f"✅ Класс создан: {classroom['grade']}{classroom['letter']} (ID: {classroom_id})")
    else:
        print(f"❌ Ошибка создания класса: {response.status_code} - {response.text}")
        return False
    
    # 5. Создание курса
    print("\n5. Создание курса...")
    course_data = {
        "course_code": "MATH1",
        "name": "Математика 1 класс",
        "grade": 1,
        "description": "Основы математики"
    }
    
    response = session.post(f"{BASE_URL}/v1/courses/", json=course_data)
    if response.status_code == 200:
        course = response.json()
        course_id = course['id']
        print(f"✅ Курс создан: {course['name']} (ID: {course_id})")
    else:
        print(f"❌ Ошибка создания курса: {response.status_code} - {response.text}")
        return False
    
    # 6. Создание учителя
    print("\n6. Создание учителя...")
    teacher_data = {
        "username": "teacher1",
        "email": "teacher1@school.kz",
        "role": "teacher",
        "password": "teacher123"
    }
    
    response = session.post(f"{BASE_URL}/v1/admin/users", json=teacher_data)
    if response.status_code == 200:
        teacher = response.json()
        teacher_id = teacher['id']
        print(f"✅ Учитель создан: {teacher['username']} (ID: {teacher_id})")
    else:
        print(f"❌ Ошибка создания учителя: {response.status_code} - {response.text}")
        return False
    
    # 7. Создание студента
    print("\n7. Создание студента...")
    student_data = {
        "classroom_id": classroom_id,
        "students": [
            {"first_name": "Айдар", "last_name": "Ахметов", "email": "aidar@student.kz"}
        ]
    }
    
    response = session.post(f"{BASE_URL}/v1/classroom_users/bulk-create-students", json=student_data)
    if response.status_code == 200:
        students = response.json()
        student_id = students[0]['user']['id']
        print(f"✅ Студент создан: {students[0]['user']['username']} (ID: {student_id})")
    else:
        print(f"❌ Ошибка создания студента: {response.status_code} - {response.text}")
        return False
    
    # 8. Создание связи курс-класс-учитель
    print("\n8. Создание связи курс-класс-учитель...")
    subject_group_data = {
        "course_id": course_id,
        "classroom_id": classroom_id,
        "teacher_id": teacher_id
    }
    
    response = session.post(f"{BASE_URL}/v1/subject-groups/", json=subject_group_data)
    if response.status_code == 200:
        group = response.json()
        print(f"✅ Связь создана: курс {course_id} -> класс {classroom_id} -> учитель {teacher_id}")
    else:
        print(f"❌ Ошибка создания связи: {response.status_code} - {response.text}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 Все основные функции работают!")
    print("✅ Система готова к использованию")
    
    return True

if __name__ == "__main__":
    test_basic_functionality()
