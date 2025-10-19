from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    """Базовая схема для продукта"""
    name: str
    description: Optional[str] = None
    image: str
    is_active: bool = True
    category_id: int


class ProductCreate(ProductBase):
    """Схема для создания продукта"""
    pass


class ProductUpdate(BaseModel):
    """Схема для обновления продукта"""
    name: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    is_active: Optional[bool] = None
    category_id: Optional[int] = None


class ProductResponse(ProductBase):
    """Схема ответа продукта"""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductListResponse(BaseModel):
    """Схема для списка продуктов"""
    items: list[ProductResponse]
    total: int

