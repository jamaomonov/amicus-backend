from typing import Optional
from fastapi import APIRouter, HTTPException, status, Query, UploadFile, File as FastAPIFile

from admin.api.v1.dependencies import DBSession
from admin.api.v1.utils.file_utils import save_product_file, delete_product_file
from admin.api.v1.products.crud import product_crud
from .crud import file_crud
from .schemas import (
    FileCreate,
    FileUpdate,
    FileResponse,
    FileListResponse,
    FileUploadResponse
)

router = APIRouter(prefix="/files", tags=["Files"])


@router.post(
    "/",
    response_model=FileResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать файл"
)
async def create_file(
    file_in: FileCreate,
    session: DBSession
):
    """Создать новый файл"""
    return await file_crud.create(session, file_in)


@router.get(
    "/",
    response_model=FileListResponse,
    summary="Получить список файлов"
)
async def get_files(
    session: DBSession,
    skip: int = Query(0, ge=0, description="Количество пропускаемых записей"),
    limit: int = Query(100, ge=1, le=100, description="Максимальное количество записей"),
    product_id: Optional[int] = Query(None, description="Фильтр по продукту")
):
    """Получить список всех файлов с пагинацией и фильтрацией"""
    files, total = await file_crud.get_all(
        session,
        skip=skip,
        limit=limit,
        product_id=product_id
    )
    return FileListResponse(items=files, total=total)


@router.get(
    "/{file_id}",
    response_model=FileResponse,
    summary="Получить файл по ID"
)
async def get_file(
    file_id: int,
    session: DBSession
):
    """Получить файл по ID"""
    file = await file_crud.get_by_id(session, file_id)
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Файл с ID {file_id} не найден"
        )
    return file


@router.patch(
    "/{file_id}",
    response_model=FileResponse,
    summary="Обновить файл"
)
async def update_file(
    file_id: int,
    file_update: FileUpdate,
    session: DBSession
):
    """Обновить файл"""
    file = await file_crud.get_by_id(session, file_id)
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Файл с ID {file_id} не найден"
        )
    return await file_crud.update(session, file, file_update)


@router.delete(
    "/{file_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить файл"
)
async def delete_file(
    file_id: int,
    session: DBSession
):
    """Удалить файл"""
    file = await file_crud.get_by_id(session, file_id)
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Файл с ID {file_id} не найден"
        )
    
    # Удаляем файл из файловой системы
    if file.path:
        delete_product_file(file.path)
    
    await file_crud.delete(session, file)


@router.post(
    "/upload",
    response_model=FileUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Загрузить файл для продукта"
)
async def upload_product_file(
    product_id: int,
    session: DBSession,
    file: UploadFile = FastAPIFile(..., description="Файл продукта (PDF, Word, Excel и т.д.)")
):
    """
    Загрузить файл для продукта.
    Файл будет сохранен в директории /files/{product_name}/
    
    Поддерживаемые форматы: PDF, DOC, DOCX, XLS, XLSX, PPT, PPTX, TXT, CSV, ODT, ODS
    """
    # Проверяем существование продукта
    product = await product_crud.get_by_id(session, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Продукт с ID {product_id} не найден"
        )
    
    # Сохраняем файл в файловую систему
    file_path = await save_product_file(file, product.name)
    
    # Создаем запись в БД
    file_create = FileCreate(
        name=file.filename or "unknown",
        path=file_path,
        product_id=product_id
    )
    
    db_file = await file_crud.create(session, file_create)
    
    return FileUploadResponse(
        id=db_file.id,
        name=db_file.name,
        path=db_file.path,
        product_id=db_file.product_id,
        message=f"Файл успешно загружен в /files/{product.name}/"
    )

