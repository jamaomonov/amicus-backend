from fastapi import APIRouter
from .v1 import router as v1_router

router = APIRouter()

# Подключаем роутеры v1
router.include_router(v1_router)
