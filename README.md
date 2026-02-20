Вот переписанная версия README — уже под **Profile Service в микросервисной архитектуре**, без лишнего про auth-логику внутри сервиса.

---

# 👤 Profile Service

Микросервис управления профилями пользователей.
Отвечает за хранение и управление персональными данными пользователя (CRUD).

Сервис является частью микросервисной архитектуры и работает за **API Gateway**.

> ⚠️ Авторизация и аутентификация выполняются отдельным Auth-сервисом.

---

# 🏗 Стек технологий

* **Python 3.12+**
* **FastAPI** — веб-фреймворк
* **SQLAlchemy 2.0 (Async)** — ORM
* **PostgreSQL** — база данных
* **Alembic** — миграции
* **Pydantic v2** — валидация данных
* **Pytest** — тестирование
* **Docker** — контейнеризация

---

# 🗃 Модель данных (Profile)

Основная сущность сервиса — **Profile**.

> ⚠️ `user_id` — это идентификатор пользователя из Auth-сервиса.
> В базе нет ForeignKey и связей между сервисами.

| Поле           | Тип         | Описание                         | Ограничения          |
| -------------- | ----------- | -------------------------------- | -------------------- |
| `id`           | `Integer`   | Уникальный идентификатор профиля | Primary Key          |
| `user_id`      | `Integer`   | ID пользователя из Auth-сервиса  | Index, Not Null      |
| `first_name`   | `String`    | Имя                              | Optional, max 100    |
| `last_name`    | `String`    | Фамилия                          | Optional, max 100    |
| `phone_number` | `String`    | Телефон                          | Unique, Optional     |
| `avatar_url`   | `String`    | Ссылка на аватар                 | Optional             |
| `created_at`   | `Timestamp` | Дата создания                    | server_default=now() |
| `updated_at`   | `Timestamp` | Дата обновления                  | auto-update          |

---

# 🔌 API Endpoints

## 📌 Создание профиля

```
POST /profiles
```

## 📌 Получение профиля по user_id

```
GET /profiles/{user_id}
```

## 📌 Получение своего профиля

```
GET /profiles/me
```

## 📌 Обновление своего профиля

```
PATCH /profiles/me
```

## 📌 Удаление профиля

```
DELETE /profiles/{user_id}
```

---

# 🛡 Архитектура безопасности

⚠️ Profile Service:

* ❌ НЕ проверяет JWT
* ❌ НЕ занимается аутентификацией
* ❌ НЕ хранит пароли

Авторизация выполняется **API Gateway** + **Auth Service**.

Gateway передаёт `user_id` через заголовки или dependency.

---

# 🔄 Взаимодействие между сервисами

Типичный сценарий:

1. Пользователь регистрируется в Auth Service
2. Auth Service:

   * либо делает HTTP-запрос в Profile Service
   * либо отправляет событие (Kafka / RabbitMQ)
3. Profile Service создаёт профиль с `user_id`

---

# 🚀 Производительность и масштабирование

* Кеширование — планируется Redis (для `/profiles/me`)
* Rate limiting — реализован на уровне API Gateway
* Масштабирование — горизонтальное через Docker/Kubernetes

---

# 🐳 Запуск через Docker

### docker-compose.yml (пример)

```yaml
version: "3.9"

services:
  db:
    image: postgres:16
    container_name: profile_db
    restart: always
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: profile_db
    ports:
      - "5432:5432"
    volumes:
      - pg_data:/var/lib/postgresql/data

volumes:
  pg_data:
```

---

# 🛠 Локальный запуск (Development)

### 1️⃣ Предварительные требования

* Python 3.12+
* Docker
* PostgreSQL (если без Docker)

---

### 2️⃣ Создание виртуального окружения

```bash
python -m venv venv
```

#### Windows

```bash
.\venv\Scripts\activate
```

#### macOS / Linux

```bash
source venv/bin/activate
```

---

### 3️⃣ Установка зависимостей

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Настройка переменных окружения

Создать `.env`:

```
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/profile_db
```

---

### 5️⃣ Применение миграций

```bash
alembic upgrade head
```

---

### 6️⃣ Запуск сервиса

```bash
uvicorn main:app --reload
```

Сервис будет доступен:

```
http://127.0.0.1:8000
```

Swagger:

```
http://127.0.0.1:8000/docs
```

---

# 🧪 Тестирование

```bash
pytest
```

---

# 📦 Будущие улучшения

* Redis кеширование профиля
* Event-driven синхронизация с Auth
* Soft delete вместо hard delete
* Observability (Prometheus + Grafana)
* Centralized logging

---