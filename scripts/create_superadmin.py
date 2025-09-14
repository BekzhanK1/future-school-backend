#!/usr/bin/env python3
"""
Скрипт для создания суперадмина
"""

import asyncio
import sys
import os

# Добавляем корневую директорию в путь
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import async_session
from app.models.user import User, UserRole
from app.core.security import get_password_hash


async def create_superadmin():
    """Создает суперадмина если его еще нет"""
    
    async with async_session() as db:
        # Проверяем, есть ли уже суперадмин
        existing_admin = await db.execute(
            "SELECT id FROM users WHERE role = 'SUPERADMIN' LIMIT 1"
        )
        if existing_admin.fetchone():
            print("✅ Суперадмин уже существует")
            return
        
        # Создаем суперадмина
        superadmin = User(
            username="superadmin",
            email="admin@school.kz",
            password_hash=get_password_hash("superadmin"),
            role=UserRole.SUPERADMIN,
            is_active=True
        )
        
        db.add(superadmin)
        await db.commit()
        await db.refresh(superadmin)
        
        print("✅ Суперадмин создан успешно!")
        print(f"   Username: superadmin")
        print(f"   Password: superadmin")
        print(f"   Email: admin@school.kz")


if __name__ == "__main__":
    asyncio.run(create_superadmin())
