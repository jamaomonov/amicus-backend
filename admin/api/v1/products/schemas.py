from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    """Базовая схема для продукта"""
    name: str
    description: Optional[str] = None
    image: Optional[str] = None
    is_active: bool = True
    category_id: int = Field(..., gt=0, description="ID категории (должен быть больше 0)")


class ProductCreate(ProductBase):
    """Схема для создания продукта"""
    pass


class ProductUpdate(BaseModel):
    """Схема для обновления продукта"""
    name: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    is_active: Optional[bool] = None
    category_id: Optional[int] = Field(None, gt=0, description="ID категории (должен быть больше 0)")


class FileInProduct(BaseModel):
    """Схема файла в продукте"""
    id: int
    name: str
    path: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductResponse(ProductBase):
    """Схема ответа продукта"""
    id: int
    created_at: datetime
    updated_at: datetime
    files: List[FileInProduct] = []

    model_config = ConfigDict(from_attributes=True)


class ProductListResponse(BaseModel):
    """Схема для списка продуктов"""
    items: list[ProductResponse]
    total: int

