from typing import Optional
from fastapi import APIRouter, HTTPException, status, Query, UploadFile, File

from admin.api.v1.dependencies import DBSession
from admin.api.v1.utils.file_utils import save_product_image, delete_product_image
from admin.api.v1.categories.crud import category_crud
from .crud import product_crud
from .schemas import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductListResponse
)

router = APIRouter(prefix="/products", tags=["Products"])


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать продукт"
)
async def create_product(
    product_in: ProductCreate,
    session: DBSession
):
    """Создать новый продукт"""
    # Проверяем существование категории
    category = await category_crud.get_by_id(session, product_in.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категория с ID {product_in.category_id} не найдена"
        )
    return await product_crud.create(session, product_in)


@router.get(
    "/",
    response_model=ProductListResponse,
    summary="Получить список продуктов"
)
async def get_products(
    session: DBSession,
    skip: int = Query(0, ge=0, description="Количество пропускаемых записей"),
    limit: int = Query(100, ge=1, le=100, description="Максимальное количество записей"),
    category_id: Optional[int] = Query(None, description="Фильтр по категории"),
    is_active: Optional[bool] = Query(None, description="Фильтр по активности")
):
    """Получить список всех продуктов с пагинацией и фильтрацией"""
    products, total = await product_crud.get_all(
        session,
        skip=skip,
        limit=limit,
        category_id=category_id,
        is_active=is_active
    )
    return ProductListResponse(items=products, total=total)


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Получить продукт по ID"
)
async def get_product(
    product_id: int,
    session: DBSession
):
    """Получить продукт по ID"""
    product = await product_crud.get_by_id(session, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Продукт с ID {product_id} не найден"
        )
    return product


@router.patch(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Обновить продукт"
)
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    session: DBSession
):
    """Обновить продукт"""
    product = await product_crud.get_by_id(session, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Продукт с ID {product_id} не найден"
        )
    
    # Проверяем существование категории, если она обновляется
    if product_update.category_id is not None:
        category = await category_crud.get_by_id(session, product_update.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Категория с ID {product_update.category_id} не найдена"
            )
    
    return await product_crud.update(session, product, product_update)


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить продукт"
)
async def delete_product(
    product_id: int,
    session: DBSession
):
    """Удалить продукт"""
    product = await product_crud.get_by_id(session, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Продукт с ID {product_id} не найден"
        )
    
    # Удаляем изображение продукта если оно есть
    if product.image:
        delete_product_image(product.image)
    
    await product_crud.delete(session, product)


@router.post(
    "/{product_id}/upload-image",
    response_model=ProductResponse,
    summary="Загрузить изображение продукта"
)
async def upload_product_image(
    product_id: int,
    session: DBSession,
    file: UploadFile = File(..., description="Изображение продукта")
):
    """
    Загрузить изображение для продукта.
    Изображение будет сохранено в директории /images/
    
    Поддерживаемые форматы: JPG, JPEG, PNG, GIF, WEBP, SVG
    """
    # Проверяем существование продукта
    product = await product_crud.get_by_id(session, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Продукт с ID {product_id} не найден"
        )
    
    # Удаляем старое изображение если оно есть
    if product.image:
        delete_product_image(product.image)
    
    # Сохраняем новое изображение
    image_path = await save_product_image(file)
    
    # Обновляем путь к изображению в БД
    product.image = image_path
    await session.commit()
    
    # Заново получаем продукт с загруженными файлами
    updated_product = await product_crud.get_by_id(session, product_id)
    
    return updated_product

