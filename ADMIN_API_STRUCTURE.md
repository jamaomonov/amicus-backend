# Структура Admin API

## Созданные модули

Для моделей **Category**, **Product** и **File** был создан полноценный CRUD API в директории `admin/api/v1/`.

### Общая структура

```
admin/api/v1/
├── dependencies.py              # Общие зависимости для всех модулей
├── __init__.py                  # Центральный роутер, объединяющий все модули
├── README.md                    # Подробная документация API
│
├── categories/                  # Модуль управления категориями
│   ├── __init__.py             # Экспорт роутера
│   ├── schemas.py              # Pydantic схемы (CategoryCreate, CategoryUpdate, CategoryResponse)
│   ├── crud.py                 # CRUD операции (CategoryCRUD)
│   └── routes.py               # API эндпоинты
│
├── products/                    # Модуль управления продуктами
│   ├── __init__.py             # Экспорт роутера
│   ├── schemas.py              # Pydantic схемы (ProductCreate, ProductUpdate, ProductResponse)
│   ├── crud.py                 # CRUD операции (ProductCRUD)
│   └── routes.py               # API эндпоинты
│
└── files/                       # Модуль управления файлами
    ├── __init__.py             # Экспорт роутера
    ├── schemas.py              # Pydantic схемы (FileCreate, FileUpdate, FileResponse)
    ├── crud.py                 # CRUD операции (FileCRUD)
    └── routes.py               # API эндпоинты
```

## Реализованные функции

### Для каждой модели созданы:

#### 1. **Schemas (Pydantic модели)**
- `Base` - базовые поля модели
- `Create` - схема для создания
- `Update` - схема для обновления (все поля опциональные)
- `Response` - схема ответа API
- `ListResponse` - схема для списков с пагинацией

#### 2. **CRUD операции**
- `create()` - создание записи
- `get_by_id()` - получение по ID
- `get_all()` - получение списка с пагинацией и фильтрацией
- `update()` - обновление записи
- `delete()` - удаление записи

#### 3. **API эндпоинты**
- `POST /` - создание
- `GET /` - список с пагинацией
- `GET /{id}` - получение по ID
- `PATCH /{id}` - обновление
- `DELETE /{id}` - удаление

## Особенности реализации

### 🎯 Чистый код
- **Разделение на слои**: routes → crud → models
- **Dependency Injection**: использование FastAPI dependencies
- **Типизация**: полная типизация всех функций
- **Документация**: docstrings и описания для всех эндпоинтов

### 🔄 Пагинация
Все эндпоинты получения списков поддерживают пагинацию:
- `skip` - количество пропускаемых записей (по умолчанию: 0)
- `limit` - максимальное количество записей (по умолчанию: 100, макс: 100)

### 🔍 Фильтрация

**Products:**
- `category_id` - фильтр по категории
- `is_active` - фильтр по активности

**Files:**
- `product_id` - фильтр по продукту

### ⚡ Асинхронность
Все операции полностью асинхронные с использованием:
- `AsyncSession` для работы с БД
- `async/await` для всех операций

### 🛡️ Обработка ошибок
- HTTP 404 - если запись не найдена
- HTTP 201 - успешное создание
- HTTP 204 - успешное удаление
- Понятные сообщения об ошибках на русском языке

## URL эндпоинтов

Все эндпоинты доступны по адресу: `http://localhost:8000/admin/api/v1/`

### Categories
- `POST /admin/api/v1/categories/`
- `GET /admin/api/v1/categories/`
- `GET /admin/api/v1/categories/{category_id}`
- `PATCH /admin/api/v1/categories/{category_id}`
- `DELETE /admin/api/v1/categories/{category_id}`

### Products
- `POST /admin/api/v1/products/`
- `GET /admin/api/v1/products/`
- `GET /admin/api/v1/products/{product_id}`
- `PATCH /admin/api/v1/products/{product_id}`
- `DELETE /admin/api/v1/products/{product_id}`

### Files
- `POST /admin/api/v1/files/`
- `GET /admin/api/v1/files/`
- `GET /admin/api/v1/files/{file_id}`
- `PATCH /admin/api/v1/files/{file_id}`
- `DELETE /admin/api/v1/files/{file_id}`

## Как использовать

### 1. Запуск сервера

```bash
cd /Users/macbook_uz/Projects/TipoProjects/amicus/backend
source venv/bin/activate
uvicorn main:app --reload
```

### 2. Интерактивная документация

После запуска сервера откройте браузер:
- **Swagger UI**: http://localhost:8000/admin/docs
- **ReDoc**: http://localhost:8000/admin/redoc

### 3. Примеры запросов

#### Создание категории
```bash
curl -X POST "http://localhost:8000/admin/api/v1/categories/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Электроника",
    "description": "Категория электронных товаров"
  }'
```

#### Создание продукта
```bash
curl -X POST "http://localhost:8000/admin/api/v1/products/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ноутбук Lenovo",
    "description": "Мощный ноутбук для работы",
    "image": "/static/images/laptop.jpg",
    "is_active": true,
    "category_id": 1
  }'
```

#### Получение списка продуктов
```bash
curl "http://localhost:8000/admin/api/v1/products/?skip=0&limit=10&category_id=1&is_active=true"
```

#### Обновление продукта
```bash
curl -X PATCH "http://localhost:8000/admin/api/v1/products/1" \
  -H "Content-Type: application/json" \
  -d '{
    "is_active": false
  }'
```

#### Удаление файла
```bash
curl -X DELETE "http://localhost:8000/admin/api/v1/files/1"
```

## Архитектурные решения

### 1. Общий dependencies.py
Все модули используют общий файл зависимостей для получения DB сессии:
```python
from admin.api.v1.dependencies import DBSession
```

### 2. CRUD паттерн
Все операции с БД вынесены в отдельные CRUD классы:
```python
category = await category_crud.create(session, category_in)
```

### 3. Pydantic модели
Строгая валидация данных на входе и выходе:
```python
class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
```

### 4. Централизованная регистрация роутеров
Все роутеры регистрируются в одном месте (`admin/api/v1/__init__.py`):
```python
router.include_router(categories_router)
router.include_router(products_router)
router.include_router(files_router)
```

## Связи между моделями

```
Category (1) ─── (N) Product (1) ─── (N) File
```

- Одна категория может содержать много продуктов
- Один продукт может содержать много файлов
- При удалении категории удаляются все связанные продукты (cascade)
- При удалении продукта удаляются все связанные файлы (cascade)

## Следующие шаги

1. ✅ Запустить сервер: `uvicorn main:app --reload`
2. ✅ Проверить документацию: http://localhost:8000/admin/docs
3. ✅ Протестировать все эндпоинты через Swagger UI
4. ⚠️ Добавить аутентификацию и авторизацию (при необходимости)
5. ⚠️ Добавить rate limiting (при необходимости)
6. ⚠️ Добавить логирование запросов (при необходимости)

## Заметки

- Все эндпоинты работают с базой данных PostgreSQL через SQLAlchemy
- Используется асинхронный драйвер для максимальной производительности
- Схемы автоматически валидируются Pydantic
- Документация API генерируется автоматически FastAPI
- Код полностью соответствует принципам чистой архитектуры

