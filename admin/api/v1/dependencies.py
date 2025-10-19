from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.db_helper import db_helper


async def get_db_session() -> AsyncSession:
    """
    Зависимость для получения сессии базы данных
    """
    async for session in db_helper.session_dependency():
        yield session


# Аннотация для упрощения использования в роутах
DBSession = Annotated[AsyncSession, Depends(get_db_session)]

