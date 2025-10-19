from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class CategoryBase(BaseModel):
    """Базовая схема для категории"""
    name: str
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    """Схема для создания категории"""
    pass


class CategoryUpdate(BaseModel):
    """Схема для обновления категории"""
    name: Optional[str] = None
    description: Optional[str] = None


class CategoryResponse(CategoryBase):
    """Схема ответа категории"""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CategoryListResponse(BaseModel):
    """Схема для списка категорий"""
    items: list[CategoryResponse]
    total: int

