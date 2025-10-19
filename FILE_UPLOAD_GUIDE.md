git# Руководство по загрузке файлов

## 📁 Структура хранения файлов

```
backend/
├── images/                    # Изображения продуктов
│   └── {uuid}.jpg            # Например: a1b2c3d4-e5f6-7890-abcd-ef1234567890.jpg
└── files/                     # Файлы продуктов (документы)
    └── {product_name}/        # Например: Laptop_Lenovo/
        └── {uuid}.pdf         # Например: b2c3d4e5-f6a7-8901-bcde-f12345678901.pdf
```

## 🖼️ Загрузка изображений для продуктов

### Эндпоинт
```
POST /admin/api/v1/products/{product_id}/upload-image
```

### Поддерживаемые форматы
- JPG / JPEG
- PNG
- GIF
- WEBP
- SVG

### Пример использования (cURL)

```bash
curl -X POST "http://localhost:8000/admin/api/v1/products/1/upload-image" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/image.jpg"
```

### Пример использования (Python)

```python
import requests

url = "http://localhost:8000/admin/api/v1/products/1/upload-image"
files = {"file": open("laptop.jpg", "rb")}

response = requests.post(url, files=files)
print(response.json())
```

### Пример ответа

```json
{
  "id": 1,
  "name": "Ноутбук Lenovo",
  "description": "Мощный ноутбук для работы",
  "image": "a1b2c3d4-e5f6-7890-abcd-ef1234567890.jpg",
  "is_active": true,
  "category_id": 1,
  "created_at": "2024-10-19T10:30:00",
  "updated_at": "2024-10-19T10:35:00"
}
```

### Доступ к изображению

После загрузки изображение доступно по адресу:
```
http://localhost:8000/images/{filename}
```

Например:
```
http://localhost:8000/images/a1b2c3d4-e5f6-7890-abcd-ef1234567890.jpg
```

## 📄 Загрузка файлов (документов) для продуктов

### Эндпоинт
```
POST /admin/api/v1/files/upload?product_id={product_id}
```

### Поддерживаемые форматы
- PDF (.pdf)
- Microsoft Word (.doc, .docx)
- Microsoft Excel (.xls, .xlsx)
- Microsoft PowerPoint (.ppt, .pptx)
- Text (.txt)
- CSV (.csv)
- OpenDocument (.odt, .ods)

### Пример использования (cURL)

```bash
curl -X POST "http://localhost:8000/admin/api/v1/files/upload?product_id=1" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/document.pdf"
```

### Пример использования (Python)

```python
import requests

url = "http://localhost:8000/admin/api/v1/files/upload"
params = {"product_id": 1}
files = {"file": open("manual.pdf", "rb")}

response = requests.post(url, params=params, files=files)
print(response.json())
```

### Пример ответа

```json
{
  "id": 5,
  "name": "manual.pdf",
  "path": "Laptop_Lenovo/b2c3d4e5-f6a7-8901-bcde-f12345678901.pdf",
  "product_id": 1,
  "message": "Файл успешно загружен в /files/Laptop_Lenovo/"
}
```

### Доступ к файлу

После загрузки файл доступен по адресу:
```
http://localhost:8000/files/{path}
```

Например:
```
http://localhost:8000/files/Laptop_Lenovo/b2c3d4e5-f6a7-8901-bcde-f12345678901.pdf
```

## 🔄 Полный цикл работы с продуктом

### 1. Создать категорию

```bash
curl -X POST "http://localhost:8000/admin/api/v1/categories/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ноутбуки",
    "description": "Категория ноутбуков"
  }'
```

Ответ:
```json
{
  "id": 1,
  "name": "Ноутбуки",
  "description": "Категория ноутбуков",
  "created_at": "2024-10-19T10:00:00",
  "updated_at": "2024-10-19T10:00:00"
}
```

### 2. Создать продукт (без изображения)

```bash
curl -X POST "http://localhost:8000/admin/api/v1/products/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Lenovo ThinkPad",
    "description": "Надежный бизнес-ноутбук",
    "image": "placeholder.jpg",
    "is_active": true,
    "category_id": 1
  }'
```

Ответ:
```json
{
  "id": 1,
  "name": "Lenovo ThinkPad",
  "description": "Надежный бизнес-ноутбук",
  "image": "placeholder.jpg",
  "is_active": true,
  "category_id": 1,
  "created_at": "2024-10-19T10:05:00",
  "updated_at": "2024-10-19T10:05:00"
}
```

### 3. Загрузить изображение продукта

```bash
curl -X POST "http://localhost:8000/admin/api/v1/products/1/upload-image" \
  -F "file=@laptop.jpg"
```

### 4. Загрузить файлы для продукта

```bash
# Загружаем инструкцию
curl -X POST "http://localhost:8000/admin/api/v1/files/upload?product_id=1" \
  -F "file=@manual.pdf"

# Загружаем спецификации
curl -X POST "http://localhost:8000/admin/api/v1/files/upload?product_id=1" \
  -F "file=@specifications.xlsx"

# Загружаем презентацию
curl -X POST "http://localhost:8000/admin/api/v1/files/upload?product_id=1" \
  -F "file=@presentation.pptx"
```

### 5. Получить продукт со всеми файлами

```bash
# Получить информацию о продукте
curl "http://localhost:8000/admin/api/v1/products/1"

# Получить все файлы продукта
curl "http://localhost:8000/admin/api/v1/files/?product_id=1"
```

## 🗑️ Удаление файлов

### Удаление файла (автоматически удаляется из файловой системы)

```bash
curl -X DELETE "http://localhost:8000/admin/api/v1/files/5"
```

### Удаление продукта (автоматически удаляются изображение и все связанные файлы)

```bash
curl -X DELETE "http://localhost:8000/admin/api/v1/products/1"
```

## 🔒 Безопасность

### Валидация файлов

1. **Проверка расширения**: Допускаются только файлы с разрешенными расширениями
2. **Уникальные имена**: Каждый файл получает уникальное имя (UUID) для предотвращения конфликтов
3. **Изоляция по продуктам**: Файлы каждого продукта хранятся в отдельной директории

### Ограничения

- Максимальный размер файла определяется настройками FastAPI (по умолчанию ограничений нет)
- Для production рекомендуется добавить ограничение размера файла

## 📊 Примеры с JavaScript/TypeScript

### Загрузка изображения (React)

```typescript
const uploadProductImage = async (productId: number, file: File) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(
    `http://localhost:8000/admin/api/v1/products/${productId}/upload-image`,
    {
      method: 'POST',
      body: formData,
    }
  );

  return await response.json();
};

// Использование
const handleImageUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
  const file = event.target.files?.[0];
  if (file) {
    const result = await uploadProductImage(1, file);
    console.log('Изображение загружено:', result);
  }
};
```

### Загрузка файла (React)

```typescript
const uploadProductFile = async (productId: number, file: File) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(
    `http://localhost:8000/admin/api/v1/files/upload?product_id=${productId}`,
    {
      method: 'POST',
      body: formData,
    }
  );

  return await response.json();
};

// Использование
const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
  const file = event.target.files?.[0];
  if (file) {
    const result = await uploadProductFile(1, file);
    console.log('Файл загружен:', result);
  }
};
```

## 🎨 Пример компонента загрузки (React)

```tsx
import React, { useState } from 'react';

const FileUploadComponent: React.FC<{ productId: number }> = ({ productId }) => {
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');

  const handleUpload = async (
    event: React.ChangeEvent<HTMLInputElement>,
    type: 'image' | 'file'
  ) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setUploading(true);
    setMessage('');

    try {
      const formData = new FormData();
      formData.append('file', file);

      const url =
        type === 'image'
          ? `/admin/api/v1/products/${productId}/upload-image`
          : `/admin/api/v1/files/upload?product_id=${productId}`;

      const response = await fetch(`http://localhost:8000${url}`, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        setMessage(`✅ Файл успешно загружен: ${result.name || result.image}`);
      } else {
        const error = await response.json();
        setMessage(`❌ Ошибка: ${error.detail}`);
      }
    } catch (error) {
      setMessage(`❌ Ошибка загрузки: ${error}`);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <h3>Загрузка файлов для продукта #{productId}</h3>

      <div>
        <label>
          Загрузить изображение:
          <input
            type="file"
            accept="image/*"
            onChange={(e) => handleUpload(e, 'image')}
            disabled={uploading}
          />
        </label>
      </div>

      <div>
        <label>
          Загрузить документ:
          <input
            type="file"
            accept=".pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx"
            onChange={(e) => handleUpload(e, 'file')}
            disabled={uploading}
          />
        </label>
      </div>

      {uploading && <p>⏳ Загрузка...</p>}
      {message && <p>{message}</p>}
    </div>
  );
};

export default FileUploadComponent;
```

## 📝 Примечания

1. **Автоматическая очистка**: При удалении файла из БД, он автоматически удаляется из файловой системы
2. **Замена изображений**: При загрузке нового изображения для продукта, старое автоматически удаляется
3. **Каскадное удаление**: При удалении продукта удаляются все связанные файлы и изображение
4. **Чистые имена директорий**: Названия продуктов очищаются от спецсимволов при создании директорий

## 🚀 Интеграция с фронтендом

### Отображение изображения продукта

```html
<img src="http://localhost:8000/images/{{ product.image }}" alt="{{ product.name }}" />
```

### Ссылка на скачивание файла

```html
<a href="http://localhost:8000/files/{{ file.path }}" download>
  Скачать {{ file.name }}
</a>
```

## 🔍 Тестирование через Swagger UI

1. Откройте http://localhost:8000/admin/docs
2. Найдите эндпоинт `POST /admin/api/v1/products/{product_id}/upload-image`
3. Нажмите "Try it out"
4. Введите ID продукта
5. Выберите файл
6. Нажмите "Execute"

Аналогично для загрузки файлов через эндпоинт `/admin/api/v1/files/upload`

