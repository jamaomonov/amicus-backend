from typing import Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.models import File
from .schemas import FileCreate, FileUpdate


class FileCRUD:
    """CRUD операции для файлов"""

    @staticmethod
    async def create(session: AsyncSession, file_in: FileCreate) -> File:
        """Создать файл"""
        file = File(**file_in.model_dump())
        session.add(file)
        await session.commit()
        await session.refresh(file)
        return file

    @staticmethod
    async def get_by_id(session: AsyncSession, file_id: int) -> Optional[File]:
        """Получить файл по ID"""
        result = await session.execute(
            select(File).where(File.id == file_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        product_id: Optional[int] = None
    ) -> tuple[list[File], int]:
        """Получить список всех файлов с пагинацией и фильтрацией"""
        # Базовый запрос
        query = select(File)
        count_query = select(func.count(File.id))
        
        # Применяем фильтры
        if product_id is not None:
            query = query.where(File.product_id == product_id)
            count_query = count_query.where(File.product_id == product_id)
        
        # Получаем общее количество
        count_result = await session.execute(count_query)
        total = count_result.scalar_one()
        
        # Получаем файлы с пагинацией
        query = query.offset(skip).limit(limit).order_by(File.id.desc())
        result = await session.execute(query)
        files = result.scalars().all()
        return list(files), total

    @staticmethod
    async def update(
        session: AsyncSession,
        file: File,
        file_update: FileUpdate
    ) -> File:
        """Обновить файл"""
        update_data = file_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(file, field, value)
        
        await session.commit()
        await session.refresh(file)
        return file

    @staticmethod
    async def delete(session: AsyncSession, file: File) -> None:
        """Удалить файл"""
        await session.delete(file)
        await session.commit()


file_crud = FileCRUD()

