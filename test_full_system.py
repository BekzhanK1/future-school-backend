#!/usr/bin/env python3
"""
Полный тест системы управления школой
Создает все необходимые данные и тестирует все функции
"""

import requests
import json
import time
from datetime import datetime, timedelta

# Конфигурация
BASE_URL = "http://localhost:8000"
SUPERADMIN_USERNAME = "superadmin"
SUPERADMIN_PASSWORD = "superadmin"

class SchoolSystemTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.access_token = None
        self.created_data = {
            'school_id': None,
            'classroom_ids': [],
            'course_ids': [],
            'teacher_ids': [],
            'student_ids': [],
            'subject_group_ids': [],
            'assignment_ids': [],
            'section_ids': [],
            'resource_ids': []
        }

    def login(self):
        """Вход в систему как суперадмин"""
        print("🔐 Вход в систему...")
        
        login_data = {
            "username": SUPERADMIN_USERNAME,
            "password": SUPERADMIN_PASSWORD
        }
        
        response = self.session.post(f"{self.base_url}/v1/auth/login", json=login_data)
        
        if response.status_code == 200:
            data = response.json()
            self.access_token = data.get('access_token')
            self.session.headers.update({'Authorization': f'Bearer {self.access_token}'})
            print("✅ Успешный вход в систему")
            return True
        else:
            print(f"❌ Ошибка входа: {response.status_code} - {response.text}")
            return False

    def create_school(self):
        """Создание школы"""
        print("\n🏫 Создание школы...")
        
        school_data = {
            "name": "Тестовая школа №1",
            "city": "Алматы",
            "country": "Казахстан",
            "contact_email": "school1@test.kz",
            "contact_phone": "+7 777 123 4567",
            "logo_url": "https://example.com/logo.png"
        }
        
        response = self.session.post(f"{self.base_url}/v1/schools/", json=school_data)
        
        if response.status_code == 200:
            school = response.json()
            self.created_data['school_id'] = school['id']
            print(f"✅ Школа создана: {school['name']} (ID: {school['id']})")
            return school
        else:
            print(f"❌ Ошибка создания школы: {response.status_code} - {response.text}")
            return None

    def create_classrooms(self):
        """Создание классов"""
        print("\n📚 Создание классов...")
        
        bulk_classroom_data = {
            "school_id": self.created_data['school_id'],
            "language": "kz",
            "grades": [1, 2, 3, 4, 5],
            "letters_per_grade": 2
        }
        
        response = self.session.post(f"{self.base_url}/v1/classrooms/bulk", json=bulk_classroom_data)
        
        if response.status_code == 200:
            classrooms = response.json()
            self.created_data['classroom_ids'] = [c['id'] for c in classrooms]
            print(f"✅ Создано {len(classrooms)} классов")
            for classroom in classrooms[:5]:  # Показываем первые 5
                print(f"   - {classroom['grade']}{classroom['letter']} (ID: {classroom['id']})")
            return classrooms
        else:
            print(f"❌ Ошибка создания классов: {response.status_code} - {response.text}")
            return None

    def create_courses(self):
        """Создание курсов"""
        print("\n📖 Создание курсов...")
        
        courses_data = [
            {"course_code": "MATH1", "name": "Математика 1 класс", "grade": 1, "description": "Основы математики для 1 класса"},
            {"course_code": "KZ1", "name": "Қазақ тілі 1 сынып", "grade": 1, "description": "Қазақ тілі негіздері"},
            {"course_code": "RUS1", "name": "Русский язык 1 класс", "grade": 1, "description": "Основы русского языка"},
            {"course_code": "MATH2", "name": "Математика 2 класс", "grade": 2, "description": "Математика для 2 класса"},
            {"course_code": "KZ2", "name": "Қазақ тілі 2 сынып", "grade": 2, "description": "Қазақ тілі 2 сынып"},
        ]
        
        bulk_course_data = {"courses": courses_data}
        
        response = self.session.post(f"{self.base_url}/v1/courses/bulk", json=bulk_course_data)
        
        if response.status_code == 200:
            courses = response.json()
            self.created_data['course_ids'] = [c['id'] for c in courses]
            print(f"✅ Создано {len(courses)} курсов")
            for course in courses:
                print(f"   - {course['name']} (ID: {course['id']})")
            return courses
        else:
            print(f"❌ Ошибка создания курсов: {response.status_code} - {response.text}")
            return None

    def create_teachers(self):
        """Создание учителей"""
        print("\n👨‍🏫 Создание учителей...")
        
        teachers_data = [
            {"username": "teacher1", "email": "teacher1@school.kz", "role": "teacher", "password": "teacher123"},
            {"username": "teacher2", "email": "teacher2@school.kz", "role": "teacher", "password": "teacher123"},
            {"username": "teacher3", "email": "teacher3@school.kz", "role": "teacher", "password": "teacher123"},
        ]
        
        created_teachers = []
        for teacher_data in teachers_data:
            response = self.session.post(f"{self.base_url}/v1/admin/users", json=teacher_data)
            if response.status_code == 200:
                teacher = response.json()
                created_teachers.append(teacher)
                self.created_data['teacher_ids'].append(teacher['id'])
                print(f"✅ Учитель создан: {teacher['username']} (ID: {teacher['id']})")
            else:
                print(f"❌ Ошибка создания учителя {teacher_data['username']}: {response.status_code} - {response.text}")
        
        return created_teachers

    def create_students(self):
        """Создание студентов"""
        print("\n👨‍🎓 Создание студентов...")
        
        # Создаем студентов для первого класса
        classroom_id = self.created_data['classroom_ids'][0]  # Берем первый класс
        
        students_data = {
            "classroom_id": classroom_id,
            "students": [
                {"first_name": "Айдар", "last_name": "Ахметов", "email": "aidar.ahmetov@student.kz"},
                {"first_name": "Айша", "last_name": "Бекова", "email": "aisha.bekova@student.kz"},
                {"first_name": "Данияр", "last_name": "Касымов", "email": "daniyar.kasymov@student.kz"},
                {"first_name": "Жанар", "last_name": "Нургалиева", "email": "zhanar.nurgalieva@student.kz"},
                {"first_name": "Марат", "last_name": "Султанов", "email": "marat.sultanov@student.kz"},
            ]
        }
        
        response = self.session.post(f"{self.base_url}/v1/classroom_users/bulk-create-students", json=students_data)
        
        if response.status_code == 200:
            students = response.json()
            self.created_data['student_ids'] = [s['user']['id'] for s in students]
            print(f"✅ Создано {len(students)} студентов в классе {classroom_id}")
            for student in students:
                print(f"   - {student['user']['username']} (ID: {student['user']['id']})")
            return students
        else:
            print(f"❌ Ошибка создания студентов: {response.status_code} - {response.text}")
            return None

    def create_subject_groups(self):
        """Создание связей курсов, классов и учителей"""
        print("\n🔗 Создание связей курсов, классов и учителей...")
        
        assignments = []
        classroom_id = self.created_data['classroom_ids'][0]  # Первый класс
        
        # Назначаем учителей на курсы
        for i, course_id in enumerate(self.created_data['course_ids'][:3]):  # Первые 3 курса
            teacher_id = self.created_data['teacher_ids'][i % len(self.created_data['teacher_ids'])]
            assignments.append({
                "course_id": course_id,
                "classroom_id": classroom_id,
                "teacher_id": teacher_id
            })
        
        bulk_assignment_data = {"assignments": assignments}
        
        response = self.session.post(f"{self.base_url}/v1/subject-groups/bulk", json=bulk_assignment_data)
        
        if response.status_code == 200:
            groups = response.json()
            self.created_data['subject_group_ids'] = [g['id'] for g in groups]
            print(f"✅ Создано {len(groups)} связей курсов с классами и учителями")
            for group in groups:
                print(f"   - {group['course']['name']} -> {group['classroom']['grade']}{group['classroom']['letter']} -> {group['teacher']['username']}")
            return groups
        else:
            print(f"❌ Ошибка создания связей: {response.status_code} - {response.text}")
            return None

    def create_assignments(self):
        """Создание заданий"""
        print("\n📝 Создание заданий...")
        
        # Входим как учитель для создания заданий
        teacher_login_data = {"username": "teacher1", "password": "teacher123"}
        teacher_response = requests.post(f"{self.base_url}/v1/auth/login", json=teacher_login_data)
        
        if teacher_response.status_code != 200:
            print("❌ Не удалось войти как учитель")
            return None
        
        teacher_token = teacher_response.json()['access_token']
        teacher_session = requests.Session()
        teacher_session.headers.update({'Authorization': f'Bearer {teacher_token}'})
        
        assignments_data = [
            {
                "course_id": self.created_data['course_ids'][0],  # Математика 1 класс
                "title": "Сложение и вычитание",
                "description": "Решите примеры на сложение и вычитание в пределах 10",
                "due_at": (datetime.now() + timedelta(days=7)).isoformat()
            },
            {
                "course_id": self.created_data['course_ids'][1],  # Казахский язык
                "title": "Буквы и звуки",
                "description": "Изучите новые буквы казахского алфавита",
                "due_at": (datetime.now() + timedelta(days=5)).isoformat()
            }
        ]
        
        created_assignments = []
        for assignment_data in assignments_data:
            response = teacher_session.post(f"{self.base_url}/v1/assignments/", json=assignment_data)
            if response.status_code == 200:
                assignment = response.json()
                created_assignments.append(assignment)
                self.created_data['assignment_ids'].append(assignment['id'])
                print(f"✅ Задание создано: {assignment['title']} (ID: {assignment['id']})")
            else:
                print(f"❌ Ошибка создания задания: {response.status_code} - {response.text}")
        
        return created_assignments

    def create_course_sections(self):
        """Создание секций курса"""
        print("\n📚 Создание секций курса...")
        
        # Используем сессию учителя
        teacher_login_data = {"username": "teacher1", "password": "teacher123"}
        teacher_response = requests.post(f"{self.base_url}/v1/auth/login", json=teacher_login_data)
        teacher_token = teacher_response.json()['access_token']
        teacher_session = requests.Session()
        teacher_session.headers.update({'Authorization': f'Bearer {teacher_token}'})
        
        sections_data = [
            {
                "course_id": self.created_data['course_ids'][0],  # Математика
                "title": "Числа от 1 до 10",
                "position": 1
            },
            {
                "course_id": self.created_data['course_ids'][0],
                "title": "Сложение",
                "position": 2
            },
            {
                "course_id": self.created_data['course_ids'][0],
                "title": "Вычитание",
                "position": 3
            }
        ]
        
        created_sections = []
        for section_data in sections_data:
            response = teacher_session.post(f"{self.base_url}/v1/course-sections/", json=section_data)
            if response.status_code == 200:
                section = response.json()
                created_sections.append(section)
                self.created_data['section_ids'].append(section['id'])
                print(f"✅ Секция создана: {section['title']} (ID: {section['id']})")
            else:
                print(f"❌ Ошибка создания секции: {response.status_code} - {response.text}")
        
        return created_sections

    def create_resources(self):
        """Создание ресурсов для секций"""
        print("\n📎 Создание ресурсов...")
        
        # Используем сессию учителя
        teacher_login_data = {"username": "teacher1", "password": "teacher123"}
        teacher_response = requests.post(f"{self.base_url}/v1/auth/login", json=teacher_login_data)
        teacher_token = teacher_response.json()['access_token']
        teacher_session = requests.Session()
        teacher_session.headers.update({'Authorization': f'Bearer {teacher_token}'})
        
        resources_data = [
            {
                "course_section_id": self.created_data['section_ids'][0],
                "type": "link",
                "title": "Видео: Числа от 1 до 10",
                "description": "Обучающее видео про числа",
                "url": "https://youtube.com/watch?v=example1",
                "position": 1
            },
            {
                "course_section_id": self.created_data['section_ids'][0],
                "type": "link",
                "title": "Интерактивная игра",
                "description": "Игра для изучения чисел",
                "url": "https://example.com/game1",
                "position": 2
            },
            {
                "course_section_id": self.created_data['section_ids'][1],
                "type": "link",
                "title": "Презентация: Сложение",
                "description": "Слайды с примерами сложения",
                "url": "https://example.com/presentation1",
                "position": 1
            }
        ]
        
        created_resources = []
        for resource_data in resources_data:
            response = teacher_session.post(f"{self.base_url}/v1/resources/", json=resource_data)
            if response.status_code == 200:
                resource = response.json()
                created_resources.append(resource)
                self.created_data['resource_ids'].append(resource['id'])
                print(f"✅ Ресурс создан: {resource['title']} (ID: {resource['id']})")
            else:
                print(f"❌ Ошибка создания ресурса: {response.status_code} - {response.text}")
        
        return created_resources

    def test_student_submission(self):
        """Тестирование отправки задания студентом"""
        print("\n📤 Тестирование отправки задания студентом...")
        
        # Входим как студент
        student_login_data = {"username": "айдар.ахметов", "password": "qwerty123"}
        student_response = requests.post(f"{self.base_url}/v1/auth/login", json=student_login_data)
        
        if student_response.status_code != 200:
            print("❌ Не удалось войти как студент")
            return None
        
        student_token = student_response.json()['access_token']
        student_session = requests.Session()
        student_session.headers.update({'Authorization': f'Bearer {student_token}'})
        
        # Отправляем задание
        assignment_id = self.created_data['assignment_ids'][0]
        submission_data = {
            "assignment_id": assignment_id,
            "text": "Я решил все примеры! 2+3=5, 7-2=5, 4+1=5"
        }
        
        response = student_session.post(f"{self.base_url}/v1/submissions/", json=submission_data)
        
        if response.status_code == 200:
            submission = response.json()
            print(f"✅ Задание отправлено студентом (ID: {submission['id']})")
            return submission
        else:
            print(f"❌ Ошибка отправки задания: {response.status_code} - {response.text}")
            return None

    def test_teacher_grading(self):
        """Тестирование оценивания учителем"""
        print("\n📊 Тестирование оценивания...")
        
        # Входим как учитель
        teacher_login_data = {"username": "teacher1", "password": "teacher123"}
        teacher_response = requests.post(f"{self.base_url}/v1/auth/login", json=teacher_login_data)
        teacher_token = teacher_response.json()['access_token']
        teacher_session = requests.Session()
        teacher_session.headers.update({'Authorization': f'Bearer {teacher_token}'})
        
        # Получаем отправки для оценивания
        assignment_id = self.created_data['assignment_ids'][0]
        response = teacher_session.get(f"{self.base_url}/v1/submissions/assignment/{assignment_id}")
        
        if response.status_code == 200:
            submissions = response.json()
            if submissions:
                submission = submissions[0]
                
                # Оцениваем
                grade_data = {
                    "submission_id": submission['id'],
                    "grade_value": 85,
                    "feedback": "Отличная работа! Все примеры решены правильно."
                }
                
                grade_response = teacher_session.post(f"{self.base_url}/v1/grades/", json=grade_data)
                
                if grade_response.status_code == 200:
                    grade = grade_response.json()
                    print(f"✅ Оценка поставлена: {grade['grade_value']}/100 (ID: {grade['id']})")
                    return grade
                else:
                    print(f"❌ Ошибка оценивания: {grade_response.status_code} - {grade_response.text}")
            else:
                print("❌ Нет отправок для оценивания")
        else:
            print(f"❌ Ошибка получения отправок: {response.status_code} - {response.text}")
        
        return None

    def test_student_dashboard(self):
        """Тестирование дашборда студента"""
        print("\n📱 Тестирование дашборда студента...")
        
        # Входим как студент
        student_login_data = {"username": "айдар.ахметов", "password": "qwerty123"}
        student_response = requests.post(f"{self.base_url}/v1/auth/login", json=student_login_data)
        student_token = student_response.json()['access_token']
        student_session = requests.Session()
        student_session.headers.update({'Authorization': f'Bearer {student_token}'})
        
        # Получаем курсы студента
        response = student_session.get(f"{self.base_url}/v1/student/courses")
        
        if response.status_code == 200:
            courses = response.json()
            print(f"✅ Студент видит {len(courses)} курсов:")
            for course in courses:
                print(f"   - {course['name']}")
            return courses
        else:
            print(f"❌ Ошибка получения курсов: {response.status_code} - {response.text}")
            return None

    def run_full_test(self):
        """Запуск полного теста системы"""
        print("🚀 Запуск полного теста системы управления школой")
        print("=" * 60)
        
        # Проверяем доступность сервера
        try:
            response = requests.get(f"{self.base_url}/")
            if response.status_code != 200:
                print("❌ Сервер недоступен")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ Не удается подключиться к серверу. Убедитесь, что сервер запущен на порту 8000")
            return False
        
        # Выполняем все тесты
        steps = [
            ("Вход в систему", self.login),
            ("Создание школы", self.create_school),
            ("Создание классов", self.create_classrooms),
            ("Создание курсов", self.create_courses),
            ("Создание учителей", self.create_teachers),
            ("Создание студентов", self.create_students),
            ("Создание связей", self.create_subject_groups),
            ("Создание заданий", self.create_assignments),
            ("Создание секций", self.create_course_sections),
            ("Создание ресурсов", self.create_resources),
            ("Отправка задания", self.test_student_submission),
            ("Оценивание", self.test_teacher_grading),
            ("Дашборд студента", self.test_student_dashboard),
        ]
        
        success_count = 0
        for step_name, step_func in steps:
            try:
                result = step_func()
                if result is not None:
                    success_count += 1
                time.sleep(1)  # Небольшая пауза между шагами
            except Exception as e:
                print(f"❌ Ошибка в шаге '{step_name}': {str(e)}")
        
        print("\n" + "=" * 60)
        print(f"📊 Результаты тестирования: {success_count}/{len(steps)} шагов выполнено успешно")
        
        if success_count == len(steps):
            print("🎉 Все тесты прошли успешно! Система полностью функциональна.")
        else:
            print("⚠️  Некоторые тесты не прошли. Проверьте логи выше.")
        
        return success_count == len(steps)

if __name__ == "__main__":
    tester = SchoolSystemTester()
    tester.run_full_test()
