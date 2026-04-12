# Profile Service

Сервис управления профилями пользователей на `FastAPI` и `SQLAlchemy Async`.

## Требования

- `Python 3.12+`
- `PostgreSQL 16+`
- `venv` или другое виртуальное окружение

## Переменные окружения

Сервис читает настройки из `.env`. Для локального запуска достаточно таких переменных:

```env
DB_PROFILE_SERVICE_HOST=127.0.0.1
DB_PROFILE_SERVICE_PORT=5432
DB_PROFILE_SERVICE_NAME=profile_db
DB_PROFILE_SERVICE_USER=platform
DB_PROFILE_SERVICE_PASS=12345
DEBUG=false
```

Важно: значение `DEBUG` должно быть булевым, например `true` или `false`.

## Локальный запуск

1. Создайте и активируйте виртуальное окружение:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Установите зависимости:

```bash
pip install -r requirements.txt
```

3. Поднимите PostgreSQL и создайте базу `profile_db`.

Пример через Docker:

```bash
docker run --name profile-db \
  -e POSTGRES_DB=profile_db \
  -e POSTGRES_USER=platform \
  -e POSTGRES_PASSWORD=12345 \
  -p 5432:5432 \
  -d postgres:16
```

4. Примените миграции:

```bash
venv/bin/alembic upgrade head
```

5. Запустите сервис:

```bash
venv/bin/uvicorn main:app --reload
```

## Проверка

После запуска сервис доступен по адресам:

- `http://127.0.0.1:8000/health`
- `http://127.0.0.1:8000/api/profile/docs`
- `http://127.0.0.1:8000/api/profile/openapi.json`

## Тесты

Установка тестовых зависимостей:

```bash
pip install -r requirements.test.txt
```

Запуск тестов:

```bash
venv/bin/pytest
```
