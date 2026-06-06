# DjangoApp by Gleb

Веб-приложение на Django для загрузки JSON-файлов

## Требования

- Python 3.14+
- Docker и Docker Compose
- Git

## Развёртывание (runserver)

1. Создайте и активируйте виртуальное окружение:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

3. Создайте файл переменных окружения:

   ```bash
   cp .env.example .env
   ```

   При необходимости отредактируйте `.env` — параметры подключения к PostgreSQL и данные суперпользователя.

4. Запустите PostgreSQL в Docker:

   ```bash
   docker compose up -d db
   ```

5. Примените миграции:

   ```bash
   python manage.py migrate
   ```

6. Создайте суперпользователя:

   ```bash
   python manage.py createsuperuser
   ```

   Либо используйте переменные из `.env` для автоматического создания:

   ```bash
   python manage.py createsuperuser --noinput
   ```

7. Запустите сервер разработки:

   ```bash
   python manage.py runserver
   ```

8. Откройте в браузере:

   - Загрузка JSON: http://127.0.0.1:8000/
   - Список записей: http://127.0.0.1:8000/items/
   - Админ-панель: http://127.0.0.1:8000/admin/

## Формат JSON-файла

```json
[
    {
        "name": "random string less than 50 characters",
        "date": "2026-06-06_14:30"
    }
]
```

- Обязательные ключи: `name` (строка, менее 50 символов), `date` (формат `YYYY-MM-DD_HH:mm`).
- Лишние ключи игнорируются.
- При ошибке хотя бы в одном элементе файл не сохраняется, пользователю показываются сообщения об ошибках.

## Запуск тестов

```bash
python3 manage.py test
```

## Стек

- Django 6
- PostgreSQL 16 (Docker)
- DataTables 2.2.2 (CDN)
