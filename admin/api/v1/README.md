# Admin API v1

## Структура

Все CRUD API модули организованы по следующей структуре:

```
admin/api/v1/
├── dependencies.py          # Общие зависимости (DB сессия)
├── __init__.py             # Подключение всех роутеров
├── categories/             # Модуль категорий
│   ├── __init__.py
│   ├── schemas.py         # Pydantic схемы
│   ├── crud.py            # CRUD операции
│   └── routes.py          # API эндпоинты
├── products/              # Модуль продуктов
│   ├── __init__.py
│   ├── schemas.py
│   ├── crud.py
│   └── routes.py
└── files/                 # Модуль файлов
    ├── __init__.py
    ├── schemas.py
    ├── crud.py
    └── routes.py
```

## Доступные эндпоинты

### Categories (Категории)

**Base URL:** `/admin/api/v1/categories`

- `POST /` - Создать категорию
- `GET /` - Получить список категорий (с пагинацией)
- `GET /{category_id}` - Получить категорию по ID
- `PATCH /{category_id}` - Обновить категорию
- `DELETE /{category_id}` - Удалить категорию

**Параметры пагинации:**
- `skip` - количество пропускаемых записей (по умолчанию: 0)
- `limit` - максимальное количество записей (по умолчанию: 100, макс: 100)

### Products (Продукты)

**Base URL:** `/admin/api/v1/products`

- `POST /` - Создать продукт
- `GET /` - Получить список продуктов (с пагинацией и фильтрацией)
- `GET /{product_id}` - Получить продукт по ID
- `PATCH /{product_id}` - Обновить продукт
- `DELETE /{product_id}` - Удалить продукт
- `POST /{product_id}/upload-image` - **Загрузить изображение продукта**

**Параметры фильтрации:**
- `skip` - количество пропускаемых записей
- `limit` - максимальное количество записей
- `category_id` - фильтр по категории (опционально)
- `is_active` - фильтр по активности (опционально)

**Загрузка изображений:**
- Поддерживаемые форматы: JPG, JPEG, PNG, GIF, WEBP, SVG
- Изображения сохраняются в `/images/`
- Доступ: `http://localhost:8000/images/{filename}`

### Files (Файлы)

**Base URL:** `/admin/api/v1/files`

- `POST /` - Создать файл (вручную)
- `GET /` - Получить список файлов (с пагинацией и фильтрацией)
- `GET /{file_id}` - Получить файл по ID
- `PATCH /{file_id}` - Обновить файл
- `DELETE /{file_id}` - Удалить файл
- `POST /upload` - **Загрузить файл для продукта**

**Параметры фильтрации:**
- `skip` - количество пропускаемых записей
- `limit` - максимальное количество записей
- `product_id` - фильтр по продукту (опционально)

**Загрузка файлов:**
- Поддерживаемые форматы: PDF, DOC, DOCX, XLS, XLSX, PPT, PPTX, TXT, CSV, ODT, ODS
- Файлы сохраняются в `/files/{product_name}/`
- Доступ: `http://localhost:8000/files/{product_name}/{filename}`

## Примеры использования

### Создание категории

```bash
curl -X POST "http://localhost:8000/admin/api/v1/categories/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Электроника",
    "description": "Электронные товары"
  }'
```

### Создание продукта

```bash
curl -X POST "http://localhost:8000/admin/api/v1/products/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ноутбук",
    "description": "Мощный ноутбук",
    "image": "placeholder.jpg",
    "is_active": true,
    "category_id": 1
  }'
```

### Загрузка изображения для продукта

```bash
curl -X POST "http://localhost:8000/admin/api/v1/products/1/upload-image" \
  -F "file=@laptop.jpg"
```

### Загрузка файла для продукта

```bash
curl -X POST "http://localhost:8000/admin/api/v1/files/upload?product_id=1" \
  -F "file=@manual.pdf"
```

### Получение списка продуктов с фильтрацией

```bash
curl "http://localhost:8000/admin/api/v1/products/?category_id=1&is_active=true&skip=0&limit=10"
```

### Получение всех файлов продукта

```bash
curl "http://localhost:8000/admin/api/v1/files/?product_id=1"
```

## Документация API

Полная интерактивная документация доступна по адресу:
- Swagger UI: http://localhost:8000/admin/docs
- ReDoc: http://localhost:8000/admin/redoc

## Принципы чистого кода

1. **Разделение ответственности**: каждый модуль отвечает за свою сущность
2. **CRUD паттерн**: все операции с базой данных вынесены в отдельные CRUD классы
3. **Валидация данных**: использование Pydantic схем для валидации входных и выходных данных
4. **Async/await**: полностью асинхронная архитектура для максимальной производительности
5. **Dependency Injection**: использование FastAPI зависимостей для получения DB сессии
6. **Типизация**: все функции полностью типизированы
7. **Документация**: каждый эндпоинт имеет описание и summary

