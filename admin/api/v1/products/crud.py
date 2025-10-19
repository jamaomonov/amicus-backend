from typing import Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.models import Product
from .schemas import ProductCreate, ProductUpdate


class ProductCRUD:
    """CRUD операции для продуктов"""

    @staticmethod
    async def create(session: AsyncSession, product_in: ProductCreate) -> Product:
        """Создать продукт"""
        product = Product(**product_in.model_dump())
        session.add(product)
        await session.commit()
        await session.refresh(product)
        return product

    @staticmethod
    async def get_by_id(session: AsyncSession, product_id: int) -> Optional[Product]:
        """Получить продукт по ID"""
        result = await session.execute(
            select(Product).where(Product.id == product_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        category_id: Optional[int] = None,
        is_active: Optional[bool] = None
    ) -> tuple[list[Product], int]:
        """Получить список всех продуктов с пагинацией и фильтрацией"""
        # Базовый запрос
        query = select(Product)
        count_query = select(func.count(Product.id))
        
        # Применяем фильтры
        if category_id is not None:
            query = query.where(Product.category_id == category_id)
            count_query = count_query.where(Product.category_id == category_id)
        
        if is_active is not None:
            query = query.where(Product.is_active == is_active)
            count_query = count_query.where(Product.is_active == is_active)
        
        # Получаем общее количество
        count_result = await session.execute(count_query)
        total = count_result.scalar_one()
        
        # Получаем продукты с пагинацией
        query = query.offset(skip).limit(limit).order_by(Product.id.desc())
        result = await session.execute(query)
        products = result.scalars().all()
        return list(products), total

    @staticmethod
    async def update(
        session: AsyncSession,
        product: Product,
        product_update: ProductUpdate
    ) -> Product:
        """Обновить продукт"""
        update_data = product_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)
        
        await session.commit()
        await session.refresh(product)
        return product

    @staticmethod
    async def delete(session: AsyncSession, product: Product) -> None:
        """Удалить продукт"""
        await session.delete(product)
        await session.commit()


product_crud = ProductCRUD()

