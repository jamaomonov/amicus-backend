from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class FileBase(BaseModel):
    """Базовая схема для файла"""
    name: str
    path: str
    product_id: int


class FileCreate(FileBase):
    """Схема для создания файла"""
    pass


class FileUpdate(BaseModel):
    """Схема для обновления файла"""
    name: Optional[str] = None
    path: Optional[str] = None
    product_id: Optional[int] = None


class FileResponse(FileBase):
    """Схема ответа файла"""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FileListResponse(BaseModel):
    """Схема для списка файлов"""
    items: list[FileResponse]
    total: int


class FileUploadResponse(BaseModel):
    """Схема ответа при загрузке файла"""
    id: int
    name: str
    path: str
    product_id: int
    message: str

    model_config = ConfigDict(from_attributes=True)

