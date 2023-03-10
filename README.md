# TODOList

## Данный дипломный проект представляет собой backend-часть для сайта планирования задач.

Проект использует следующие технологии:

- [Django](https://www.djangoproject.com/) - Django makes it easier to build better web apps more quickly and with less code.
- [Django-rest-framework](https://www.django-rest-framework.org/) - Django REST framework is a powerful and flexible toolkit for building Web APIs.
- [Django-filter](https://django-filter.readthedocs.io/en/stable/#) - Django-filter is a generic, reusable application to alleviate writing some of the more mundane bits of view code. Specifically, it allows users to filter down a queryset based on a model’s fields, displaying the form to let them do this.
- [Postgresql](https://www.postgresql.org/) - The World's Most Advanced Open Source Relational Database.
- [Djoser](https://djoser.readthedocs.io/en/latest/getting_started.html) - REST implementation of Django authentication system. djoser library provides a set of Django Rest Framework views to handle basic actions such as registration, login, logout, password reset and account activation. It works with custom user model.
- [Drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/) - Sane and flexible OpenAPI 3.0 schema generation for Django REST framework.
- [Pydantic](https://docs.pydantic.dev/) - Data validation and settings management using Python type annotations.
- [Redis](https://redis.io/) - The open source, in-memory data store used by millions of developers as a database, cache, streaming engine, and message broker.

## Installation

### 1. Создать виртуальное окружение.

```sh
# для активации окружения
poetry shell
```
```sh
# для первичной установки
poetry install
```
```sh
# для обновления
poetry update
```

### 2. Создайте свой .env фаил в корне проекта.

### 3. Заполнить .env фаил:
```xml
DB_ENGINE=django.db.backends.postgresql
DB_NAME=todolist
DB_USER=todolist
DB_PASSWORD=todolist
DB_HOST=localhost
DB_PORT=5432
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=todolist@gmail.com
EMAIL_HOST_PASSWORD=todolist
EMAIL_PORT=587
SECRET_KEY='todolist'
DEBUG=True
DOCKER_HUB_USERNAME=todolist
OAUTH2_KEY=111111
OAUTH2_SECRET=1111111
TOKEN_TELEGRAM_BOT=727257272:AAHLdsfdsfdsfdsfdsf
```

### 4. Запустить образ postgres из корня проекта.
```sh
docker-compose up postgres
```

### 5. Выполнить миграции.
```sh
./manage.py migrate 
```

### 6. Запустить сервер.
```sh
./manage.py runserver 0.0.0.0:8000  
```

### 7. Запустить образ redis из корня проекта.
```sh
docker-compose up redis
```

### 8. Запустить telegram-bot:
```sh
./manage.py runbot
```

### 9. Запустить образ frontend:
```sh
docker-compose up front
```

### 10. Для локального запуска всех образов, выполнить из корня проекта.
```sh
docker-compose up --build -d
```

## Testing

### 1. Запустить образ postgres из корня проекта.
```sh
docker-compose up postgres
```

### 2. Запустить тесты
```sh
pytest
```