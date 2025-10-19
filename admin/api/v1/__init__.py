from fastapi import APIRouter

from .categories import router as categories_router
from .products import router as products_router
from .files import router as files_router

router = APIRouter()

# Подключаем все роутеры
router.include_router(categories_router)
router.include_router(products_router)
router.include_router(files_router)

__all__ = ["router"]

