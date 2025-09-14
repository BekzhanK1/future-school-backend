# 🎓 Система управления школой

Полнофункциональная система управления школой, построенная на FastAPI с поддержкой всех основных функций образовательного процесса.

## 📋 Содержание

- [🚀 Быстрый старт](#-быстрый-старт)
- [🏗️ Архитектура системы](#️-архитектура-системы)
- [📊 Модели данных](#-модели-данных)
- [🔐 Система аутентификации](#-система-аутентификации)
- [📚 API эндпоинты](#-api-эндпоинты)
- [👥 Роли и права доступа](#-роли-и-права-доступа)
- [🧪 Тестирование](#-тестирование)
- [📖 Примеры использования](#-примеры-использования)
- [🔧 Конфигурация](#-конфигурация)
- [📝 Логирование](#-логирование)
- [🚀 Развертывание](#-развертывание)

## 🚀 Быстрый старт

### 🐳 Запуск с Docker (Рекомендуется)

```bash
# Клонируйте репозиторий
git clone <repository-url>
cd future-school-backend

# Запустите приложение
docker-compose up --build

# Приложение будет доступно по адресу: http://localhost:8000
```

### 📋 Локальная установка

```bash
# Клонируйте репозиторий
git clone <repository-url>
cd future-school-backend

# Создайте виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

# Установите зависимости
pip install -r requirements.txt

# Примените миграции
alembic upgrade head

# Создайте суперадмина (опционально)
python scripts/create_superadmin.py

# Запустите сервер
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Доступ к API

- **API документация:** http://localhost:8000/docs
- **Альтернативная документация:** http://localhost:8000/redoc
- **OpenAPI схема:** http://localhost:8000/openapi.json

## 🏗️ Архитектура системы

### Технологический стек

- **Backend:** FastAPI (Python 3.10+)
- **База данных:** SQLite (разработка) / PostgreSQL (продакшен)
- **ORM:** SQLAlchemy (асинхронная)
- **Миграции:** Alembic
- **Валидация:** Pydantic
- **Аутентификация:** JWT токены
- **Хеширование паролей:** bcrypt
- **Файловое хранилище:** Локальная файловая система

### Структура проекта

```
future-school-backend/
├── app/
│   ├── api/                    # API эндпоинты
│   │   └── v1/
│   │       ├── auth.py         # Аутентификация
│   │       ├── schools.py      # Управление школами
│   │       ├── classrooms.py   # Управление классами
│   │       ├── courses.py      # Управление курсами
│   │       ├── users.py        # Управление пользователями
│   │       ├── assignments.py  # Управление заданиями
│   │       ├── submissions.py  # Отправка заданий
│   │       ├── grades.py       # Оценивание
│   │       └── ...
│   ├── core/                   # Основные настройки
│   ├── crud/                   # CRUD операции
│   ├── db/                     # Настройки базы данных
│   ├── models/                 # SQLAlchemy модели
│   ├── schemas/                # Pydantic схемы
│   ├── services/               # Бизнес-логика
│   └── dependencies/           # Зависимости FastAPI
├── alembic/                    # Миграции базы данных
├── scripts/                    # Вспомогательные скрипты
├── tests/                      # Тесты
├── main.py                     # Точка входа
├── requirements.txt            # Зависимости
└── README.md                   # Документация
```

## 📊 Модели данных

### Основные сущности

#### 1. **User (Пользователь)**
```python
class User(Base):
    id: int
    username: str
    email: str
    password_hash: str
    role: UserRole  # SUPERADMIN, SCHOOLADMIN, TEACHER, STUDENT
    is_active: bool
    kundelik_id: Optional[str]
    school_id: Optional[int]
```

#### 2. **School (Школа)**
```python
class School(Base):
    id: int
    name: str
    city: str
    country: str
    contact_email: str
    contact_phone: str
    logo_url: Optional[str]
    created_at: datetime
```

#### 3. **Classroom (Класс)**
```python
class Classroom(Base):
    id: int
    grade: int  # 1-12
    letter: str  # A, B, C, D, E
    language: str  # kz, ru, en
    school_id: int
    created_at: datetime
```

#### 4. **Course (Курс)**
```python
class Course(Base):
    id: int
    course_code: str  # MATH1, KZ1, etc.
    name: str
    description: Optional[str]
    grade: int  # 1-12
    created_at: datetime
```

#### 5. **SubjectGroup (Связь курс-класс-учитель)**
```python
class SubjectGroup(Base):
    id: int
    course_id: int
    classroom_id: int
    teacher_id: int
    created_at: datetime
```

#### 6. **Assignment (Задание)**
```python
class Assignment(Base):
    id: int
    course_id: int
    teacher_id: int
    title: str
    description: Optional[str]
    due_at: datetime
    created_at: datetime
```

#### 7. **Submission (Отправка задания)**
```python
class Submission(Base):
    id: int
    assignment_id: int
    student_id: int
    text: Optional[str]
    file_url: Optional[str]
    submitted_at: datetime
```

#### 8. **Grade (Оценка)**
```python
class Grade(Base):
    id: int
    submission_id: int
    teacher_id: int
    grade_value: int  # 0-100
    feedback: Optional[str]
    created_at: datetime
```

#### 9. **CourseSection (Секция курса)**
```python
class CourseSection(Base):
    id: int
    course_id: int
    title: str
    position: int
    created_at: datetime
```

#### 10. **Resource (Ресурс)**
```python
class Resource(Base):
    id: int
    course_section_id: int
    type: ResourceType  # FILE, LINK
    title: str
    description: Optional[str]
    url: Optional[str]
    position: int
    created_at: datetime
```

## 🔐 Система аутентификации

### Роли пользователей

1. **SUPERADMIN** - Полный доступ ко всем функциям
2. **SCHOOLADMIN** - Управление школой и пользователями
3. **TEACHER** - Управление курсами, заданиями, оценивание
4. **STUDENT** - Просмотр курсов, отправка заданий

### JWT токены

- **Access Token** - для аутентификации API запросов (15 минут)
- **Refresh Token** - для обновления access token (7 дней)

### Пример аутентификации

```python
# Вход в систему
POST /v1/auth/login
{
    "username": "teacher1",
    "password": "password123"
}

# Ответ
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "user": {
        "id": 1,
        "username": "teacher1",
        "email": "teacher@school.kz",
        "role": "TEACHER"
    }
}
```

## 📚 API эндпоинты

### Аутентификация

| Метод | Эндпоинт | Описание | Роли |
|-------|----------|----------|------|
| POST | `/v1/auth/login` | Вход в систему | Все |
| POST | `/v1/auth/refresh` | Обновление токена | Все |
| POST | `/v1/auth/logout` | Выход из системы | Все |
| GET | `/v1/auth/me` | Текущий пользователь | Все |

### Управление школами

| Метод | Эндпоинт | Описание | Роли |
|-------|----------|----------|------|
| POST | `/v1/schools/` | Создание школы | SUPERADMIN |
| GET | `/v1/schools/` | Список школ | SUPERADMIN, SCHOOLADMIN |
| GET | `/v1/schools/{id}` | Получение школы | SUPERADMIN, SCHOOLADMIN |
| PUT | `/v1/schools/{id}` | Обновление школы | SUPERADMIN, SCHOOLADMIN |
| DELETE | `/v1/schools/{id}` | Удаление школы | SUPERADMIN |

### Управление классами

| Метод | Эндпоинт | Описание | Роли |
|-------|----------|----------|------|
| POST | `/v1/classrooms/` | Создание класса | SCHOOLADMIN |
| POST | `/v1/classrooms/bulk` | Массовое создание классов | SCHOOLADMIN |
| GET | `/v1/classrooms/` | Список классов | SCHOOLADMIN, TEACHER |
| GET | `/v1/classrooms/{id}` | Получение класса | SCHOOLADMIN, TEACHER |
| PUT | `/v1/classrooms/{id}` | Обновление класса | SCHOOLADMIN |
| DELETE | `/v1/classrooms/{id}` | Удаление класса | SCHOOLADMIN |

### Управление курсами

| Метод | Эндпоинт | Описание | Роли |
|-------|----------|----------|------|
| POST | `/v1/courses/` | Создание курса | SCHOOLADMIN |
| POST | `/v1/courses/bulk` | Массовое создание курсов | SCHOOLADMIN |
| GET | `/v1/courses/` | Список курсов | Все |
| GET | `/v1/courses/{id}` | Получение курса | Все |
| PUT | `/v1/courses/{id}` | Обновление курса | SCHOOLADMIN |
| DELETE | `/v1/courses/{id}` | Удаление курса | SCHOOLADMIN |

### Управление пользователями

| Метод | Эндпоинт | Описание | Роли |
|-------|----------|----------|------|
| POST | `/v1/admin/users` | Создание пользователя | SUPERADMIN, SCHOOLADMIN |
| GET | `/v1/admin/users` | Список пользователей | SUPERADMIN, SCHOOLADMIN |
| GET | `/v1/admin/users/{id}` | Получение пользователя | SUPERADMIN, SCHOOLADMIN |
| PUT | `/v1/admin/users/{id}` | Обновление пользователя | SUPERADMIN, SCHOOLADMIN |
| DELETE | `/v1/admin/users/{id}` | Удаление пользователя | SUPERADMIN, SCHOOLADMIN |

### Управление заданиями

| Метод | Эндпоинт | Описание | Роли |
|-------|----------|----------|------|
| POST | `/v1/assignments/` | Создание задания | TEACHER |
| GET | `/v1/assignments/` | Список заданий | TEACHER, STUDENT |
| GET | `/v1/assignments/{id}` | Получение задания | TEACHER, STUDENT |
| PUT | `/v1/assignments/{id}` | Обновление задания | TEACHER |
| DELETE | `/v1/assignments/{id}` | Удаление задания | TEACHER |

### Отправка заданий

| Метод | Эндпоинт | Описание | Роли |
|-------|----------|----------|------|
| POST | `/v1/submissions/` | Отправка задания | STUDENT |
| GET | `/v1/submissions/` | Список отправок | STUDENT |
| GET | `/v1/submissions/{id}` | Получение отправки | STUDENT, TEACHER |
| PUT | `/v1/submissions/{id}` | Обновление отправки | STUDENT |

### Оценивание

| Метод | Эндпоинт | Описание | Роли |
|-------|----------|----------|------|
| POST | `/v1/grades/` | Создание оценки | TEACHER |
| GET | `/v1/grades/` | Список оценок | TEACHER, STUDENT |
| GET | `/v1/grades/{id}` | Получение оценки | TEACHER, STUDENT |
| PUT | `/v1/grades/{id}` | Обновление оценки | TEACHER |

## 👥 Роли и права доступа

### SUPERADMIN
- ✅ Полный доступ ко всем функциям
- ✅ Управление школами
- ✅ Создание суперадминов и школьных админов
- ✅ Просмотр всех данных

### SCHOOLADMIN
- ✅ Управление школой
- ✅ Создание классов и курсов
- ✅ Создание учителей и студентов
- ✅ Просмотр отчетов школы

### TEACHER
- ✅ Создание заданий для своих курсов
- ✅ Создание секций курса
- ✅ Добавление ресурсов к секциям
- ✅ Оценивание заданий студентов
- ✅ Просмотр своих курсов и классов

### STUDENT
- ✅ Просмотр своих курсов
- ✅ Отправка заданий
- ✅ Просмотр оценок
- ✅ Просмотр ресурсов курса

## 🧪 Тестирование

### Запуск тестов

```bash
# Упрощенный тест основных функций
python simple_test.py

# Полный тест всех функций
python final_test.py

# Запуск сервера для тестирования
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Примеры тестов

#### 1. Создание школы
```python
import requests

# Вход в систему
login_data = {
    "username": "superadmin",
    "password": "superadmin"
}
response = requests.post("http://localhost:8000/v1/auth/login", json=login_data)
token = response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Создание школы
school_data = {
    "name": "Школа №1",
    "city": "Алматы",
    "country": "Казахстан",
    "contact_email": "school1@example.kz",
    "contact_phone": "+7 777 123 4567"
}
response = requests.post("http://localhost:8000/v1/schools/", json=school_data, headers=headers)
print(response.json())
```

#### 2. Массовое создание классов
```python
# Создание классов для всех классов (1-12) с буквами A-E
bulk_data = {
    "school_id": 1,
    "language": "kz",
    "grades": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    "letters_per_grade": 5
}
response = requests.post("http://localhost:8000/v1/classrooms/bulk", json=bulk_data, headers=headers)
print(f"Создано {len(response.json())} классов")
```

#### 3. Создание студентов с дефолтным паролем
```python
# Массовое создание студентов
students_data = {
    "classroom_id": 1,
    "students": [
        {"first_name": "Айдар", "last_name": "Ахметов", "email": "aidar@student.kz"},
        {"first_name": "Айша", "last_name": "Бекова", "email": "aisha@student.kz"},
        {"first_name": "Данияр", "last_name": "Касымов", "email": "daniyar@student.kz"}
    ]
}
response = requests.post("http://localhost:8000/v1/classroom_users/bulk-create-students", 
                        json=students_data, headers=headers)
print(f"Создано {len(response.json())} студентов с паролем 'qwerty123'")
```

#### 4. Создание задания
```python
# Вход как учитель
teacher_login = {"username": "teacher1", "password": "teacher123"}
teacher_response = requests.post("http://localhost:8000/v1/auth/login", json=teacher_login)
teacher_token = teacher_response.json()["access_token"]
teacher_headers = {"Authorization": f"Bearer {teacher_token}"}

# Создание задания
assignment_data = {
    "course_id": 1,
    "title": "Сложение и вычитание",
    "description": "Решите примеры на сложение и вычитание в пределах 10",
    "due_at": "2025-09-21T23:59:59"
}
response = requests.post("http://localhost:8000/v1/assignments/", 
                        json=assignment_data, headers=teacher_headers)
print(response.json())
```

## 📖 Примеры использования

### Сценарий 1: Настройка школы

```python
# 1. Создание школы
school = create_school("Школа №1", "Алматы", "Казахстан")

# 2. Массовое создание классов
classrooms = create_classrooms_bulk(school.id, grades=[1,2,3,4,5], letters_per_grade=2)

# 3. Создание курсов
courses = create_courses_bulk([
    {"course_code": "MATH1", "name": "Математика 1 класс", "grade": 1},
    {"course_code": "KZ1", "name": "Қазақ тілі 1 сынып", "grade": 1},
    {"course_code": "RUS1", "name": "Русский язык 1 класс", "grade": 1}
])

# 4. Создание учителей
teachers = create_teachers([
    {"username": "math_teacher", "email": "math@school.kz", "role": "teacher"},
    {"username": "kz_teacher", "email": "kz@school.kz", "role": "teacher"}
])

# 5. Создание студентов
students = create_students_bulk(classroom_id=1, students=[
    {"first_name": "Айдар", "last_name": "Ахметов", "email": "aidar@student.kz"},
    {"first_name": "Айша", "last_name": "Бекова", "email": "aisha@student.kz"}
])
```

### Сценарий 2: Настройка курса

```python
# 1. Создание связи курс-класс-учитель
subject_group = create_subject_group(course_id=1, classroom_id=1, teacher_id=1)

# 2. Создание секций курса
sections = create_course_sections(course_id=1, sections=[
    {"title": "Числа от 1 до 10", "position": 1},
    {"title": "Сложение", "position": 2},
    {"title": "Вычитание", "position": 3}
])

# 3. Добавление ресурсов к секциям
resources = create_resources(section_id=1, resources=[
    {"type": "link", "title": "Видео урок", "url": "https://youtube.com/watch?v=example"},
    {"type": "file", "title": "Презентация", "url": "/files/presentation.pdf"}
])
```

### Сценарий 3: Работа с заданиями

```python
# 1. Создание задания учителем
assignment = create_assignment(
    course_id=1,
    title="Домашнее задание",
    description="Решите примеры на сложение",
    due_at="2025-09-21T23:59:59"
)

# 2. Отправка задания студентом
submission = submit_assignment(
    assignment_id=assignment.id,
    text="Я решил все примеры! 2+3=5, 7-2=5"
)

# 3. Оценивание учителем
grade = create_grade(
    submission_id=submission.id,
    grade_value=85,
    feedback="Отличная работа!"
)
```

## 🔧 Конфигурация

### Переменные окружения

```bash
# База данных
DATABASE_URL=sqlite:///./data/dev.db

# JWT секреты
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:8080"]

# Файловое хранилище
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=10485760  # 10MB
```

### Настройка базы данных

```python
# Для разработки (SQLite)
DATABASE_URL = "sqlite:///./data/dev.db"

# Для продакшена (PostgreSQL)
DATABASE_URL = "postgresql://user:password@localhost/school_db"
```

## 📝 Логирование

### Настройка логирования

```python
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
```

### Уровни логирования

- **DEBUG** - Детальная информация для отладки
- **INFO** - Общая информация о работе системы
- **WARNING** - Предупреждения о потенциальных проблемах
- **ERROR** - Ошибки, которые не останавливают работу
- **CRITICAL** - Критические ошибки, останавливающие работу

## 🚀 Развертывание

### 🐳 Docker развертывание (SQLite)

```bash
# Простой запуск с SQLite
docker-compose up --build

# Запуск в фоновом режиме
docker-compose up -d --build

# Остановка
docker-compose down

# Просмотр логов
docker-compose logs -f app
```

### 📁 Структура Docker

```
future-school-backend/
├── Dockerfile              # Образ приложения
├── docker-compose.yml      # Конфигурация контейнеров
├── .dockerignore           # Исключения для Docker
└── scripts/
    └── create_superadmin.py # Скрипт создания админа
```

### 🔧 Конфигурация Docker

**Dockerfile:**
- Базовый образ: Python 3.10-slim
- Автоматическая установка зависимостей
- Применение миграций при запуске
- Порт: 8000

**docker-compose.yml:**
- Сервис: `app`
- База данных: SQLite (файл)
- Volumes: `./data` и `./uploads`
- Переменные окружения для JWT

### 🗄️ База данных

По умолчанию используется SQLite:
- Файл: `./data/dev.db`
- Автоматически создается при первом запуске
- Миграции применяются автоматически
- Данные сохраняются в volume

### 🔐 Доступ к приложению

После запуска Docker:
- **API:** http://localhost:8000
- **Документация:** http://localhost:8000/docs
- **Суперадмин:** `superadmin` / `superadmin`

### 📊 Мониторинг

```bash
# Статус контейнеров
docker-compose ps

# Логи приложения
docker-compose logs app

# Логи в реальном времени
docker-compose logs -f app

# Вход в контейнер
docker-compose exec app bash
```

### 🔄 Обновление

```bash
# Пересборка и перезапуск
docker-compose up --build

# Только перезапуск
docker-compose restart

# Очистка (удаление контейнеров и образов)
docker-compose down --rmi all
```

### Nginx конфигурация

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/static/files/;
    }
}
```

## 📊 Мониторинг и метрики

### Health Check

```python
# Проверка состояния системы
GET /health
{
    "status": "healthy",
    "database": "connected",
    "timestamp": "2025-09-14T19:30:00Z"
}
```

### Метрики производительности

- Время ответа API
- Количество запросов в секунду
- Использование памяти
- Количество активных соединений с БД

## 🔒 Безопасность

### Рекомендации по безопасности

1. **Используйте HTTPS в продакшене**
2. **Регулярно обновляйте зависимости**
3. **Используйте сильные пароли**
4. **Ограничивайте доступ к API**
5. **Логируйте все действия пользователей**
6. **Регулярно делайте резервные копии**

### Аудит безопасности

```python
# Логирование действий пользователей
@router.post("/sensitive-action")
async def sensitive_action(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Логируем действие
    logger.info(f"User {current_user.id} performed sensitive action")
    
    # Выполняем действие
    return {"status": "success"}
```

## 🤝 Вклад в проект

### Как внести вклад

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Добавьте тесты
5. Создайте Pull Request

### Стандарты кода

- Используйте PEP 8
- Добавляйте docstrings для функций
- Покрывайте код тестами
- Обновляйте документацию

## 📞 Поддержка

### Получение помощи

- **Документация API:** http://localhost:8000/docs
- **Issues:** Создайте issue в GitHub
- **Email:** support@school-system.com

### Часто задаваемые вопросы

**Q: Как создать суперадмина?**
A: Используйте скрипт `python scripts/create_superadmin.py`

**Q: Как изменить пароль пользователя?**
A: Используйте API `PUT /v1/admin/users/{id}` с новым паролем

**Q: Как экспортировать данные?**
A: Используйте API эндпоинты для получения данных в JSON формате

**Q: Как настроить уведомления?**
A: Система поддерживает webhook'и для интеграции с внешними сервисами

---

## 🎉 Заключение

Система управления школой предоставляет полный набор инструментов для управления образовательным процессом. Она построена с использованием современных технологий и следует лучшим практикам разработки.

**Основные преимущества:**
- ✅ Полная функциональность
- ✅ Масштабируемость
- ✅ Безопасность
- ✅ Простота использования
- ✅ Гибкость настройки

**Система готова к использованию в продакшене!** 🚀

---

*Документация обновлена: 14 сентября 2025*
