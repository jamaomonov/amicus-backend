from typing import Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.models import Category
from .schemas import CategoryCreate, CategoryUpdate


class CategoryCRUD:
    """CRUD операции для категорий"""

    @staticmethod
    async def create(session: AsyncSession, category_in: CategoryCreate) -> Category:
        """Создать категорию"""
        category = Category(**category_in.model_dump())
        session.add(category)
        await session.commit()
        await session.refresh(category)
        return category

    @staticmethod
    async def get_by_id(session: AsyncSession, category_id: int) -> Optional[Category]:
        """Получить категорию по ID"""
        result = await session.execute(
            select(Category).where(Category.id == category_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[list[Category], int]:
        """Получить список всех категорий с пагинацией"""
        # Получаем общее количество
        count_result = await session.execute(select(func.count(Category.id)))
        total = count_result.scalar_one()
        
        # Получаем категории с пагинацией
        result = await session.execute(
            select(Category)
            .offset(skip)
            .limit(limit)
            .order_by(Category.id.desc())
        )
        categories = result.scalars().all()
        return list(categories), total

    @staticmethod
    async def update(
        session: AsyncSession,
        category: Category,
        category_update: CategoryUpdate
    ) -> Category:
        """Обновить категорию"""
        update_data = category_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(category, field, value)
        
        await session.commit()
        await session.refresh(category)
        return category

    @staticmethod
    async def delete(session: AsyncSession, category: Category) -> None:
        """Удалить категорию"""
        await session.delete(category)
        await session.commit()


category_crud = CategoryCRUD()

