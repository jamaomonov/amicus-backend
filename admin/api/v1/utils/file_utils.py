import os
import uuid
from pathlib import Path
from typing import Optional
from fastapi import UploadFile, HTTPException, status

from core.config import IMAGES_DIR, FILES_DIR


# Разрешенные расширения файлов
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"}
ALLOWED_DOCUMENT_EXTENSIONS = {
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", 
    ".ppt", ".pptx", ".txt", ".csv", ".odt", ".ods"
}


def get_file_extension(filename: str) -> str:
    """Получить расширение файла"""
    return Path(filename).suffix.lower()


def validate_file_extension(filename: str, allowed_extensions: set) -> bool:
    """Проверить расширение файла"""
    extension = get_file_extension(filename)
    return extension in allowed_extensions


async def save_upload_file(
    file: UploadFile,
    directory: Path,
    subdirectory: Optional[str] = None,
    allowed_extensions: Optional[set] = None
) -> tuple[str, str]:
    """
    Сохранить загруженный файл
    
    Args:
        file: Загруженный файл
        directory: Основная директория для сохранения
        subdirectory: Поддиректория (например, название продукта)
        allowed_extensions: Разрешенные расширения файлов
    
    Returns:
        tuple[str, str]: (путь к файлу относительно directory, полный путь)
    
    Raises:
        HTTPException: Если файл не прошел валидацию
    """
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Имя файла не указано"
        )
    
    # Валидация расширения
    if allowed_extensions:
        if not validate_file_extension(file.filename, allowed_extensions):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Недопустимый тип файла. Разрешены: {', '.join(allowed_extensions)}"
            )
    
    # Получаем расширение файла
    extension = get_file_extension(file.filename)
    
    # Генерируем уникальное имя файла
    unique_filename = f"{uuid.uuid4()}{extension}"
    
    # Определяем директорию для сохранения
    save_directory = directory
    if subdirectory:
        save_directory = directory / subdirectory
        save_directory.mkdir(parents=True, exist_ok=True)
    
    # Полный путь к файлу
    file_path = save_directory / unique_filename
    
    # Сохраняем файл
    try:
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при сохранении файла: {str(e)}"
        )
    
    # Возвращаем относительный путь и полный путь
    if subdirectory:
        relative_path = f"{subdirectory}/{unique_filename}"
    else:
        relative_path = unique_filename
    
    return relative_path, str(file_path)


async def save_product_image(file: UploadFile) -> str:
    """
    Сохранить изображение продукта в /images/
    
    Returns:
        str: Путь к файлу для сохранения в БД (например, "uuid.jpg")
    """
    relative_path, _ = await save_upload_file(
        file=file,
        directory=IMAGES_DIR,
        allowed_extensions=ALLOWED_IMAGE_EXTENSIONS
    )
    return relative_path


async def save_product_file(file: UploadFile, product_name: str) -> str:
    """
    Сохранить файл продукта в /files/{product_name}/
    
    Args:
        file: Загруженный файл
        product_name: Название продукта (используется как имя поддиректории)
    
    Returns:
        str: Путь к файлу для сохранения в БД (например, "product_name/uuid.pdf")
    """
    # Очищаем название продукта от недопустимых символов
    clean_product_name = "".join(
        c if c.isalnum() or c in (' ', '-', '_') else '_' 
        for c in product_name
    ).strip().replace(' ', '_')
    
    relative_path, _ = await save_upload_file(
        file=file,
        directory=FILES_DIR,
        subdirectory=clean_product_name,
        allowed_extensions=ALLOWED_DOCUMENT_EXTENSIONS
    )
    return relative_path


def delete_file(file_path: str, base_directory: Path) -> bool:
    """
    Удалить файл из файловой системы
    
    Args:
        file_path: Относительный путь к файлу
        base_directory: Базовая директория
    
    Returns:
        bool: True если файл успешно удален, False если файл не найден
    """
    try:
        full_path = base_directory / file_path
        if full_path.exists():
            full_path.unlink()
            
            # Удаляем пустую поддиректорию если она есть
            parent_dir = full_path.parent
            if parent_dir != base_directory and not any(parent_dir.iterdir()):
                parent_dir.rmdir()
            
            return True
        return False
    except Exception:
        return False


def delete_product_image(image_path: str) -> bool:
    """Удалить изображение продукта"""
    return delete_file(image_path, IMAGES_DIR)


def delete_product_file(file_path: str) -> bool:
    """Удалить файл продукта"""
    return delete_file(file_path, FILES_DIR)

