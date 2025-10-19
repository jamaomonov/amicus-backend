from fastapi import APIRouter, HTTPException, status, Query

from admin.api.v1.dependencies import DBSession
from .crud import category_crud
from .schemas import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
    CategoryListResponse
)

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать категорию"
)
async def create_category(
    category_in: CategoryCreate,
    session: DBSession
):
    """Создать новую категорию"""
    return await category_crud.create(session, category_in)


@router.get(
    "/",
    response_model=CategoryListResponse,
    summary="Получить список категорий"
)
async def get_categories(
    session: DBSession,
    skip: int = Query(0, ge=0, description="Количество пропускаемых записей"),
    limit: int = Query(100, ge=1, le=100, description="Максимальное количество записей")
):
    """Получить список всех категорий с пагинацией"""
    categories, total = await category_crud.get_all(session, skip=skip, limit=limit)
    return CategoryListResponse(items=categories, total=total)


@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
    summary="Получить категорию по ID"
)
async def get_category(
    category_id: int,
    session: DBSession
):
    """Получить категорию по ID"""
    category = await category_crud.get_by_id(session, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категория с ID {category_id} не найдена"
        )
    return category


@router.patch(
    "/{category_id}",
    response_model=CategoryResponse,
    summary="Обновить категорию"
)
async def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    session: DBSession
):
    """Обновить категорию"""
    category = await category_crud.get_by_id(session, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категория с ID {category_id} не найдена"
        )
    return await category_crud.update(session, category, category_update)


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить категорию"
)
async def delete_category(
    category_id: int,
    session: DBSession
):
    """Удалить категорию"""
    category = await category_crud.get_by_id(session, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категория с ID {category_id} не найдена"
        )
    await category_crud.delete(session, category)

