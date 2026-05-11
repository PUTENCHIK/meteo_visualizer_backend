# Backend проекта MeteoVisualizer

## О проекте

### Описание

Бэкенд фулстек-приложения визуализации измерений датчиков сети мачтовых комплексов МАМКА. Предоставляет REST API приложения, эндпоинты авторизации и вебсокет-подключения для получения данных от API источника через программный шлюз.

Дополнительная информация о разработке размещена в [документе](./_docs/CodeCases.md).

### Стек технологий

* **Фреймворк**: FastAPI
* **Язык**: Python 3.12+
* **СУБД**: PostgreSQL (драйвер asyncpg)
* **Кэш**: Redis
* **ORM**: SQLModel (SQLAlchemy + Pydantic)
* **Миграции**: Alembic
* **Безопасность**: PyJWT, pwdlib (argon2)
* **Linting/Formatting**: Ruff

## Развёртывание

### Общий старт

1. Клонирование репозитория:
    ```bash
    git clone https://github.com/PUTENCHIK/meteo_visualizer_backend.git
    cd meteo_visualizer_backend
    ```

2. Настройка окружения. Скопировать `.env.example` или `.env.docker.example`, в зависисмости от способа поднятия, и переименовать в `.env` и `.env.docker`. В качестве окружения будет использоваться соответствующий файл. Поменять переменные окружения:

    * `POSTGRES_USER`. Пользователь Postgre, от имени которого будут открываться сессии с БД. Должен иметь права на указанную БД. По умолчанию установлен суперпользователь postgres, но для локальной разработки лучше поменять на создаваемого пользователя с правами на БД.
    * `POSTGRES_PASSWORD`. Указать настоящий пароль пользователя БД.
    * `POSTGRES_DB`. Название базы, к которой подключается приложение.
    * `DATABASE_URL`. Заполняемый на основании предыдущих переменных URL подключения к БД. Менять не нужно, только если Postgre использует не дефолтный порт 5432.

    * `REDIS_URL`. Для локальной разработки менять не нужно, только если при установке не указывался другой порт. Для Docker менять только если для службы Redis указывается другой порт.

    * `APP_HOST`. Хост, на котором разворачивается приложение.
    
        - **Локально**. Можно поменять на localhost для ограничения источников, которые могут обращаться к приложению, но тогда фронтенд тоже должен быть на том же компьюторе и localhost.
        - **Docker**. Оставить 0.0.0.0, иначе фронтенд не будет иметь доступа.

    * `APP_PORT`. Порт, на котором разворачивается приложение.
    * `APP_RELOAD`. Перезагрузка FastAPI при изменениях в исходных файлах.
    * `ALLOW_ORIGINS`. Список источников CORS, которые могут делать запросы к API. Указать адреса с портом, на котором будет развёрнут фронтенд.

    * `AUTH_TOKEN_SECRET_KEY`. Секретный ключ, использующийся для JWT токенов. Обязательно поменять на случайный, минимум 32-байтный ключ.
    * `AUTH_TOKEN_ALGORITHM`. Алгоритм шифрования JWT.

    * `INITIAL_DATA_PATH`. Путь к конфигурационному файлу с данными инициализации. При использовании указанного по умолчанию создаётся 2 роли и суперпользователь.
    * `INITIAL_USERS_PASSWORD`. Использующийся для создания пользователей из данных инициализации общий пароль. Сам пароль инициализации можно поменять на другой, а после поднятия приложения после авторизации поменять на личный.

### Локально

#### База данных Postgre

1. Установка Postgre:
    ```bash
    sudo apt update
    sudo apt install postgresql postgresql-contrib -y
    ```

2. Запуск сервиса:
    ```bash
    sudo systemctl start postgresql
    sudo systemctl enable postgresql
    ```

3. Создание базы данных и пользователя
    ```bash
    # Переходим в оболочку postgres
    sudo -i -u postgres psql
    ```

    ```sql
    -- Создаем базу данных
    CREATE DATABASE meteo_visualizer;

    -- Создаем пользователя с паролем
    CREATE USER meteo_user WITH PASSWORD 'your_password';

    -- Даем пользователю права на базу
    GRANT ALL PRIVILEGES ON DATABASE meteo_visualizer TO meteo_user;

    -- Для современных версий Postgres (15+) нужно также дать права на схему public:
    \c meteo_visualizer
    GRANT ALL ON SCHEMA public TO meteo_user;

    -- Выход
    \q
    ```

#### Хранилище Redis

1. Установка Redis:
    ```bash
    sudo apt update
    sudo apt install redis-server -y
    ```

2. Запуск сервиса:
    ```bash
    sudo systemctl start redis-server
    sudo systemctl enable redis-server
    ```

3. Проверка статуса и порта Redis:
    ```bash
    redis-cli ping
    ```

#### Приложение FastAPI

1. Создание виртуального окружения (опционально):
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

2. Установка зависимостей
    ```bash
    pip install -r requirements.txt
    ```

3. Применение миграций Alembic:
    ```bash
    alembic upgrade head
    ```

4. Запуск uvicorn сервер:
    ```bash
    python main.py
    ```

### Docker

1. После настройки `.env.docker`, поднять контейнер:

    ```bash
    docker compose --env-file .env.docker up -d --build
    ```

## Структура проекта

```
.
├── src/                    # Исходный код
│   ├── auth/               # JWT-авторизация
│   ├── db/                 # Соедниение с БД
│   ├── factories/          # Фабрики
│   ├── managers/           # Менеджеры
│   ├── models/             # ORM-модели
│   ├── repositories/       # Репозитории
│   ├── routers/            # Роутеры
│   ├── schemas/            # Pydantic-схемы
│   ├── services/           # Сервисы
│   ├── utils/              # Дополнительные инструменты
│   └── config.py           # Класс для загрузки .env
├── _docs_/                 # Дополнительные MD
├── initial_data/           # Папка с YAML данными инициализации
├── migrations/             # Миграции Alembic
├── tests/                  # Тесты Pytest
│   └── conftest.py         # Конфигурация и фикстуры тестов
├── .env                    # Файл локального окружения (игнорируется Git)
├── .env.docker             # Файл окружения Docker (игнорируется Git)
├── .env.example            # Пример файла локального окружения
├── .env.docker.example     # Пример файла окружения Docker
├── .coveragerc             # Файл конфигурации для coverage
├── .editorconfig           # Конфигурация редакторов кода
├── alembic.ini             # Конфигурация Alembic
├── pytest.ini              # Конфигурация Pytest
├── pyproject.toml          # Настройки Ruff и инструментов сборки
├── app.py                  # Приложение FastAPI
├── main.py                 # Точка входа в приложение; сервер uvicorn
├── docker-compose.yml      # Описание инфраструктуры Docker
├── Dockerfile              # Инструкция для сборки образа приложения
└── requirements.txt        # Список зависимостей
```

## API приложения

Автогенерируемое API доступно при запуске по маршруту `/docs`.

## Тестирование

Используется `Pytest`. Реализованы шаблонные модульные тесты.

Запуск тестов автоматической генерацией отчётов о покрытии кода:
```bash
pytest
```